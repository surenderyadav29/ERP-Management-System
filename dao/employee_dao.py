"""
Employee DAO
Data Access Object for Employee entity
"""

from typing import List, Optional
from database.db_connection import get_db
from model.employee import Employee


class EmployeeDAO:
    """Data Access Object for Employee operations"""
    
    def __init__(self):
        self.db = get_db()
    
    def insert(self, employee: Employee) -> Optional[int]:
        """Insert a new employee into the database"""
        query = """
            INSERT INTO employees (name, department, phone, email)
            VALUES (%s, %s, %s, %s)
        """
        params = (employee.name, employee.department, employee.phone, employee.email)
        return self.db.execute_query(query, params)
    
    def find_by_id(self, employee_id: int) -> Optional[Employee]:
        """Find an employee by ID"""
        query = "SELECT * FROM employees WHERE employee_id = %s"
        results = self.db.execute_query(query, (employee_id,), fetch=True)
        if results and len(results) > 0:
            return Employee.from_dict(results[0])
        return None
    
    def find_all(self) -> List[Employee]:
        """Get all employees"""
        query = "SELECT * FROM employees ORDER BY employee_id DESC"
        results = self.db.execute_query(query, fetch=True)
        return [Employee.from_dict(row) for row in results] if results else []
    
    def update(self, employee: Employee) -> bool:
        """Update an existing employee"""
        query = """
            UPDATE employees 
            SET name = %s, department = %s, phone = %s, email = %s
            WHERE employee_id = %s
        """
        params = (
            employee.name, 
            employee.department, 
            employee.phone, 
            employee.email, 
            employee.employee_id
        )
        result = self.db.execute_query(query, params)
        return result is not None
    
    def delete(self, employee_id: int) -> bool:
        """Delete an employee by ID"""
        query = "DELETE FROM employees WHERE employee_id = %s"
        result = self.db.execute_query(query, (employee_id,))
        return result is not None
    
    def search(self, keyword: str) -> List[Employee]:
        """Search employees by name, email, department, or phone"""
        query = """
            SELECT * FROM employees 
            WHERE name LIKE %s OR email LIKE %s OR department LIKE %s OR phone LIKE %s
            ORDER BY employee_id DESC
        """
        search_term = f"%{keyword}%"
        results = self.db.execute_query(
            query, (search_term, search_term, search_term, search_term), fetch=True
        )
        return [Employee.from_dict(row) for row in results] if results else []
    
    def get_departments(self) -> List[str]:
        """Get list of unique departments"""
        query = "SELECT DISTINCT department FROM employees WHERE department IS NOT NULL"
        results = self.db.execute_query(query, fetch=True)
        return [row['department'] for row in results] if results else []