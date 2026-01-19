from typing import Any
import logging
from django.contrib.auth.models import User
from staff.domain_service.user_domain_service import UserDomainService
from staff.types.dataclass import (
    EditProfileRequest,
    EditProfileResponse
)

class EditProfileApplicationService:
    '''Application service for editing user's own profile.'''
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.user_domain_service: UserDomainService = UserDomainService()
    
    def edit_profile(
        self, 
        profile_request: EditProfileRequest,
        authenticated_user: User
    ) -> dict[str, Any]:
        '''
        Edit authenticated user's profile information.
        
        Args:
            profile_request: EditProfileRequest with fields to update
            authenticated_user: User authenticated via token
            
        Returns:
            dictionary with response data and status
        '''
        try:
            # Update profile through domain service
            success: bool
            message: str
            response_data: EditProfileResponse | None
            success, message, response_data = self.user_domain_service.update_user_profile(
                user=authenticated_user,
                profile_request=profile_request
            )
            if not success:
                # Check specific error types
                if 'ya existe' in message.lower():
                    return {
                        'response': message,
                        'msg': -1,
                        'status_code_http': 400
                    }
                
                if 'no encontrado' in message.lower():
                    return {
                        'response': message,
                        'msg': -1,
                        'status_code_http': 404
                    }
                # Other errors
                return {
                    'response': message,
                    'msg': -1,
                    'status_code_http': 500
                }
            # Build success response
            self.logger.info(
                f'User {authenticated_user.username} updated their profile. '
                f'Fields updated: {", ".join(response_data.fields_updated)}'
            )
            return {
                'response': message,
                'msg': 1,
                'status_code_http': 200,
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
                f'Error in edit profile application service: {str(e)}',
                exc_info=True
            )
            return {
                'response': 'Ocurrió un error al actualizar el perfil.',
                'msg': -1,
                'status_code_http': 500
            }