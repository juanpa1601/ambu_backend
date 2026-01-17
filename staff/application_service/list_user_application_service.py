from typing import Any
import logging
from django.contrib.auth.models import User
from staff.domain_service import (
    UserDomainService,
    AuthDomainService
)
from staff.types.dataclass import UserListResponse

class ListUsersApplicationService:
    '''
    Application service for listing users.
    Handles authorization and orchestrates user retrieval.
    '''
    
    def __init__(self):
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
                    'response': 'You do not have permission to access this resource.',
                    'msg': -1,
                    'status_code': 403
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
                    'document_number': item.document_number
                }
                for item in user_items
            ]
            self.logger.info(
                f'User {requesting_user.username} successfully retrieved {len(user_items)} users'
            )
            return {
                'response': 'Users retrieved successfully.',
                'msg': 1,
                'status_code': 200,
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
                'response': 'An error occurred while retrieving users.',
                'msg': -1,
                'status_code': 500
            }