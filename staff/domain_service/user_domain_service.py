from django.db import transaction
from django.contrib.auth.models import User
from staff.models.base_staff import BaseStaff
from staff.models.healthcare import Healthcare
from staff.models.driver import Driver
from staff.models.administrative import Administrative
from staff.types.dataclass import (
    UserListItem, 
    UserDetailResponse,
    ProfileInformationResponse,
    CreateUserRequest,
    CreateUserResponse,
    EditProfileRequest,
    EditProfileResponse
) 
from datetime import datetime
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
                        'blood_type': getattr(driver, 'blood_type', None)
                    }
                # Check Administrative
                elif hasattr(base_staff, 'administrative_profile'):
                    staff_type = 'administrative'
                    administrative: Administrative = base_staff.administrative_profile
                    specific_data = {
                        'department': administrative.department,
                        'role': administrative.role,
                        'access_level': administrative.access_level
                    }
            # Build full name
            full_name: str = user.get_full_name() or user.username
            # Get signature URL
            signature_url: str | None = base_staff.signature if base_staff.signature else None
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
            tuple of (success, message, user_object)
        '''
        try:
            user: User = User.objects.get(id=system_user_id)
            # Check if user is superuser (cannot change status)
            if user.is_superuser:
                self.logger.warning(
                    f'Attempted to change status of superuser: {user.username} (system_user_id: {system_user_id})'
                )
                return (False, 'No se puede cambiar el estado de cuentas de superusuario.', None)
            # Check if status is already the same
            status_text: str
            if user.is_active == new_status:
                status_text = 'activo' if new_status else 'inactivo'
                self.logger.info(f'User {user.username} is already {status_text}')
                return (False, f'Usuario ya está {status_text}.', user)
            # Update user status
            old_status: bool = user.is_active
            user.is_active = new_status
            user.save()
            status_text = 'activo' if new_status else 'inactivo'
            self.logger.info(
                f'User {user.username} (system_user_id: {system_user_id}) status changed from {old_status} to {new_status}'
            )
            return (True, f'Usuario {status_text} exitosamente.', user)
        except User.DoesNotExist:
            self.logger.warning(f'User not found with id: {system_user_id}')
            return (False, 'Usuario no encontrado.', None)
        except Exception as e:
            self.logger.error(f'Error changing user status: {str(e)}', exc_info=True)
            raise

    def get_profile_information(
        self, 
        user: User
    ) -> ProfileInformationResponse | None:
        '''
        Retrieve profile information for the authenticated user.
        Excludes sensitive fields like password, last_login, is_staff, is_active, is_superuser.
        
        Args:
            user: Authenticated User object
            
        Returns:
            ProfileInformationResponse dataclass with user profile information or None
        '''
        try:
            # Check if user has a BaseStaff profile
            try:
                base_staff: BaseStaff = BaseStaff.objects.select_related('system_user').get(system_user=user)
            except BaseStaff.DoesNotExist:
                self.logger.warning(f'User {user.username} (id: {user.id}) does not have a staff profile')
                return None
            # Build full name
            full_name: str = user.get_full_name() or user.username
            # Get signature URL
            signature_url: str | None = base_staff.signature if base_staff.signature else None
            # Determine staff type and get specific data
            staff_type: str | None = None
            specific_data: dict | None = None
            # Check if user is superuser
            if user.is_superuser:
                staff_type = 'superuser'
                specific_data = {
                    'is_superuser': True,
                    'permissions': 'full_access',
                    'role': 'System Administrator'
                }
                self.logger.info(f'Retrieved superuser profile for user: {user.username}')
            # Check Healthcare
            elif hasattr(base_staff, 'healthcare_profile'):
                staff_type = 'healthcare'
                healthcare: Healthcare = base_staff.healthcare_profile
                specific_data = {
                    'professional_registration': healthcare.professional_registration,
                    'professional_position': healthcare.professional_position
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
                    'blood_type': getattr(driver, 'blood_type', None)
                }
            # Check Administrative
            elif hasattr(base_staff, 'administrative_profile'):
                staff_type = 'administrative'
                administrative: Administrative = base_staff.administrative_profile
                specific_data = {
                    'department': administrative.department,
                    'role': administrative.role,
                    'access_level': administrative.access_level
                }
            # Build response
            profile_info: ProfileInformationResponse = ProfileInformationResponse(
                # System User data (sin campos sensibles)
                system_user_id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=full_name,
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
            self.logger.info(f'Retrieved profile information for user: {user.username}, staff_type: {staff_type}')
            return profile_info
        except Exception as e:
            self.logger.error(f'Error retrieving profile information: {str(e)}', exc_info=True)
            raise

    @transaction.atomic
    def create_user_with_staff_profile(
        self, 
        user_request: CreateUserRequest
    ) -> tuple[bool, str, CreateUserResponse | None]:
        '''
        Create a new user with BaseStaff and specific staff profile.
        Uses database transaction to ensure data integrity.
        
        Args:
            user_request: CreateUserRequest dataclass with user data
            
        Returns:
            tuple of (success, message, CreateUserResponse or None)
        '''
        try:
            # Step 1: Validate username uniqueness
            if User.objects.filter(username=user_request.username).exists():
                self.logger.warning(f'Username already exists: {user_request.username}')
                return (False, 'Username ya existe. Intenta otro..', None)
            # Step 2: Validate email uniqueness
            if User.objects.filter(email=user_request.email).exists():
                self.logger.warning(f'Email already exists: {user_request.email}')
                return (False, 'El email ya existe. Intenta otro.', None)
            # Step 3: Validate document_number uniqueness
            if BaseStaff.objects.filter(document_number=user_request.document_number).exists():
                self.logger.warning(f'Document number already exists: {user_request.document_number}')
                return (False, 'Número de documento ya existe. Intenta otro.', None)
            # Step 4: Create System User
            user: User = User.objects.create_user(
                username=user_request.username,
                email=user_request.email,
                password=user_request.password,
                first_name=user_request.first_name,
                last_name=user_request.last_name,
                is_active=True,
                is_staff=False
            )
            self.logger.info(f'Created system user: {user.username} (id: {user.id})')
            # Step 5: Create Base Staff
            base_staff: BaseStaff = BaseStaff.objects.create(
                system_user=user,
                document_type=user_request.document_type,
                document_number=user_request.document_number,
                type_personnel=user_request.type_personnel,
                phone_number=user_request.phone_number,
                address=user_request.address,
                birth_date=user_request.birth_date,
                signature=user_request.signature
                # signature will be handled separately if needed
            )
            self.logger.info(f'Created base staff profile: {base_staff.id} for user: {user.username}')
            # Step 6: Create specific staff profile based on type_personnel
            staff_type: str = user_request.type_personnel.lower()
            if user_request.type_personnel == 'Healthcare':
                healthcare: Healthcare = Healthcare.objects.create(
                    base_staff=base_staff,
                    professional_registration=user_request.professional_registration,
                    professional_position=user_request.professional_position
                )
                self.logger.info(f'Created healthcare profile for user: {user.username}')
            elif user_request.type_personnel == 'Driver':
                driver: Driver = Driver.objects.create(
                    base_staff=base_staff,
                    license_number=user_request.license_number,
                    license_category=user_request.license_category,
                    license_issue_date=user_request.license_issue_date,
                    license_expiry_date=user_request.license_expiry_date,
                    blood_type=user_request.blood_type
                )
                self.logger.info(f'Created driver profile for user: {user.username}')
            elif user_request.type_personnel == 'Administrative':
                administrative: Administrative = Administrative.objects.create(
                    base_staff=base_staff,
                    department=user_request.department,
                    role=user_request.role,
                    access_level=user_request.access_level
                )
                self.logger.info(f'Created administrative profile for user: {user.username}')
            # Step 7: Build response
            response: CreateUserResponse = CreateUserResponse(
                system_user_id=user.id,
                username=user.username,
                email=user.email,
                base_staff_id=base_staff.id,
                staff_type=staff_type,
                created_at=user.date_joined.isoformat()
            )
            self.logger.info(
                f'Successfully created complete user profile: {user.username}, '
                f'type: {user_request.type_personnel}'
            )
            return (True, 'Usuario creado correctamente.', response)
        except Exception as e:
            self.logger.error(f'Error creating user: {str(e)}', exc_info=True)
            # Transaction will be rolled back automatically
            return (False, f'Ocurrió un error al crear el usuario: {str(e)}', None)
        
    @transaction.atomic
    def update_user_profile(
        self, 
        user: User,
        profile_request: EditProfileRequest
    ) -> tuple[bool, str, EditProfileResponse | None]:
        '''
        Update user's own profile information.
        Uses database transaction to ensure data integrity.
        
        Args:
            user: Authenticated User object
            profile_request: EditProfileRequest dataclass with fields to update
            
        Returns:
            tuple of (success, message, EditProfileResponse or None)
        '''
        try:
            fields_updated: list[str] = []
            # Step 1: Get BaseStaff profile
            try:
                base_staff: BaseStaff = BaseStaff.objects.select_related('system_user').get(system_user=user)
            except BaseStaff.DoesNotExist:
                self.logger.warning(f'User {user.username} does not have a staff profile')
                return (False, 'Perfil de usuario no encontrado.', None)
            # Step 2: Determine staff type
            staff_type: str | None = None
            if hasattr(base_staff, 'healthcare_profile'):
                staff_type = 'healthcare'
                specific_profile = base_staff.healthcare_profile
            elif hasattr(base_staff, 'driver_profile'):
                staff_type = 'driver'
                specific_profile = base_staff.driver_profile
            elif hasattr(base_staff, 'administrative_profile'):
                staff_type = 'administrative'
                specific_profile = base_staff.administrative_profile
            else:
                self.logger.warning(f'User {user.username} has no specific profile type')
                return (False, 'El usuario no tiene un tipo de perfil específico.', None)
            # Step 3: Update System User fields
            if profile_request.email is not None:
                # Validate email uniqueness (exclude current user)
                if User.objects.filter(email=profile_request.email).exclude(id=user.id).exists():
                    self.logger.warning(f'Email already exists: {profile_request.email}')
                    return (False, 'El email ya existe. Intenta otro.', None)
                user.email = profile_request.email
                fields_updated.append('email')
            if profile_request.first_name is not None:
                user.first_name = profile_request.first_name
                fields_updated.append('first_name')
            if profile_request.last_name is not None:
                user.last_name = profile_request.last_name
                fields_updated.append('last_name')
            if profile_request.password is not None:
                user.set_password(profile_request.password)
                fields_updated.append('password')
            # Save user if any field was updated
            if any(field in fields_updated for field in ['email', 'first_name', 'last_name', 'password']):
                user.save()
                self.logger.info(f'Updated system user fields for: {user.username}')
            # Step 4: Update Base Staff fields
            if profile_request.phone_number is not None:
                base_staff.phone_number = profile_request.phone_number
                fields_updated.append('phone_number')
            if profile_request.address is not None:
                base_staff.address = profile_request.address
                fields_updated.append('address')
            if profile_request.birth_date is not None:
                base_staff.birth_date = profile_request.birth_date
                fields_updated.append('birth_date')
            if profile_request.signature is not None:
                base_staff.signature = profile_request.signature
                fields_updated.append('signature')
            # Save base_staff if any field was updated
            if any(field in fields_updated for field in ['phone_number', 'address', 'birth_date', 'signature']):
                base_staff.save()
                self.logger.info(f'Updated base staff fields for: {user.username}')
            # Step 5: Update specific profile fields based on staff type
            if staff_type == 'healthcare':
                if profile_request.professional_registration is not None:
                    specific_profile.professional_registration = profile_request.professional_registration
                    fields_updated.append('professional_registration')
                if profile_request.professional_position is not None:
                    specific_profile.professional_position = profile_request.professional_position
                    fields_updated.append('professional_position')
                if any(field in fields_updated for field in ['professional_registration', 'professional_position']):
                    specific_profile.save()
                    self.logger.info(f'Updated healthcare profile for: {user.username}')
            elif staff_type == 'driver':
                if profile_request.license_number is not None:
                    specific_profile.license_number = profile_request.license_number
                    fields_updated.append('license_number')
                if profile_request.license_category is not None:
                    specific_profile.license_category = profile_request.license_category
                    fields_updated.append('license_category')
                if profile_request.license_issue_date is not None:
                    specific_profile.license_issue_date = profile_request.license_issue_date
                    fields_updated.append('license_issue_date')
                if profile_request.license_expiry_date is not None:
                    specific_profile.license_expiry_date = profile_request.license_expiry_date
                    fields_updated.append('license_expiry_date')
                if profile_request.blood_type is not None:
                    specific_profile.blood_type = profile_request.blood_type
                    fields_updated.append('blood_type')
                if any(field in fields_updated for field in ['license_number', 'license_category', 'license_issue_date', 'license_expiry_date', 'blood_type']):
                    specific_profile.save()
                    self.logger.info(f'Updated driver profile for: {user.username}')
            elif staff_type == 'administrative':
                if profile_request.department is not None:
                    specific_profile.department = profile_request.department
                    fields_updated.append('department')
                if profile_request.role is not None:
                    specific_profile.role = profile_request.role
                    fields_updated.append('role')
                if profile_request.access_level is not None:
                    specific_profile.access_level = profile_request.access_level
                    fields_updated.append('access_level')
                if any(field in fields_updated for field in ['department', 'role', 'access_level']):
                    specific_profile.save()
                    self.logger.info(f'Updated administrative profile for: {user.username}')
            # Step 6: Build response
            response: EditProfileResponse = EditProfileResponse(
                system_user_id=user.id,
                username=user.username,
                email=user.email,
                base_staff_id=base_staff.id,
                staff_type=staff_type,
                updated_at=datetime.now().isoformat(),
                fields_updated=fields_updated
            )
            self.logger.info(
                f'Successfully updated profile for user: {user.username}, '
                f'fields: {", ".join(fields_updated)}'
            )
            return (True, 'Perfil de usuario actualizado correctamente.', response)
        except Exception as e:
            self.logger.error(f'Error updating user profile: {str(e)}', exc_info=True)
            # Transaction will be rolled back automatically
            return (False, f'Ocurrió un error al actualizar el perfil de usuario: {str(e)}', None)
        
    @transaction.atomic
    def update_user_profile_by_admin(
        self, 
        system_user_id: int,
        profile_request: EditProfileRequest,
        admin_user: User
    ) -> tuple[bool, str, EditProfileResponse | None]:
        '''
        Update any user's profile information by an administrator.
        Similar to update_user_profile but for admin users editing others.
        Uses database transaction to ensure data integrity.
        
        Args:
            system_user_id: ID of the user to update
            profile_request: EditProfileRequest dataclass with fields to update
            admin_user: Administrator user performing the update
            
        Returns:
            tuple of (success, message, EditProfileResponse or None)
        '''
        try:
            fields_updated: list[str] = []
            # Step 1: Get target user
            try:
                user: User = User.objects.get(id=system_user_id)
            except User.DoesNotExist:
                self.logger.warning(f'User with id {system_user_id} not found')
                return (False, 'Usuario no encontrado.', None)
            # Step 2: Get BaseStaff profile
            try:
                base_staff: BaseStaff = BaseStaff.objects.select_related('system_user').get(system_user=user)
            except BaseStaff.DoesNotExist:
                self.logger.warning(f'User {user.username} does not have a staff profile')
                return (False, 'Perfil de usuario no encontrado.', None)
            # Step 3: Determine staff type
            staff_type: str | None = None
            if hasattr(base_staff, 'healthcare_profile'):
                staff_type = 'healthcare'
                specific_profile = base_staff.healthcare_profile
            elif hasattr(base_staff, 'driver_profile'):
                staff_type = 'driver'
                specific_profile = base_staff.driver_profile
            elif hasattr(base_staff, 'administrative_profile'):
                staff_type = 'administrative'
                specific_profile = base_staff.administrative_profile
            else:
                self.logger.warning(f'User {user.username} has no specific profile type')
                return (False, 'El usuario no tiene un tipo de perfil específico.', None)
            # Step 4: Update System User fields
            if profile_request.email is not None:
                # Validate email uniqueness (exclude current user)
                if User.objects.filter(email=profile_request.email).exclude(id=user.id).exists():
                    self.logger.warning(f'Email already exists: {profile_request.email}')
                    return (False, 'El email ya existe. Intenta otro.', None)
                user.email = profile_request.email
                fields_updated.append('email')
            if profile_request.first_name is not None:
                user.first_name = profile_request.first_name
                fields_updated.append('first_name')
            if profile_request.last_name is not None:
                user.last_name = profile_request.last_name
                fields_updated.append('last_name')
            if profile_request.password is not None:
                user.set_password(profile_request.password)
                fields_updated.append('password')
            # Save user if any field was updated
            if any(field in fields_updated for field in ['email', 'first_name', 'last_name', 'password']):
                user.save()
                self.logger.info(f'Admin {admin_user.username} updated system user fields for: {user.username}')
            # Step 5: Update Base Staff fields
            if profile_request.phone_number is not None:
                base_staff.phone_number = profile_request.phone_number
                fields_updated.append('phone_number')
            if profile_request.address is not None:
                base_staff.address = profile_request.address
                fields_updated.append('address')
            if profile_request.birth_date is not None:
                base_staff.birth_date = profile_request.birth_date
                fields_updated.append('birth_date')
            if profile_request.signature is not None:
                base_staff.signature = profile_request.signature
                fields_updated.append('signature')
            # Save base_staff if any field was updated
            if any(field in fields_updated for field in ['phone_number', 'address', 'birth_date', 'signature']):
                base_staff.save()
                self.logger.info(f'Admin {admin_user.username} updated base staff fields for: {user.username}')
            # Step 6: Update specific profile fields based on staff type
            if staff_type == 'healthcare':
                if profile_request.professional_registration is not None:
                    specific_profile.professional_registration = profile_request.professional_registration
                    fields_updated.append('professional_registration')
                if profile_request.professional_position is not None:
                    specific_profile.professional_position = profile_request.professional_position
                    fields_updated.append('professional_position')
                if any(field in fields_updated for field in ['professional_registration', 'professional_position']):
                    specific_profile.save()
                    self.logger.info(f'Admin {admin_user.username} updated healthcare profile for: {user.username}')
            elif staff_type == 'driver':
                if profile_request.license_number is not None:
                    specific_profile.license_number = profile_request.license_number
                    fields_updated.append('license_number')
                if profile_request.license_category is not None:
                    specific_profile.license_category = profile_request.license_category
                    fields_updated.append('license_category')
                if profile_request.license_issue_date is not None:
                    specific_profile.license_issue_date = profile_request.license_issue_date
                    fields_updated.append('license_issue_date')
                if profile_request.license_expiry_date is not None:
                    specific_profile.license_expiry_date = profile_request.license_expiry_date
                    fields_updated.append('license_expiry_date')
                if profile_request.blood_type is not None:
                    specific_profile.blood_type = profile_request.blood_type
                    fields_updated.append('blood_type')
                if any(field in fields_updated for field in ['license_number', 'license_category', 'license_issue_date', 'license_expiry_date', 'blood_type']):
                    specific_profile.save()
                    self.logger.info(f'Admin {admin_user.username} updated driver profile for: {user.username}')
            elif staff_type == 'administrative':
                if profile_request.department is not None:
                    specific_profile.department = profile_request.department
                    fields_updated.append('department')
                if profile_request.role is not None:
                    specific_profile.role = profile_request.role
                    fields_updated.append('role')
                if profile_request.access_level is not None:
                    specific_profile.access_level = profile_request.access_level
                    fields_updated.append('access_level')
                if any(field in fields_updated for field in ['department', 'role', 'access_level']):
                    specific_profile.save()
                    self.logger.info(f'Admin {admin_user.username} updated administrative profile for: {user.username}')
            # Step 7: Build response
            response: EditProfileResponse = EditProfileResponse(
                system_user_id=user.id,
                username=user.username,
                email=user.email,
                base_staff_id=base_staff.id,
                staff_type=staff_type,
                updated_at=datetime.now().isoformat(),
                fields_updated=fields_updated
            )
            self.logger.info(
                f'Admin {admin_user.username} successfully updated user: {user.username}, '
                f'fields: {", ".join(fields_updated)}'
            )
            return (True, 'Perfil de usuario actualizado correctamente.', response)
        except Exception as e:
            self.logger.error(f'Error updating user profile by admin: {str(e)}', exc_info=True)
            # Transaction will be rolled back automatically
            return (False, f'Ocurrió un error al actualizar el perfil de usuario: {str(e)}', None)
        