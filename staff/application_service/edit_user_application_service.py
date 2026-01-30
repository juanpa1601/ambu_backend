from typing import Any
import logging
from django.contrib.auth.models import User
from staff.domain_service import (
    UserDomainService, 
    AuthDomainService
)
from staff.types.dataclass import (
    EditProfileResponse, 
    EditProfileRequest
)
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class EditUserApplicationService:
    '''
    Application service for administrative users to edit other user profiles.
    Requires administrative or superuser privileges.
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1  

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_domain_service: AuthDomainService = AuthDomainService()
        self.user_domain_service: UserDomainService = UserDomainService()
    
    def edit_user(
        self, 
        system_user_id: int,
        profile_request: EditProfileRequest,
        requesting_user: User
    ) -> dict[str, Any]:
        '''
        Edit user profile by administrative user.
        Only administrative users and superusers can perform this action.
        
        Args:
            system_user_id: ID of the user to update
            profile_request: EditProfileRequest with fields to update
            requesting_user: User making the request (must be admin or superuser)
            
        Returns:
            dictionary with response data and status
        '''
        try:
            # Step 1: Verify requesting user is administrative or superuser
            is_admin: bool = self.auth_domain_service.is_administrative_user(requesting_user)
            is_superuser: bool = requesting_user.is_superuser
            if not (is_admin or is_superuser):
                self.logger.warning(
                    f'User {requesting_user.username} attempted to edit user without permission'
                )
                return {
                    'response': 'No tienes permiso para editar usuarios.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_403_FORBIDDEN
                }
            # Step 2: Prevent editing their own profile (use edit_profile instead)
            if requesting_user.id == system_user_id:
                self.logger.warning(
                    f'Admin {requesting_user.username} attempted to edit their own profile via edit_user endpoint'
                )
                return {
                    'response': 'Usa la sección de editar perfil, para editar tu propio perfil.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_400_BAD_REQUEST
                }
            # Step 3: Update user profile through domain service
            success: bool
            message: str
            response_data: EditProfileResponse | None
            success, message, response_data = self.user_domain_service.update_user_profile_by_admin(
                system_user_id=system_user_id,
                profile_request=profile_request,
                admin_user=requesting_user
            )
            if not success:
                # Check specific error types
                if 'ya existe' in message.lower():
                    return {
                        'response': message,
                        'msg': self.FAILURE,
                        'status_code_http': HTTP_400_BAD_REQUEST
                    }
                if 'no encontrado' in message.lower():
                    return {
                        'response': message,
                        'msg': self.FAILURE,
                        'status_code_http': HTTP_404_NOT_FOUND
                    }
                # Other errors
                return {
                    'response': message,
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
                }
            # Step 4: Build success response
            self.logger.info(
                f'Admin {requesting_user.username} updated user {response_data.username}. '
                f'Fields updated: {", ".join(response_data.fields_updated)}'
            )
            return {
                'response': message,
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'data': {
                    'system_user_id': response_data.system_user_id,
                    'username': response_data.username,
                    'email': response_data.email,
                    'base_staff_id': response_data.base_staff_id,
                    'staff_type': response_data.staff_type,
                    'updated_at': response_data.updated_at,
                    'fields_updated': response_data.fields_updated
                }
            }
        except Exception as e:
            self.logger.error(
                f'Error in edit user application service: {str(e)}',
                exc_info=True
            )
            return {
                'response': 'Ocurrió un error al actualizar el usuario.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }