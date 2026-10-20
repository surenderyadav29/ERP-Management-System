"""
Student Service
Business logic layer for Student operations
"""

from typing import List, Optional, Tuple
from dao.student_dao import StudentDAO
from dao.course_dao import CourseDAO
from model.student import Student
from util.validators import Validators


class StudentService:
    """Service class for Student business logic"""
    
    def __init__(self):
        self.student_dao = StudentDAO()
        self.course_dao = CourseDAO()
    
    def add_student(self, student_data: dict) -> Tuple[bool, str]:
        """Add a new student with validation"""
        # Validate data
        is_valid, error_msg = Validators.validate_student_data(student_data)
        if not is_valid:
            return False, error_msg
        
        # Check if course exists
        if student_data.get('course_id'):
            course = self.course_dao.find_by_id(student_data['course_id'])
            if not course:
                return False, "Selected course does not exist!"
        
        # Create student object
        student = Student(
            student_name=student_data['student_name'],
            course_id=student_data.get('course_id'),
            phone=student_data.get('phone', ''),
            email=student_data.get('email', ''),
            total_fees=float(student_data.get('total_fees', 0))
        )
        
        # Insert into database
        student_id = self.student_dao.insert(student)
        if student_id:
            return True, f"Student added successfully! ID: {student_id}"
        return False, "Failed to add student. Please try again."
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """Get a student by ID"""
        return self.student_dao.find_by_id(student_id)
    
    def get_all_students(self) -> List[Student]:
        """Get all students"""
        return self.student_dao.find_all()
    
    def update_student(self, student_data: dict) -> Tuple[bool, str]:
        """Update an existing student"""
        # Validate data
        is_valid, error_msg = Validators.validate_student_data(student_data)
        if not is_valid:
            return False, error_msg
        
        # Check if student exists
        existing = self.student_dao.find_by_id(student_data['student_id'])
        if not existing:
            return False, "Student not found!"
        
        # Check if course exists
        if student_data.get('course_id'):
            course = self.course_dao.find_by_id(student_data['course_id'])
            if not course:
                return False, "Selected course does not exist!"
        
        # Update student object
        student = Student(
            student_id=student_data['student_id'],
            student_name=student_data['student_name'],
            course_id=student_data.get('course_id'),
            phone=student_data.get('phone', ''),
            email=student_data.get('email', ''),
            total_fees=float(student_data.get('total_fees', 0))
        )
        
        # Update in database
        if self.student_dao.update(student):
            return True, "Student updated successfully!"
        return False, "Failed to update student. Please try again."
    
    def delete_student(self, student_id: int) -> Tuple[bool, str]:
        """Delete a student"""
        # Check if student exists
        student = self.student_dao.find_by_id(student_id)
        if not student:
            return False, "Student not found!"
        
        # Delete from database
        if self.student_dao.delete(student_id):
            return True, "Student deleted successfully!"
        return False, "Failed to delete student. Please try again."
    
    def search_students(self, keyword: str) -> List[Student]:
        """Search students by keyword"""
        return self.student_dao.search(keyword)
    
    def get_students_by_course(self, course_id: int) -> List[Student]:
        """Get students enrolled in a specific course"""
        all_students = self.student_dao.find_all()
        return [s for s in all_students if s.course_id == course_id]