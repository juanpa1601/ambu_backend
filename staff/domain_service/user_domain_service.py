from django.contrib.auth.models import User
from staff.models.base_staff import BaseStaff
from staff.models.healthcare import Healthcare
from staff.models.driver import Driver
from staff.models.administrative import Administrative
from staff.types.dataclass import (
    UserListItem, 
    UserDetailResponse
) 
import logging

class UserDomainService:
    '''Domain service for user-related operations.'''
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_all_staff_users(self) -> list[UserListItem]:
        '''
        Retrieve all staff users with their basic information.
        
        Returns:
            list of UserListItem dataclasses
        '''
        try:
            # Query all BaseStaff with related system_user
            base_staff_list: list[BaseStaff] = BaseStaff.objects.select_related('system_user').all()
            user_items: list[UserListItem] = []
            for base_staff in base_staff_list:
                user: User = base_staff.system_user
                # Build full name
                full_name: str = user.get_full_name() or user.username
                user_item: UserListItem = UserListItem(
                    system_user_id=user.id,
                    full_name=full_name,
                    is_active=user.is_active,
                    document_type=base_staff.document_type,
                    document_number=base_staff.document_number,
                    type_personnel=base_staff.type_personnel
                )
                user_items.append(user_item)
            self.logger.info(f'Retrieved {len(user_items)} staff users')
            return user_items
        except Exception as e:
            self.logger.error(f'Error retrieving staff users: {str(e)}', exc_info=True)
            raise

    def get_user_detail_by_system_user_id(
        self, 
        system_user_id: int
    ) -> UserDetailResponse | None:
        '''
        Retrieve complete user details by system_user_id.
        
        Args:
            system_user_id: ID of the system_user (User model)
            
        Returns:
            UserDetailResponse dataclass with all user information or None
        '''
        try:
            # Get User directly by system_user_id
            user: User = User.objects.get(id=system_user_id)
            # Check if user has a BaseStaff profile
            try:
                base_staff: BaseStaff = BaseStaff.objects.select_related('system_user').get(system_user=user)
            except BaseStaff.DoesNotExist:
                self.logger.warning(f'User {user.username} (id: {system_user_id}) does not have a staff profile')
                return None
            # Check if user is superuser
            if user.is_superuser:
                staff_type = 'superuser'
                specific_data = {
                    'is_superuser': True,
                    'permissions': 'full_access',
                    'role': 'System Administrator'
                }
                self.logger.info(f'Retrieved superuser detail for system_user_id: {system_user_id}')
            else:
                # Determine staff type and get specific data
                staff_type: str | None = None
                specific_data: dict | None = None
                # Check Healthcare
                if hasattr(base_staff, 'healthcare_profile'):
                    staff_type = 'healthcare'
                    healthcare: Healthcare = base_staff.healthcare_profile
                    specific_data = {
                        'professional_registration': healthcare.professional_registration,
                        'professional_position': healthcare.professional_position,
                        'signature_url': base_staff.signature.url if base_staff.signature else None
                    }
                # Check Driver
                elif hasattr(base_staff, 'driver_profile'):
                    staff_type = 'driver'
                    driver: Driver = base_staff.driver_profile
                    specific_data = {
                        'license_number': driver.license_number,
                        'license_category': driver.license_category,
                        'license_issue_date': driver.license_issue_date.isoformat() if driver.license_issue_date else None,
                        'license_expiry_date': driver.license_expiry_date.isoformat() if driver.license_expiry_date else None,
                        'blood_type': getattr(driver, 'blood_type', None),
                        'signature_url': base_staff.signature.url if base_staff.signature else None
                    }
                # Check Administrative
                elif hasattr(base_staff, 'administrative_profile'):
                    staff_type = 'administrative'
                    administrative: Administrative = base_staff.administrative_profile
                    specific_data = {
                        'department': administrative.department,
                        'role': administrative.role,
                        'access_level': administrative.access_level,
                        'signature_url': base_staff.signature.url if base_staff.signature else None
                    }
            # Build full name
            full_name: str = user.get_full_name() or user.username
            # Get signature URL
            signature_url: str | None = base_staff.signature.url if base_staff.signature else None
            # Build response
            user_detail: UserDetailResponse = UserDetailResponse(
                # System User data
                system_user_id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=full_name,
                is_active=user.is_active,
                is_staff=user.is_staff,
                date_joined=user.date_joined.isoformat(),
                # Base Staff data
                base_staff_id=base_staff.id,
                document_type=base_staff.document_type,
                document_number=base_staff.document_number,
                type_personnel=base_staff.type_personnel,
                phone_number=base_staff.phone_number,
                address=base_staff.address,
                birth_date=base_staff.birth_date.isoformat() if base_staff.birth_date else None,
                signature_url=signature_url,
                created_at=base_staff.created_at.isoformat(),
                updated_at=base_staff.updated_at.isoformat(),
                # Specific profile data
                staff_type=staff_type or 'unknown',
                specific_data=specific_data
            )
            self.logger.info(f'Retrieved user detail for system_user_id: {system_user_id}, staff_type: {staff_type}')
            return user_detail
        except User.DoesNotExist:
            self.logger.warning(f'User not found with system_user_id: {system_user_id}')
            return None
        except Exception as e:
            self.logger.error(f'Error retrieving user detail: {str(e)}', exc_info=True)
            raise

    def change_user_active_status(
        self, 
        system_user_id: int,
        new_status: bool
    ) -> tuple[bool, str, User | None]:
        '''
        Change the active status of a user.
        
        Args:
            system_user_id: ID of the system_user (User model)
            new_status: New active status (True/False)
            
        Returns:
            Tuple of (success, message, user_object)
        '''
        try:
            user: User = User.objects.get(id=system_user_id)
            # Check if user is superuser (cannot change status)
            if user.is_superuser:
                self.logger.warning(
                    f'Attempted to change status of superuser: {user.username} (system_user_id: {system_user_id})'
                )
                return (False, 'Cannot change status of superuser accounts.', None)
            # Check if status is already the same
            if user.is_active == new_status:
                status_text = 'active' if new_status else 'inactive'
                self.logger.info(f'User {user.username} is already {status_text}')
                return (False, f'User is already {status_text}.', user)
            # Update user status
            old_status: bool = user.is_active
            user.is_active = new_status
            user.save()
            status_text = 'activated' if new_status else 'deactivated'
            self.logger.info(
                f'User {user.username} (system_user_id: {system_user_id}) status changed from {old_status} to {new_status}'
            )
            return (True, f'User successfully {status_text}.', user)
        except User.DoesNotExist:
            self.logger.warning(f'User not found with id: {system_user_id}')
            return (False, 'User not found.', None)
        except Exception as e:
            self.logger.error(f'Error changing user status: {str(e)}', exc_info=True)
            raise