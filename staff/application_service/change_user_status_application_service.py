from typing import Any
import logging
from django.contrib.auth.models import User
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from staff.domain_service.auth_domain_service import AuthDomainService
from staff.domain_service.user_domain_service import UserDomainService
from staff.types.dataclass import ChangeUserStatusRequest

class ChangeUserStatusApplicationService:
    '''
    Application service for changing user active status.
    Handles authorization and orchestrates status change.
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_domain_service: AuthDomainService = AuthDomainService()
        self.user_domain_service: UserDomainService = UserDomainService()
    
    def change_user_status(
        self, 
        system_user_id: int,
        status_request: ChangeUserStatusRequest,
        requesting_user: User
    ) -> dict[str, Any]:
        '''
        Change user active status if requesting user is administrative.
        
        Args:
            system_user_id: ID of the SystemUser record
            status_request: ChangeUserStatusRequest with new status
            requesting_user: User making the request
            
        Returns:
            dictionary with response data and status
        '''
        try:
            # Step 1: Verify requesting user is administrative
            is_admin: bool = self.auth_domain_service.is_administrative_user(requesting_user)
            if not is_admin:
                self.logger.warning(
                    f'Non-administrative user {requesting_user.username} attempted to change user status'
                )
                return {
                    'response': 'No tienes permiso para cambiar el estado del usuario.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_403_FORBIDDEN
                }
            # Step 2: Change user status through domain service
            success: bool
            message: str
            user: User | None
            success, message, user = self.user_domain_service.change_user_active_status(
                system_user_id=system_user_id,
                new_status=status_request.status
            )
            if not success:
                # Check if user not found
                if 'no encontrado' in message.lower():
                    return {
                        'response': message,
                        'msg': self.FAILURE,
                        'status_code_http': HTTP_404_NOT_FOUND
                    }
                # Other errors (superuser, already same status, etc.)
                return {
                    'response': message,
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_400_BAD_REQUEST
                }
            # Step 3: Build success response
            self.logger.info(
                f'User {requesting_user.username} changed status of system_user_id {system_user_id} to {status_request.status}'
            )
            return {
                'response': message,
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'new_status': user.is_active
                }
            }
        except Exception as e:
            self.logger.error(
                f'Error changing user status for system_user_id {system_user_id}: {str(e)}',
                exc_info=True
            )
            return {
                'response': 'Ocurrió un error al cambiar el estado del usuario.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }