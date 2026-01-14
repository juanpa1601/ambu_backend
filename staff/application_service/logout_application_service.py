from typing import Any
import logging
from django.contrib.auth.models import User

from staff.types.dataclass import (
    LogoutRequest, 
    LogoutResponse
)
from staff.domain_service import AuthDomainService

class LogoutApplicationService:
    '''
    Application service for logout operations.
    Orchestrates the logout process using domain services.
    '''
    
    def __init__(self):
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
            Dictionary with response data and status
        '''
        try:
            # Verify user consistency
            if user.id != logout_request.user_id:
                self.logger.warning(
                    f'User ID mismatch: token user {user.id} vs request user {logout_request.user_id}'
                )
                return {
                    'response': 'Invalid user credentials.',
                    'msg': -1,
                    'status': 403
                }
            # Check if user has an active token
            has_token: bool = self.auth_domain_service.verify_user_has_token(user)
            if not has_token:
                self.logger.info(f'User {user.username} attempted logout without active token')
                return {
                    'response': 'No active session found.',
                    'msg': -1,
                    'status': 400
                }
            # Revoke the token
            token_revoked: bool = self.auth_domain_service.revoke_token(user)
            if not token_revoked:
                return {
                    'response': 'Failed to logout. Please try again.',
                    'msg': -1,
                    'status': 500
                }
            # Build successful response
            logout_response: LogoutResponse = LogoutResponse(
                success=True,
                message='Logout successful'
            )
            self.logger.info(f'User {user.username} logged out successfully')
            return {
                'response': logout_response.message,
                'msg': 1,
                'status': 200,
                'data': {
                    'success': logout_response.success,
                    'username': user.username
                }
            }
        except Exception as e:
            self.logger.error(f'Error during logout for user {user.username}: {str(e)}', exc_info=True)
            return {
                'response': 'An error occurred during logout.',
                'msg': -1,
                'status': 500
            }