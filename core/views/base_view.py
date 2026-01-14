from django.conf import settings
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from typing import (
    Any, 
    Callable,
    Type
)
import logging

class BaseView(APIView):
    '''
    Base view class providing common functionality for all API endpoints.
    
    This class implements the Template Method pattern, providing a standardized
    way to handle requests with built-in validation, authentication, and error
    handling. All custom API views should inherit from this class.
    
    Features:
        - Automatic serializer validation
        - Authentication verification
        - Consistent error response formatting
        - Centralized exception handling
        - Standardized service layer integration
    
    Usage:
        class MyCustomView(BaseView):
            def post(self, request: Request) -> Response:
                return self._handle_request(
                    request=request,
                    serializer_class=MySerializer,
                    service_method_callback=self._process_data,
                    requires_auth=True
                )
            
            def _process_data(
                self, 
                validated_data: dict[str, Any], 
                user: User
            ) -> dict[str, Any]:
                # Your business logic here
                return {'response': 'Success', 'msg': 1}
    
    Design Pattern:
        Template Method - _handle_request() defines the algorithm skeleton,
        with child classes providing specific implementations via callbacks.
    
    Attributes:
        logger (logging.Logger): Logger instance for this view
    '''
    SUCCESS: int = 1
    ERROR: int = -1

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # PROTECTED METHODS - Usage by child classes only
    # ------------------------------------------------------------------
    def _handle_request(
        self,
        request: Request,
        serializer_class: Type[serializers.Serializer] | None,
        service_method_callback: Callable,
        requires_auth: bool = True
    ) -> Response:
        '''
        Template method for handling API requests with standardized flow.
        
        This method orchestrates the entire request handling process:
        1. Authentication validation (if required)
        2. Input data validation (if serializer provided)
        3. Service layer invocation
        4. Response formatting
        5. Error handling
        
        Args:
            request: The incoming HTTP request object
            serializer_class: Serializer class for input validation (None to skip)
            service_method_callback: Function that processes the request
                                   Signature: (validated_data, user) -> dict
                                   or: (user) -> dict if no serializer
            requires_auth: Whether to verify user authentication (default: True)
        
        Returns:
            Response: Formatted HTTP response with status code
        
        Example:
            def post(self, request: Request) -> Response:
                return self._handle_request(
                    request=request,
                    serializer_class=CreateUserSerializer,
                    service_method_callback=self._create_user,
                    requires_auth=False
                )
            
            def _create_user(
                self, 
                validated_data: dict[str, Any], 
                user: User
            ) -> dict[str, Any]:
                return UserService.create(validated_data)
        
        Notes:
            - Service callback must return dict with 'msg' key
            - msg == -1 indicates error, anything else is success
            - All exceptions are caught and converted to 500 responses
        '''
        try:
            # Step 1: Validate authentication if required
            if requires_auth:
                auth_error: Response | None = self._validate_authentication(request)
                if auth_error:
                    return auth_error
            # Step 2: Validate input data if serializer provided
            validated_data: dict[str, Any] | None = None
            if serializer_class:
                validated_data, validation_error = self._validate_serializer(
                    serializer_class, 
                    request.data
                )
                if validation_error:
                    return validation_error
            # Step 3: Invoke service layer
            if requires_auth:
                # Protected API - pass user to callback
                if validated_data is not None:
                    service_response = service_method_callback(validated_data, request.user)
                else:
                    service_response = service_method_callback(request.user)
            else:
                # Public API - don't pass user to callback
                if validated_data is not None:
                    service_response = service_method_callback(validated_data)
                else:
                    service_response = service_method_callback()
            # Step 4: Format and return response
            return self._handle_service_response(service_response)
        except Exception as e:
            return self._handle_unexpected_error(e)

    def _validate_serializer(
        self, 
        serializer_class: Type[serializers.Serializer], 
        data: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, Response | None]:
        '''
        Validate input data against a serializer schema.
        
        This method creates a serializer instance, validates the input data,
        and returns either the validated data or a formatted error response.
        
        Args:
            serializer_class: Django REST Framework serializer class
            data: Dictionary of input data to validate
        
        Returns:
            tuple: (validated_data, error_response)
                - If validation succeeds: (dict, None)
                - If validation fails: (None, Response)
        
        Example:
            validated_data, error = self.__validate_serializer(
                UserSerializer, 
                {'username': 'john', 'email': 'invalid'}
            )
            if error:
                return error
        
        Notes:
            - This is a private method, use _handle_request() instead
            - Errors include field-specific validation messages
        '''
        serializer: serializers.Serializer = serializer_class(data=data)
        if not serializer.is_valid():
            self.logger.warning(
                f'Validation failed: {serializer.errors}'
            )
            return None, Response(
                {
                    'response': 'Invalid input data.',
                    'msg': self.ERROR,
                    'errors': serializer.errors
                },
                status=HTTP_400_BAD_REQUEST
            )
        return serializer.validated_data, None

    def _validate_authentication(
        self, 
        request: Request
    ) -> Response | None:
        '''
        Verify that the request has valid authentication credentials.
        
        Checks if the user is authenticated and has a valid session/token.
        
        Args:
            request: The HTTP request object containing user information
        
        Returns:
            Response | None: 
                - None if authentication is valid
                - 401 Response if authentication fails
        
        Example:
            error = self.__validate_authentication(request)
            if error:
                return error
        
        Notes:
            - This is a private method, use _handle_request() instead
            - Relies on DRF's authentication classes configured in settings
        '''
        if not request.user or not request.user.is_authenticated:
            self.logger.warning(
                f'Unauthenticated access attempt to {self.__class__.__name__}'
            )
            return Response(
                {
                    'response': 'Authentication credentials were not provided or are invalid.',
                    'msg': self.ERROR,
                },
                status=HTTP_401_UNAUTHORIZED
            )
        return None

    def _handle_service_response(
        self, 
        service_response: dict[str, Any], 
        success_status: int = HTTP_200_OK,
        error_status: int = HTTP_400_BAD_REQUEST
    ) -> Response:
        '''
        Convert service layer response into HTTP response with appropriate status.
        
        Interprets the 'msg' field from service response to determine if the
        operation was successful or failed, then formats the HTTP response.
        
        Args:
            service_response: Dictionary returned from service layer
                            Must contain 'msg' key (-1 for error, else success)
            success_status: HTTP status code for successful operations (default: 200)
            error_status: HTTP status code for failed operations (default: 400)
        
        Returns:
            Response: Django REST Framework response object
        
        Example:
            service_result = UserService.create_user(data)
            # service_result = {'response': 'User created', 'msg': 1, 'user_id': 123}
            return self.__handle_service_response(service_result)
        
        Convention:
            Service responses should follow this structure:
            - Success: {'response': 'message', 'msg': 1, ...other_data}
            - Error: {'response': 'error message', 'msg': -1}
        
        Notes:
            - This is a private method, use _handle_request() instead
        '''
        # Get HTTP status code from service response
        status_code: int | None = service_response.get('status_code_http')
        if status_code is None:
            if service_response.get('msg') == self.ERROR:
                self.logger.info(f'Service returned error: {service_response.get("response")}')
                return Response(
                    service_response, 
                    status=error_status
                )
            else:
                return Response(
                    service_response, 
                    status=success_status
                )
        else:
            return Response(
                service_response,
                status=status_code
            )

    def _handle_unexpected_error(
        self, 
        exception: Exception
    ) -> Response:
        '''
        Handle unexpected exceptions with environment-aware error exposure.
        
        Logs the full exception and returns a sanitized error response.
        In DEBUG mode, includes exception details for development.
        In production, returns generic error message for security.
        
        Args:
            exception: The caught exception
        
        Returns:
            Response: 500 Internal Server Error response
        
        Security:
            - Production (DEBUG=False): Generic error message only
            - Development (DEBUG=True): Full exception details included
        
        Example:
            # In production
            {
                "response": "An unexpected error occurred. Please try again later.",
                "msg": -1,
                "error_detail": null
            }
            
            # In development
            {
                "response": "An unexpected error occurred. Please try again later.",
                "msg": -1,
                "error_detail": "AttributeError: 'NoneType' object has no attribute 'id'"
            }
        
        Notes:
            - Always logs full exception with stack trace
            - Error detail only exposed when settings.DEBUG is True
        '''
        # Log full exception details (always logged, even in production)
        self.logger.error(
            f'Unexpected error in {self.__class__.__name__}: {str(exception)}',
            exc_info=True,  # Includes full stack trace in logs
            extra={
                'view_class': self.__class__.__name__,
                'exception_type': type(exception).__name__,
            }
        )
        # Prepare response based on environment
        response_data: dict[str, Any] = {
            'response': 'An unexpected error occurred. Please try again later.',
            'msg': self.ERROR,
        }
        # Only include error details in development
        if settings.DEBUG:
            response_data['error_detail'] = str(exception)
            response_data['exception_type'] = type(exception).__name__
        return Response(
            response_data,
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )