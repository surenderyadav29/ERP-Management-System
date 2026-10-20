"""
Attendance Service
Business logic layer for Attendance operations
"""

from typing import List, Optional, Tuple
from datetime import date
from dao.attendance_dao import AttendanceDAO
from dao.student_dao import StudentDAO
from model.attendance import Attendance
from util.validators import Validators


class AttendanceService:
    """Service class for Attendance business logic"""
    
    def __init__(self):
        self.attendance_dao = AttendanceDAO()
        self.student_dao = StudentDAO()
    
    def mark_attendance(self, attendance_data: dict) -> Tuple[bool, str]:
        """Mark attendance for a student"""
        # Validate data
        is_valid, error_msg = Validators.validate_attendance_data(attendance_data)
        if not is_valid:
            return False, error_msg
        
        # Check if student exists
        student = self.student_dao.find_by_id(attendance_data['student_id'])
        if not student:
            return False, "Student not found!"
        
        # Check for duplicate
        if self.attendance_dao.check_duplicate(
            attendance_data['student_id'], 
            attendance_data['attendance_date']
        ):
            return False, "Attendance already marked for this student on this date!"
        
        # Create attendance object
        attendance = Attendance(
            student_id=attendance_data['student_id'],
            attendance_date=attendance_data['attendance_date'],
            status=attendance_data.get('status', 'Present')
        )
        
        # Insert into database
        attendance_id = self.attendance_dao.insert(attendance)
        if attendance_id:
            return True, "Attendance marked successfully!"
        return False, "Failed to mark attendance. Please try again."
    
    def get_attendance(self, attendance_id: int) -> Optional[Attendance]:
        """Get an attendance record by ID"""
        return self.attendance_dao.find_by_id(attendance_id)
    
    def get_all_attendance(self) -> List[Attendance]:
        """Get all attendance records"""
        return self.attendance_dao.find_all()
    
    def get_student_attendance(self, student_id: int) -> List[Attendance]:
        """Get attendance records for a student"""
        return self.attendance_dao.find_by_student(student_id)
    
    def get_date_attendance(self, date_str: str) -> List[Attendance]:
        """Get attendance records for a specific date"""
        return self.attendance_dao.find_by_date(date_str)
    
    def update_attendance(self, attendance_data: dict) -> Tuple[bool, str]:
        """Update an existing attendance record"""
        # Validate data
        is_valid, error_msg = Validators.validate_attendance_data(attendance_data)
        if not is_valid:
            return False, error_msg
        
        # Check if record exists
        existing = self.attendance_dao.find_by_id(attendance_data['attendance_id'])
        if not existing:
            return False, "Attendance record not found!"
        
        # Update attendance object
        attendance = Attendance(
            attendance_id=attendance_data['attendance_id'],
            student_id=attendance_data['student_id'],
            attendance_date=attendance_data['attendance_date'],
            status=attendance_data.get('status', 'Present')
        )
        
        # Update in database
        if self.attendance_dao.update(attendance):
            return True, "Attendance updated successfully!"
        return False, "Failed to update attendance. Please try again."
    
    def delete_attendance(self, attendance_id: int) -> Tuple[bool, str]:
        """Delete an attendance record"""
        # Check if record exists
        attendance = self.attendance_dao.find_by_id(attendance_id)
        if not attendance:
            return False, "Attendance record not found!"
        
        # Delete from database
        if self.attendance_dao.delete(attendance_id):
            return True, "Attendance deleted successfully!"
        return False, "Failed to delete attendance. Please try again."
    
    def get_attendance_report(self, student_id: int) -> dict:
        """Get attendance statistics for a student"""
        student = self.student_dao.find_by_id(student_id)
        if not student:
            return {}
        
        stats = self.attendance_dao.get_attendance_stats(student_id)
        total = stats['total_days']
        present = stats['present_days']
        percentage = (present / total * 100) if total > 0 else 0
        
        return {
            'student_id': student_id,
            'student_name': student.student_name,
            'total_days': total,
            'present_days': present,
            'absent_days': stats['absent_days'],
            'percentage': round(percentage, 2)
        }
    
    def bulk_mark_attendance(self, date_str: str, attendance_list: List[dict]) -> Tuple[bool, str]:
        """Mark attendance for multiple students"""
        success_count = 0
        for item in attendance_list:
            attendance_data = {
                'student_id': item['student_id'],
                'attendance_date': date_str,
                'status': item.get('status', 'Present')
            }
            is_valid, _ = self.mark_attendance(attendance_data)
            if is_valid:
                success_count += 1
        
        return True, f"Attendance marked for {success_count} students."