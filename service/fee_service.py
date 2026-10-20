"""
Fee Service
Business logic layer for Fee Payment operations
"""

from typing import List, Optional, Tuple
from datetime import date
from dao.fee_dao import FeeDAO
from dao.student_dao import StudentDAO
from model.fee import FeePayment
from util.validators import Validators


class FeeService:
    """Service class for Fee Payment business logic"""
    
    def __init__(self):
        self.fee_dao = FeeDAO()
        self.student_dao = StudentDAO()
    
    def record_payment(self, payment_data: dict) -> Tuple[bool, str]:
        """Record a new fee payment"""
        # Validate data
        is_valid, error_msg = Validators.validate_fee_data(payment_data)
        if not is_valid:
            return False, error_msg
        
        # Check if student exists
        student = self.student_dao.find_by_id(payment_data['student_id'])
        if not student:
            return False, "Student not found!"
        
        # Create fee payment object
        fee = FeePayment(
            student_id=payment_data['student_id'],
            amount_paid=float(payment_data['amount_paid']),
            payment_date=payment_data.get('payment_date', date.today())
        )
        
        # Insert into database
        receipt_id = self.fee_dao.insert(fee)
        if receipt_id:
            return True, f"Payment recorded successfully! Receipt ID: {receipt_id}"
        return False, "Failed to record payment. Please try again."
    
    def get_payment(self, receipt_id: int) -> Optional[FeePayment]:
        """Get a payment by receipt ID"""
        return self.fee_dao.find_by_id(receipt_id)
    
    def get_all_payments(self) -> List[FeePayment]:
        """Get all payments"""
        return self.fee_dao.find_all()
    
    def get_student_payments(self, student_id: int) -> List[FeePayment]:
        """Get all payments for a student"""
        return self.fee_dao.find_by_student(student_id)
    
    def update_payment(self, payment_data: dict) -> Tuple[bool, str]:
        """Update an existing payment"""
        # Validate data
        is_valid, error_msg = Validators.validate_fee_data(payment_data)
        if not is_valid:
            return False, error_msg
        
        # Check if payment exists
        existing = self.fee_dao.find_by_id(payment_data['receipt_id'])
        if not existing:
            return False, "Payment record not found!"
        
        # Update payment object
        fee = FeePayment(
            receipt_id=payment_data['receipt_id'],
            student_id=payment_data['student_id'],
            amount_paid=float(payment_data['amount_paid']),
            payment_date=payment_data.get('payment_date', date.today())
        )
        
        # Update in database
        if self.fee_dao.update(fee):
            return True, "Payment updated successfully!"
        return False, "Failed to update payment. Please try again."
    
    def delete_payment(self, receipt_id: int) -> Tuple[bool, str]:
        """Delete a payment"""
        # Check if payment exists
        payment = self.fee_dao.find_by_id(receipt_id)
        if not payment:
            return False, "Payment record not found!"
        
        # Delete from database
        if self.fee_dao.delete(receipt_id):
            return True, "Payment deleted successfully!"
        return False, "Failed to delete payment. Please try again."
    
    def get_payment_summary(self, student_id: int) -> dict:
        """Get payment summary for a student"""
        student = self.student_dao.find_by_id(student_id)
        if not student:
            return {}
        
        total_paid = self.fee_dao.get_total_paid(student_id)
        total_fees = student.total_fees
        balance = total_fees - total_paid
        
        return {
            'student_name': student.student_name,
            'total_fees': total_fees,
            'total_paid': total_paid,
            'balance': balance
        }
    
    def generate_receipt(self, receipt_id: int) -> Optional[dict]:
        """Generate receipt details"""
        payment = self.fee_dao.find_by_id(receipt_id)
        if not payment:
            return None
        
        student = self.student_dao.find_by_id(payment.student_id)
        if not student:
            return None
        
        total_paid = self.fee_dao.get_total_paid(payment.student_id)
        balance = student.total_fees - total_paid
        
        return {
            'receipt_id': payment.receipt_id,
            'student_id': payment.student_id,
            'student_name': student.student_name,
            'amount_paid': payment.amount_paid,
            'payment_date': payment.payment_date,
            'total_fees': student.total_fees,
            'total_paid': total_paid,
            'balance': balance
        }