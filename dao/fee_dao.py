"""
Fee DAO
Data Access Object for Fee Payment entity
"""

from typing import List, Optional
from database.db_connection import get_db
from model.fee import FeePayment


class FeeDAO:
    """Data Access Object for Fee Payment operations"""
    
    def __init__(self):
        self.db = get_db()
    
    def insert(self, fee: FeePayment) -> Optional[int]:
        """Insert a new fee payment into the database"""
        query = """
            INSERT INTO fee_payments (student_id, amount_paid, payment_date)
            VALUES (%s, %s, %s)
        """
        params = (fee.student_id, fee.amount_paid, fee.payment_date)
        return self.db.execute_query(query, params)
    
    def find_by_id(self, receipt_id: int) -> Optional[FeePayment]:
        """Find a fee payment by receipt ID"""
        query = """
            SELECT f.*, s.student_name 
            FROM fee_payments f 
            JOIN students s ON f.student_id = s.student_id 
            WHERE f.receipt_id = %s
        """
        results = self.db.execute_query(query, (receipt_id,), fetch=True)
        if results and len(results) > 0:
            return FeePayment.from_dict(results[0])
        return None
    
    def find_all(self) -> List[FeePayment]:
        """Get all fee payments"""
        query = """
            SELECT f.*, s.student_name 
            FROM fee_payments f 
            JOIN students s ON f.student_id = s.student_id 
            ORDER BY f.receipt_id DESC
        """
        results = self.db.execute_query(query, fetch=True)
        return [FeePayment.from_dict(row) for row in results] if results else []
    
    def find_by_student(self, student_id: int) -> List[FeePayment]:
        """Get all payments for a student"""
        query = """
            SELECT f.*, s.student_name 
            FROM fee_payments f 
            JOIN students s ON f.student_id = s.student_id 
            WHERE f.student_id = %s 
            ORDER BY f.payment_date DESC
        """
        results = self.db.execute_query(query, (student_id,), fetch=True)
        return [FeePayment.from_dict(row) for row in results] if results else []
    
    def update(self, fee: FeePayment) -> bool:
        """Update an existing fee payment"""
        query = """
            UPDATE fee_payments 
            SET student_id = %s, amount_paid = %s, payment_date = %s
            WHERE receipt_id = %s
        """
        params = (fee.student_id, fee.amount_paid, fee.payment_date, fee.receipt_id)
        result = self.db.execute_query(query, params)
        return result is not None
    
    def delete(self, receipt_id: int) -> bool:
        """Delete a fee payment by receipt ID"""
        query = "DELETE FROM fee_payments WHERE receipt_id = %s"
        result = self.db.execute_query(query, (receipt_id,))
        return result is not None
    
    def get_total_paid(self, student_id: int) -> float:
        """Get total amount paid by a student"""
        query = "SELECT SUM(amount_paid) as total FROM fee_payments WHERE student_id = %s"
        results = self.db.execute_query(query, (student_id,), fetch=True)
        return results[0]['total'] if results and results[0]['total'] else 0.0
    
    def get_daily_collection(self, date: str) -> float:
        """Get total collection for a specific date"""
        query = "SELECT SUM(amount_paid) as total FROM fee_payments WHERE payment_date = %s"
        results = self.db.execute_query(query, (date,), fetch=True)
        return results[0]['total'] if results and results[0]['total'] else 0.0
    
    def get_monthly_collection(self, year: int, month: int) -> float:
        """Get total collection for a specific month"""
        query = """
            SELECT SUM(amount_paid) as total 
            FROM fee_payments 
            WHERE YEAR(payment_date) = %s AND MONTH(payment_date) = %s
        """
        results = self.db.execute_query(query, (year, month), fetch=True)
        return results[0]['total'] if results and results[0]['total'] else 0.0