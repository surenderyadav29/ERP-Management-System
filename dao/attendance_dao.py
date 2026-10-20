"""
Attendance DAO
Data Access Object for Attendance entity
"""

from typing import List, Optional
from database.db_connection import get_db
from model.attendance import Attendance


class AttendanceDAO:
    """Data Access Object for Attendance operations"""
    
    def __init__(self):
        self.db = get_db()
    
    def insert(self, attendance: Attendance) -> Optional[int]:
        """Insert a new attendance record into the database"""
        query = """
            INSERT INTO attendance (student_id, attendance_date, status)
            VALUES (%s, %s, %s)
        """
        params = (attendance.student_id, attendance.attendance_date, attendance.status)
        return self.db.execute_query(query, params)
    
    def find_by_id(self, attendance_id: int) -> Optional[Attendance]:
        """Find an attendance record by ID"""
        query = """
            SELECT a.*, s.student_name 
            FROM attendance a 
            JOIN students s ON a.student_id = s.student_id 
            WHERE a.attendance_id = %s
        """
        results = self.db.execute_query(query, (attendance_id,), fetch=True)
        if results and len(results) > 0:
            return Attendance.from_dict(results[0])
        return None
    
    def find_all(self) -> List[Attendance]:
        """Get all attendance records"""
        query = """
            SELECT a.*, s.student_name 
            FROM attendance a 
            JOIN students s ON a.student_id = s.student_id 
            ORDER BY a.attendance_date DESC, a.attendance_id DESC
        """
        results = self.db.execute_query(query, fetch=True)
        return [Attendance.from_dict(row) for row in results] if results else []
    
    def find_by_student(self, student_id: int) -> List[Attendance]:
        """Get all attendance records for a student"""
        query = """
            SELECT a.*, s.student_name 
            FROM attendance a 
            JOIN students s ON a.student_id = s.student_id 
            WHERE a.student_id = %s 
            ORDER BY a.attendance_date DESC
        """
        results = self.db.execute_query(query, (student_id,), fetch=True)
        return [Attendance.from_dict(row) for row in results] if results else []
    
    def find_by_date(self, date: str) -> List[Attendance]:
        """Get all attendance records for a specific date"""
        query = """
            SELECT a.*, s.student_name 
            FROM attendance a 
            JOIN students s ON a.student_id = s.student_id 
            WHERE a.attendance_date = %s 
            ORDER BY s.student_name
        """
        results = self.db.execute_query(query, (date,), fetch=True)
        return [Attendance.from_dict(row) for row in results] if results else []
    
    def update(self, attendance: Attendance) -> bool:
        """Update an existing attendance record"""
        query = """
            UPDATE attendance 
            SET student_id = %s, attendance_date = %s, status = %s
            WHERE attendance_id = %s
        """
        params = (
            attendance.student_id, 
            attendance.attendance_date, 
            attendance.status, 
            attendance.attendance_id
        )
        result = self.db.execute_query(query, params)
        return result is not None
    
    def delete(self, attendance_id: int) -> bool:
        """Delete an attendance record by ID"""
        query = "DELETE FROM attendance WHERE attendance_id = %s"
        result = self.db.execute_query(query, (attendance_id,))
        return result is not None
    
    def get_attendance_stats(self, student_id: int) -> dict:
        """Get attendance statistics for a student"""
        query = """
            SELECT 
                COUNT(*) as total_days,
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_days,
                SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent_days
            FROM attendance 
            WHERE student_id = %s
        """
        results = self.db.execute_query(query, (student_id,), fetch=True)
        if results:
            return results[0]
        return {'total_days': 0, 'present_days': 0, 'absent_days': 0}
    
    def check_duplicate(self, student_id: int, date: str) -> bool:
        """Check if attendance already marked for student on date"""
        query = "SELECT COUNT(*) as count FROM attendance WHERE student_id = %s AND attendance_date = %s"
        results = self.db.execute_query(query, (student_id, date), fetch=True)
        return results[0]['count'] > 0 if results else False