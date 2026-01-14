from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import logging

class AuthDomainService:
    '''
    Domain service responsible for core authentication business logic.
    Handles user authentication and token generation.
    '''
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def authenticate_user(
        self, 
        username: str,
        password: str
    ) -> User | None:
        '''
        Authenticate user with provided credentials.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            User object if authentication successful, None otherwise
        '''
        user: User | None = authenticate(username=username, password=password)
        if user is None:
            self.logger.warning(f'Failed login attempt for username: {username}')
            return None
        if not user.is_active:
            self.logger.warning(f'Inactive user login attempt: {username}')
            return None
        self.logger.info(f'Successful authentication for user: {username}')
        return user
    
    def generate_token(
        self, 
        user: User
    ) -> str:
        '''
        Generate or retrieve Django auth token for user.
        
        Args:
            user: Authenticated user object
            
        Returns:
            Token string
        '''
        token, created = Token.objects.get_or_create(user=user)
        if created:
            self.logger.info(f'New token created for user: {user.username}')
        return token.key
    
    def get_staff_type(
        self, 
        user: User
    ) -> str | None:
        '''
        Determine the staff type for the authenticated user.
        
        Args:
            user: Authenticated user object
            
        Returns:
            Staff type string ('healthcare', 'driver', 'administrative') or None
        '''
        try:
            if hasattr(user, 'staff_profile'):
                base_staff = user.staff_profile
                if hasattr(base_staff, 'healthcare_profile'):
                    return 'healthcare'
                elif hasattr(base_staff, 'driver_profile'):
                    return 'driver'
                elif hasattr(base_staff, 'administrative_profile'):
                    return 'administrative'
        except Exception as e:
            self.logger.error(f'Error determining staff type: {str(e)}')
        return None

    def revoke_token(
        self, 
        user: User
    ) -> bool:
        '''
        Revoke (delete) authentication token for user.
        
        Args:
            user: User object whose token should be revoked
            
        Returns:
            True if token was deleted, False if no token existed
        '''
        try:
            token: Token = Token.objects.get(user=user)
            token.delete()
            self.logger.info(f'Token revoked for user: {user.username}')
            return True
        except Token.DoesNotExist:
            self.logger.warning(f'No token found for user: {user.username}')
            return False
        except Exception as e:
            self.logger.error(f'Error revoking token for user {user.username}: {str(e)}')
            raise
    
    def verify_user_has_token(
        self, 
        user: User
    ) -> bool:
        '''
        Check if user has an active token.
        
        Args:
            user: User object to check
            
        Returns:
            True if user has a token, False otherwise
        '''
        try:
            return Token.objects.filter(user=user).exists()
        except Exception as e:
            self.logger.error(f'Error checking token for user {user.username}: {str(e)}')
            return False    