"""
Course Model
Represents a course entity in the ERP system
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Course:
    """Course data model"""
    course_id: Optional[int] = None
    course_name: str = ""
    duration: str = ""
    fees: float = 0.0
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'duration': self.duration,
            'fees': self.fees,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Course from dictionary"""
        return cls(
            course_id=data.get('course_id'),
            course_name=data.get('course_name', ''),
            duration=data.get('duration', ''),
            fees=data.get('fees', 0.0),
            created_at=data.get('created_at')
        )
    
    def __str__(self):
        return f"Course(ID={self.course_id}, Name={self.course_name})"