from typing import Any
import logging
from staff.types.dataclass import (
    LoginRequest, 
    LoginResponse
)
from django.contrib.auth.models import User
from staff.domain_service import AuthDomainService
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class LoginApplicationService:
    '''
    Application service for login operations.
    Orchestrates the login process using domain services.
    '''

    SUCCESS: int = 1
    FAILURE: int = -1    

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_domain_service: AuthDomainService = AuthDomainService()
    
    def login(
        self, 
        login_data: LoginRequest
    ) -> dict[str, Any]:
        '''
        Process user login request.
        
        Args:
            login_data: LoginRequest dataclass with username and password
            
        Returns:
            dictionary with response data and status
        '''
        try:
            # Step 1: Authenticate user
            user: User | None = self.auth_domain_service.authenticate_user(
                username=login_data.username,
                password=login_data.password
            )
            if user is None:
                return {
                    'response': 'Credenciales invalidas. Por favor, verifica tu username y password.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_403_FORBIDDEN
                }
            # Step 2: Generate tokens
            token: str = self.auth_domain_service.generate_token(user)
            # Step 3: Get staff type
            staff_type: str | None = self.auth_domain_service.get_staff_type(user)
            # Step 4: Build response
            login_response: LoginResponse = LoginResponse(
                access_token=token,
                system_user_id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.get_full_name() or user.username,
                staff_type=staff_type
            )
            self.logger.info(f'User {user.username} logged in successfully')
            return {
                'response': 'Inicio de sesión exitoso.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'data': {
                    'access_token': login_response.access_token,
                    'user': {
                        'id': login_response.system_user_id,
                        'username': login_response.username,
                        'email': login_response.email,
                        'full_name': login_response.full_name,
                        'staff_type': login_response.staff_type
                    }
                }
            }
        except Exception as e:
            self.logger.error(f'Error during login: {str(e)}', exc_info=True)
            return {
                'response': 'Ocurrió un error durante el inicio de sesión.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }