from typing import Any
import logging
from django.contrib.auth.models import User

from staff.types.dataclass import (
    LogoutRequest, 
    LogoutResponse
)
from staff.domain_service import AuthDomainService
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class LogoutApplicationService:
    '''
    Application service for logout operations.
    Orchestrates the logout process using domain services.
    '''

    SUCCESS: int = 1
    FAILURE: int = -1  

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_domain_service: AuthDomainService = AuthDomainService()
    
    def logout(
        self, 
        logout_request: LogoutRequest,
        user: User
    ) -> dict[str, Any]:
        '''
        Process user logout request.
        
        Args:
            logout_request: LogoutRequest dataclass with user information
            user: Authenticated User object from request
            
        Returns:
            dictionary with response data and status
        '''
        try:
            # Verify user consistency
            if user.id != logout_request.user_id:
                self.logger.warning(
                    f'User ID mismatch: token user {user.id} vs request user {logout_request.user_id}'
                )
                return {
                    'response': 'Credenciales inválidas.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_403_FORBIDDEN
                }
            # Check if user has an active token
            has_token: bool = self.auth_domain_service.verify_user_has_token(user)
            if not has_token:
                self.logger.info(f'User {user.username} attempted logout without active token')
                return {
                    'response': 'No se encontró una sesión activa.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_400_BAD_REQUEST
                }
            # Revoke the token
            token_revoked: bool = self.auth_domain_service.revoke_token(user)
            if not token_revoked:
                return {
                    'response': 'Error al cerrar sesión. Por favor, inténtalo de nuevo.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
                }
            # Build successful response
            logout_response: LogoutResponse = LogoutResponse(
                success=True,
                message='Cierre de sesión exitoso'
            )
            self.logger.info(f'User {user.username} logged out successfully')
            return {
                'response': logout_response.message,
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'data': {
                    'success': logout_response.success,
                    'username': user.username
                }
            }
        except Exception as e:
            self.logger.error(f'Error during logout for user {user.username}: {str(e)}', exc_info=True)
            return {
                'response': 'Ocurrió un error durante el cierre de sesión.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }