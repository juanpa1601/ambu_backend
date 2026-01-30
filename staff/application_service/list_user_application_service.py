from typing import Any
import logging
from django.contrib.auth.models import User
from staff.domain_service import (
    UserDomainService,
    AuthDomainService
)
from staff.types.dataclass import UserListResponse
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class ListUsersApplicationService:
    '''
    Application service for listing users.
    Handles authorization and orchestrates user retrieval.
    '''

    SUCCESS: int = 1
    FAILURE: int = -1    

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_domain_service: AuthDomainService = AuthDomainService()
        self.user_domain_service: UserDomainService = UserDomainService()
    
    def list_users(
        self, 
        requesting_user: User
    ) -> dict[str, Any]:
        '''
        List all staff users if requesting user is administrative.
        
        Args:
            requesting_user: User making the request
            
        Returns:
            dictionary with response data and status
        '''
        try:
            # Step 1: Verify user is administrative
            is_admin: bool = self.auth_domain_service.is_administrative_user(requesting_user)
            if not is_admin:
                self.logger.warning(
                    f'Non-administrative user {requesting_user.username} attempted to list users'
                )
                return {
                    'response': 'No tienes permiso para acceder a este recurso.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_403_FORBIDDEN
                }
            # Step 2: Get all staff users
            user_items: list[UserListResponse] = self.user_domain_service.get_all_staff_users()
            # Step 3: Build response
            users_data: list[dict[str, Any]] = [
                {
                    'system_user_id': item.system_user_id,
                    'full_name': item.full_name,
                    'is_active': item.is_active,
                    'document_type': item.document_type,
                    'document_number': item.document_number,
                    'type_personnel': item.type_personnel
                }
                for item in user_items
            ]
            self.logger.info(
                f'User {requesting_user.username} successfully retrieved {len(user_items)} users'
            )
            return {
                'response': 'Usuarios recuperados exitosamente.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'data': {
                    'users': users_data,
                    'total_count': len(user_items)
                }
            }
        except Exception as e:
            self.logger.error(
                f'Error listing users for {requesting_user.username}: {str(e)}',
                exc_info=True
            )
            return {
                'response': 'Ocurrió un error al recuperar los usuarios.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }