"""
Employee Service
Business logic layer for Employee operations
"""

from typing import List, Optional, Tuple
from dao.employee_dao import EmployeeDAO
from model.employee import Employee
from util.validators import Validators


class EmployeeService:
    """Service class for Employee business logic"""
    
    def __init__(self):
        self.employee_dao = EmployeeDAO()
    
    def add_employee(self, employee_data: dict) -> Tuple[bool, str]:
        """Add a new employee with validation"""
        # Validate data
        is_valid, error_msg = Validators.validate_employee_data(employee_data)
        if not is_valid:
            return False, error_msg
        
        # Create employee object
        employee = Employee(
            name=employee_data['name'],
            department=employee_data.get('department', ''),
            phone=employee_data.get('phone', ''),
            email=employee_data.get('email', '')
        )
        
        # Insert into database
        employee_id = self.employee_dao.insert(employee)
        if employee_id:
            return True, f"Employee added successfully! ID: {employee_id}"
        return False, "Failed to add employee. Please try again."
    
    def get_employee(self, employee_id: int) -> Optional[Employee]:
        """Get an employee by ID"""
        return self.employee_dao.find_by_id(employee_id)
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return self.employee_dao.find_all()
    
    def update_employee(self, employee_data: dict) -> Tuple[bool, str]:
        """Update an existing employee"""
        # Validate data
        is_valid, error_msg = Validators.validate_employee_data(employee_data)
        if not is_valid:
            return False, error_msg
        
        # Check if employee exists
        existing = self.employee_dao.find_by_id(employee_data['employee_id'])
        if not existing:
            return False, "Employee not found!"
        
        # Update employee object
        employee = Employee(
            employee_id=employee_data['employee_id'],
            name=employee_data['name'],
            department=employee_data.get('department', ''),
            phone=employee_data.get('phone', ''),
            email=employee_data.get('email', '')
        )
        
        # Update in database
        if self.employee_dao.update(employee):
            return True, "Employee updated successfully!"
        return False, "Failed to update employee. Please try again."
    
    def delete_employee(self, employee_id: int) -> Tuple[bool, str]:
        """Delete an employee"""
        # Check if employee exists
        employee = self.employee_dao.find_by_id(employee_id)
        if not employee:
            return False, "Employee not found!"
        
        # Delete from database
        if self.employee_dao.delete(employee_id):
            return True, "Employee deleted successfully!"
        return False, "Failed to delete employee. Please try again."
    
    def search_employees(self, keyword: str) -> List[Employee]:
        """Search employees by keyword"""
        return self.employee_dao.search(keyword)
    
    def get_departments(self) -> List[str]:
        """Get list of departments"""
        return self.employee_dao.get_departments()