"""
Enquiry Model
Represents an enquiry entity in the ERP system
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Enquiry:
    """Enquiry data model"""
    enquiry_id: Optional[int] = None
    name: str = ""
    phone: str = ""
    course: str = ""
    reference: str = ""
    status: str = "Pending"
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'enquiry_id': self.enquiry_id,
            'name': self.name,
            'phone': self.phone,
            'course': self.course,
            'reference': self.reference,
            'status': self.status,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Enquiry from dictionary"""
        return cls(
            enquiry_id=data.get('enquiry_id'),
            name=data.get('name', ''),
            phone=data.get('phone', ''),
            course=data.get('course', ''),
            reference=data.get('reference', ''),
            status=data.get('status', 'Pending'),
            created_at=data.get('created_at')
        )
    
    def __str__(self):
        return f"Enquiry(ID={self.enquiry_id}, Name={self.name})"