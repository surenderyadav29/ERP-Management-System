"""
Fee Model
Represents a fee payment entity in the ERP system
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class FeePayment:
    """Fee Payment data model"""
    receipt_id: Optional[int] = None
    student_id: int = 0
    amount_paid: float = 0.0
    payment_date: Optional[date] = None
    created_at: Optional[datetime] = None
    
    # Additional fields for display
    student_name: str = ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'receipt_id': self.receipt_id,
            'student_id': self.student_id,
            'amount_paid': self.amount_paid,
            'payment_date': self.payment_date,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create FeePayment from dictionary"""
        return cls(
            receipt_id=data.get('receipt_id'),
            student_id=data.get('student_id', 0),
            amount_paid=data.get('amount_paid', 0.0),
            payment_date=data.get('payment_date'),
            created_at=data.get('created_at'),
            student_name=data.get('student_name', '')
        )
    
    def __str__(self):
        return f"FeePayment(Receipt={self.receipt_id}, Student={self.student_id})"