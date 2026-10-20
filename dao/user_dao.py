"""
User DAO
Data Access Object for User entity (Authentication)
"""

from typing import Optional
from database.db_connection import get_db
from model.user import User


class UserDAO:
    """Data Access Object for User operations"""
    
    def __init__(self):
        self.db = get_db()
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user by username and password"""
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        results = self.db.execute_query(query, (username, password), fetch=True)
        if results and len(results) > 0:
            return User.from_dict(results[0])
        return None
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by ID"""
        query = "SELECT * FROM users WHERE user_id = %s"
        results = self.db.execute_query(query, (user_id,), fetch=True)
        if results and len(results) > 0:
            return User.from_dict(results[0])
        return None
    
    def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        results = self.db.execute_query(query, (username,), fetch=True)
        if results and len(results) > 0:
            return User.from_dict(results[0])
        return None
    
    def insert(self, user: User) -> Optional[int]:
        """Insert a new user into the database"""
        query = """
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
        """
        params = (user.username, user.password, user.role)
        return self.db.execute_query(query, params)
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Update user password"""
        query = "UPDATE users SET password = %s WHERE user_id = %s"
        result = self.db.execute_query(query, (new_password, user_id))
        return result is not None