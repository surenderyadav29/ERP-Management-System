"""
Student Model
Represents a student entity in the ERP system
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Student:
    """Student data model"""
    student_id: Optional[int] = None
    student_name: str = ""
    course_id: Optional[int] = None
    phone: str = ""
    email: str = ""
    total_fees: float = 0.0
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'student_id': self.student_id,
            'student_name': self.student_name,
            'course_id': self.course_id,
            'phone': self.phone,
            'email': self.email,
            'total_fees': self.total_fees,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Student from dictionary"""
        return cls(
            student_id=data.get('student_id'),
            student_name=data.get('student_name', ''),
            course_id=data.get('course_id'),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            total_fees=data.get('total_fees', 0.0),
            created_at=data.get('created_at')
        )
    
    def __str__(self):
        return f"Student(ID={self.student_id}, Name={self.student_name})"