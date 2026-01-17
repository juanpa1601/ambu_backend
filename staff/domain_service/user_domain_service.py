from django.contrib.auth.models import User
from staff.models.base_staff import BaseStaff
from staff.types.dataclass import UserListItem
from typing import List
import logging

class UserDomainService:
    '''
    Domain service for user-related operations.
    '''
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_all_staff_users(self) -> List[UserListItem]:
        '''
        Retrieve all staff users with their basic information.
        
        Returns:
            List of UserListItem dataclasses
        '''
        try:
            # Query all BaseStaff with related system_user
            base_staff_list: List[BaseStaff] = BaseStaff.objects.select_related('system_user').all()
            user_items: List[UserListItem] = []
            for base_staff in base_staff_list:
                user: User = base_staff.system_user
                # Build full name
                full_name: str = user.get_full_name() or user.username
                user_item: UserListItem = UserListItem(
                    system_user_id=user.id,
                    full_name=full_name,
                    is_active=user.is_active,
                    document_type=base_staff.document_type,
                    document_number=base_staff.document_number
                )
                user_items.append(user_item)
            self.logger.info(f'Retrieved {len(user_items)} staff users')
            return user_items
        except Exception as e:
            self.logger.error(f'Error retrieving staff users: {str(e)}', exc_info=True)
            raise