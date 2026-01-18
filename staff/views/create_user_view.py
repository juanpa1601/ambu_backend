from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from staff.application_service import CreateUserApplicationService
from staff.serializers.input import CreateUserSerializer
from staff.types.dataclass import CreateUserRequest
from typing import Any
from django.contrib.auth.models import User

class CreateUserView(BaseView):
    '''
    API endpoint to create a new user with staff profile.
    Requires authentication and administrative or superuser role.
    Supports creating Healthcare, Driver, or Administrative users.
    
    POST /api/staff/create-user/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Content-Type: application/json
    
    Request Body - Healthcare:
        {
            "username": "healthcare_user_2",
            "email": "healthcare2@ambu.com",
            "password": "SecurePass123!",
            "first_name": "Dr. Ana",
            "last_name": "Martinez",
            "document_type": "DNI",
            "document_number": "87654321",
            "type_personnel": "Healthcare",
            "phone_number": "+51987654322",
            "address": "Av. Salud 456, Lima",
            "birth_date": "1990-06-15",
            "professional_registration": "CMP-54321",
            "professional_position": "Emergency Doctor"
        }
    
    Request Body - Driver:
        {
            "username": "driver_user_2",
            "email": "driver2@ambu.com",
            "password": "SecurePass123!",
            "first_name": "Luis",
            "last_name": "Ramirez",
            "document_type": "DNI",
            "document_number": "11223355",
            "type_personnel": "Driver",
            "phone_number": "+51998877666",
            "address": "Av. Transport 789, Lima",
            "birth_date": "1992-09-20",
            "license_number": "L-2024-67890",
            "license_category": "A-IIb",
            "license_issue_date": "2021-03-15",
            "license_expiry_date": "2031-03-15",
            "blood_type": "A+"
        }
    
    Request Body - Administrative:
        {
            "username": "admin_user_2",
            "email": "admin2@ambu.com",
            "password": "SecurePass123!",
            "first_name": "Sofia",
            "last_name": "Torres",
            "document_type": "DNI",
            "document_number": "55667799",
            "type_personnel": "Administrative",
            "phone_number": "+51987123457",
            "address": "Av. Admin 123, Lima",
            "birth_date": "1989-04-10",
            "department": "Human Resources",
            "role": "HR Manager",
            "access_level": "Level 3"
        }
    
    Success Response (201 Created):
        {
            "response": "User created successfully.",
            "msg": 1,
            "data": {
                "system_user_id": 5,
                "username": "healthcare_user_2",
                "email": "healthcare2@ambu.com",
                "base_staff_id": 5,
                "staff_type": "healthcare",
                "created_at": "2026-01-18T10:30:00Z"
            }
        }
    
    Error Response (403 Forbidden):
        {
            "response": "You do not have permission to create users.",
            "msg": -1
        }
    
    Error Response (400 Bad Request - Username exists):
        {
            "response": "Username already exists.",
            "msg": -1
        }
    
    Error Response (400 Bad Request - Missing required field):
        {
            "response": "Invalid data provided.",
            "msg": -1,
            "errors": {
                "professional_registration": ["This field is required for Healthcare personnel."]
            }
        }
    '''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(
        self, 
        request: Request
    ) -> Response:
        '''
        Handle POST request to create a new user.
        Only administrative users and superusers can access this endpoint.
        
        Args:
            request: HTTP request with authentication token and user data
            
        Returns:
            Response with created user data or error message
        '''
        def service_callback(validated_data: dict[str, Any], user: User) -> dict[str, Any]:
            # Create request dataclass
            user_request = CreateUserRequest(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                document_type=validated_data['document_type'],
                document_number=validated_data['document_number'],
                type_personnel=validated_data['type_personnel'],
                phone_number=validated_data['phone_number'],
                address=validated_data['address'],
                birth_date=validated_data['birth_date'],
                signature=validated_data.get('signature'),
                professional_registration=validated_data.get('professional_registration'),
                professional_position=validated_data.get('professional_position'),
                license_number=validated_data.get('license_number'),
                license_category=validated_data.get('license_category'),
                license_issue_date=validated_data.get('license_issue_date'),
                license_expiry_date=validated_data.get('license_expiry_date'),
                blood_type=validated_data.get('blood_type'),
                department=validated_data.get('department'),
                role=validated_data.get('role'),
                access_level=validated_data.get('access_level')
            )
            # Call application service
            create_user_service: CreateUserApplicationService = CreateUserApplicationService()
            return create_user_service.create_user(
                user_request=user_request,
                requesting_user=user
            )
        
        return self._handle_request(
            request=request,
            serializer_class=CreateUserSerializer,
            service_method_callback=service_callback,
            requires_auth=True
        )