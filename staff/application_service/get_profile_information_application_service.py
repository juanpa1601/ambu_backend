from typing import Any
import logging
from django.contrib.auth.models import User
from ..types.dataclass import ProfileInformationResponse
from staff.domain_service.user_domain_service import UserDomainService

class GetProfileInformationApplicationService:
    '''Application service for retrieving authenticated user's profile information.'''
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.user_domain_service: UserDomainService = UserDomainService()
    
    def get_profile_information(
        self, 
        authenticated_user: User
    ) -> dict[str, Any]:
        '''
        Get profile information for the authenticated user.
        Excludes sensitive fields.
        
        Args:
            authenticated_user: User authenticated via token
            
        Returns:
            Dictionary with response data and status
        '''
        try:
            # Step 1: Get profile information from domain service
            profile_info: ProfileInformationResponse | None = self.user_domain_service.get_profile_information(authenticated_user)
            if not profile_info:
                self.logger.warning(
                    f'User {authenticated_user.username} does not have a staff profile'
                )
                return {
                    'response': 'User profile not found.',
                    'msg': -1,
                    'status_code_http': 404
                }
            # Step 2: Build response data
            response_data: dict[str, Any] = {
                'system_user': {
                    'id': profile_info.system_user_id,
                    'username': profile_info.username,
                    'email': profile_info.email,
                    'first_name': profile_info.first_name,
                    'last_name': profile_info.last_name,
                    'full_name': profile_info.full_name,
                    'date_joined': profile_info.date_joined,
                },
                'base_staff': {
                    'id': profile_info.base_staff_id,
                    'document_type': profile_info.document_type,
                    'document_number': profile_info.document_number,
                    'type_personnel': profile_info.type_personnel,
                    'phone_number': profile_info.phone_number,
                    'address': profile_info.address,
                    'birth_date': profile_info.birth_date,
                    'signature_url': profile_info.signature_url,
                    'created_at': profile_info.created_at,
                    'updated_at': profile_info.updated_at,
                },
                'staff_type': profile_info.staff_type,
                'specific_profile': profile_info.specific_data
            }
            self.logger.info(
                f'User {authenticated_user.username} retrieved their profile information'
            )
            return {
                'response': 'Profile information retrieved successfully.',
                'msg': 1,
                'status_code_http': 200,
                'data': response_data
            }
        except Exception as e:
            self.logger.error(
                f'Error getting profile information for user {authenticated_user.username}: {str(e)}',
                exc_info=True
            )
            return {
                'response': 'An error occurred while retrieving profile information.',
                'msg': -1,
                'status_code_http': 500
            }