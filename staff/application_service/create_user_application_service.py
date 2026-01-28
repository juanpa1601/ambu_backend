from typing import Any
import logging
from django.contrib.auth.models import User
from staff.domain_service import (
    AuthDomainService, 
    UserDomainService
)
from staff.types.dataclass import CreateUserRequest
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class CreateUserApplicationService:
    '''
    Application service for creating new users with staff profiles.
    Handles authorization and orchestrates user creation.
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1    

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_domain_service: AuthDomainService = AuthDomainService()
        self.user_domain_service: UserDomainService = UserDomainService()
    
    def create_user(
        self, 
        user_request: CreateUserRequest,
        requesting_user: User
    ) -> dict[str, Any]:
        '''
        Create a new user if requesting user is administrative or superuser.
        
        Args:
            user_request: CreateUserRequest with user data
            requesting_user: User making the request
            
        Returns:
            dictionary with response data and status
        '''
        try:
            # Step 1: Verify requesting user is administrative or superuser
            is_admin: bool = self.auth_domain_service.is_administrative_user(requesting_user)
            is_superuser: bool = requesting_user.is_superuser
            if not (is_admin or is_superuser):
                self.logger.warning(
                    f'User {requesting_user.username} attempted to create user without permission'
                )
                return {
                    'response': 'No tienes permiso para crear usuarios.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_403_FORBIDDEN
                }
            # Step 2: Create user through domain service
            success: bool
            message: str
            response_data: CreateUserRequest
            success, message, response_data = self.user_domain_service.create_user_with_staff_profile(
                user_request=user_request
            )
            if not success:
                # Check specific error types
                if 'ya existe' in message.lower():
                    return {
                        'response': message,
                        'msg': self.FAILURE,
                        'status_code_http': HTTP_400_BAD_REQUEST
                    }
                # Other errors
                return {
                    'response': message,
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
                }
            # Step 3: Build success response
            self.logger.info(
                f'User {requesting_user.username} created new user: {response_data.username} '
                f'(type: {response_data.staff_type})'
            )
            return {
                'response': message,
                'msg': self.SUCCESS,
                'status_code_http': HTTP_201_CREATED,
                'data': {
                    'system_user_id': response_data.system_user_id,
                    'username': response_data.username,
                    'email': response_data.email,
                    'base_staff_id': response_data.base_staff_id,
                    'staff_type': response_data.staff_type,
                    'created_at': response_data.created_at
                }
            }
        except Exception as e:
            self.logger.error(
                f'Error in create user application service: {str(e)}',
                exc_info=True
            )
            return {
                'response': 'Ocurrió un error al crear el usuario.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }