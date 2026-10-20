"""
Employee Model
Represents an employee entity in the ERP system
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Employee:
    """Employee data model"""
    employee_id: Optional[int] = None
    name: str = ""
    department: str = ""
    phone: str = ""
    email: str = ""
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'department': self.department,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Employee from dictionary"""
        return cls(
            employee_id=data.get('employee_id'),
            name=data.get('name', ''),
            department=data.get('department', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            created_at=data.get('created_at')
        )
    
    def __str__(self):
        return f"Employee(ID={self.employee_id}, Name={self.name})"