from typing import Any
import logging
from django.contrib.auth.models import User

from staff.domain_service import AuthDomainService
from staff.types.dataclass import ValidateSessionResponse

class ValidateSessionApplicationService:
    """
    Application service for validating user session.
    Checks if authentication token is still valid.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_domain_service: AuthDomainService = AuthDomainService()
    
    def validate_session(
        self, 
        authenticated_user: User
    ) -> ValidateSessionResponse:
        '''
        Validate if user's session (token) is still valid.
        
        Args:
            authenticated_user: User authenticated via token
            
        Returns:
            Dictionary with response data and status
        '''
        try:
            # Step 1: Validate session through domain service
            is_valid: bool
            message: str
            is_valid, message = self.auth_domain_service.validate_user_session(
                user=authenticated_user
            )
            if not is_valid:
                self.logger.warning(
                    f'Invalid session for user: {authenticated_user.username} - {message}'
                )
                return ValidateSessionResponse(
                    is_valid=False,
                    username=authenticated_user.username,
                    user_id=authenticated_user.id,
                    staff_type=None
                ).to_dict()
            # Step 2: Get staff type
            staff_type = self.auth_domain_service.get_staff_type(
                user=authenticated_user
            )
            # Step 3: Build success response
            self.logger.info(
                f'Valid session confirmed for user: {authenticated_user.username}'
            )
            return ValidateSessionResponse(
                is_valid=True,
                username=authenticated_user.username,
                user_id=authenticated_user.id,
                staff_type=staff_type
            ).to_dict() 
        except Exception as e:
            self.logger.error(
                f'Error validating session for user {authenticated_user.username}: {str(e)}',
                exc_info=True
            )
            return ValidateSessionResponse(
                is_valid=False,
                username=authenticated_user.username,
                user_id=authenticated_user.id,
                staff_type=None
            ).to_dict()