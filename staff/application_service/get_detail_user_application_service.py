from typing import Any
import logging
from django.contrib.auth.models import User
from ..domain_service import (
    UserDomainService, 
    AuthDomainService
)
from ..types.dataclass import UserDetailResponse
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class GetDetailUserApplicationService:
    '''Application service for retrieving user details.'''

    SUCCESS: int = 1
    FAILURE: int = -1  

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.user_domain_service: UserDomainService = UserDomainService()
        self.auth_domain_service: AuthDomainService = AuthDomainService()

    def get_user_detail(
        self, 
        system_user_id: int,
        requesting_user: User
    ) -> dict[str, Any]:
        '''
        Get detailed user information by system_user_id.
        
        Args:
            system_user_id: ID of the SystemUser record to retrieve
            requesting_user: User making the request (for logging)
            
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
            # Step 2: Get user detail from domain service
            user_detail: UserDetailResponse | None = self.user_domain_service.get_user_detail_by_system_user_id(system_user_id)
            if not user_detail:
                self.logger.warning(
                    f'User {requesting_user.username} requested non-existent system_user_id: {system_user_id}'
                )
                return {
                    'response': 'Usuario no encontrado.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_404_NOT_FOUND
                }
            # Step 3: Build response data
            response_data: dict[str, Any] = {
                'system_user': {
                    'id': user_detail.system_user_id,
                    'username': user_detail.username,
                    'email': user_detail.email,
                    'first_name': user_detail.first_name,
                    'last_name': user_detail.last_name,
                    'full_name': user_detail.full_name,
                    'is_active': user_detail.is_active,
                    'is_staff': user_detail.is_staff,
                    'date_joined': user_detail.date_joined,
                },
                'base_staff': {
                    'id': user_detail.base_staff_id,
                    'document_type': user_detail.document_type,
                    'document_number': user_detail.document_number,
                    'type_personnel': user_detail.type_personnel,
                    'phone_number': user_detail.phone_number,
                    'address': user_detail.address,
                    'birth_date': user_detail.birth_date,
                    'created_at': user_detail.created_at,
                    'updated_at': user_detail.updated_at,
                },
                'staff_type': user_detail.staff_type,
                'specific_profile': user_detail.specific_data
            }
            self.logger.info(
                f'User {requesting_user.username} retrieved detail for system_user_id: {system_user_id}'
            )
            return {
                'response': 'Detalle del usuario recuperado exitosamente.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'data': response_data
            }
        except Exception as e:
            self.logger.error(
                f'Error getting user detail for system_user_id {system_user_id}: {str(e)}',
                exc_info=True
            )
            return {
                'response': 'Ocurrió un error al recuperar el detalle del usuario.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }