"""
Attendance Model
Represents an attendance record in the ERP system
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class Attendance:
    """Attendance data model"""
    attendance_id: Optional[int] = None
    student_id: int = 0
    attendance_date: Optional[date] = None
    status: str = "Present"
    created_at: Optional[datetime] = None
    
    # Additional fields for display (populated via JOINs)
    student_name: str = ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'attendance_id': self.attendance_id,
            'student_id': self.student_id,
            'attendance_date': self.attendance_date,
            'status': self.status,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Attendance from dictionary"""
        return cls(
            attendance_id=data.get('attendance_id'),
            student_id=data.get('student_id', 0),
            attendance_date=data.get('attendance_date'),
            status=data.get('status', 'Present'),
            created_at=data.get('created_at'),
            student_name=data.get('student_name', '')
        )
    
    def __str__(self):
        return f"Attendance(ID={self.attendance_id}, Student={self.student_id}, Status={self.status})"