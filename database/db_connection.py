"""
Database Connection Module
Handles MySQL database connection for the ERP System
"""

import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """Singleton class for database connection management"""
    
    _instance = None
    _connection = None
    
    # Database configuration - CHANGE PASSWORD HERE
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Surender@1234',  # Change this to your MySQL password
        'database': 'erp_system_db',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci',
        'autocommit': True
    }
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """Get database connection"""
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(**self.DB_CONFIG)
                print("✓ Database connection established successfully!")
            return self._connection
        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            return None
    
    def close_connection(self):
        """Close database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("✓ Database connection closed.")
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and optionally fetch results"""
        connection = self.get_connection()
        if connection is None:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.lastrowid
        except Error as e:
            print(f"✗ Query execution error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def execute_many(self, query, params_list):
        """Execute multiple queries"""
        connection = self.get_connection()
        if connection is None:
            return None
        
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.executemany(query, params_list)
            connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"✗ Batch execution error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()


# Global database instance
db = DatabaseConnection()


def get_db():
    """Get database instance"""
    return db