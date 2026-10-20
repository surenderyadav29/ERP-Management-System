"""
User Model
Represents a user entity for authentication
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """User data model for authentication"""
    user_id: Optional[int] = None
    username: str = ""
    password: str = ""
    role: str = "admin"
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create User from dictionary"""
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username', ''),
            password=data.get('password', ''),
            role=data.get('role', 'admin'),
            created_at=data.get('created_at')
        )
    
    def __str__(self):
        return f"User(ID={self.user_id}, Username={self.username}, Role={self.role})"