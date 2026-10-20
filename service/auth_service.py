"""
Authentication Service
Business logic layer for User authentication
"""

from typing import Optional, Tuple
from dao.user_dao import UserDAO
from model.user import User


class AuthService:
    """Service class for authentication business logic"""
    
    def __init__(self):
        self.user_dao = UserDAO()
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """Authenticate user login"""
        if not username or not password:
            return False, "Username and password are required!", None
        
        user = self.user_dao.authenticate(username, password)
        if user:
            return True, "Login successful!", user
        return False, "Invalid username or password!", None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        if not old_password or not new_password:
            return False, "All fields are required!"
        
        user = self.user_dao.find_by_id(user_id)
        if not user:
            return False, "User not found!"
        
        if user.password != old_password:
            return False, "Current password is incorrect!"
        
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters!"
        
        if self.user_dao.update_password(user_id, new_password):
            return True, "Password changed successfully!"
        return False, "Failed to change password!"
    
    def create_user(self, username: str, password: str, role: str = 'admin') -> Tuple[bool, str]:
        """Create a new user"""
        if not username or not password:
            return False, "Username and password are required!"
        
        if len(username) < 4:
            return False, "Username must be at least 4 characters!"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters!"
        
        # Check if username already exists
        existing = self.user_dao.find_by_username(username)
        if existing:
            return False, "Username already exists!"
        
        user = User(username=username, password=password, role=role)
        user_id = self.user_dao.insert(user)
        
        if user_id:
            return True, f"User created successfully! ID: {user_id}"
        return False, "Failed to create user!"