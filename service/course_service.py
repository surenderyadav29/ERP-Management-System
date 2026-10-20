"""
Course Service
Business logic layer for Course operations
"""

from typing import List, Optional, Tuple
from dao.course_dao import CourseDAO
from dao.student_dao import StudentDAO
from model.course import Course
from util.validators import Validators


class CourseService:
    """Service class for Course business logic"""
    
    def __init__(self):
        self.course_dao = CourseDAO()
        self.student_dao = StudentDAO()
    
    def add_course(self, course_data: dict) -> Tuple[bool, str]:
        """Add a new course with validation"""
        # Validate data
        is_valid, error_msg = Validators.validate_course_data(course_data)
        if not is_valid:
            return False, error_msg
        
        # Create course object
        course = Course(
            course_name=course_data['course_name'],
            duration=course_data['duration'],
            fees=float(course_data.get('fees', 0))
        )
        
        # Insert into database
        course_id = self.course_dao.insert(course)
        if course_id:
            return True, f"Course added successfully! ID: {course_id}"
        return False, "Failed to add course. Please try again."
    
    def get_course(self, course_id: int) -> Optional[Course]:
        """Get a course by ID"""
        return self.course_dao.find_by_id(course_id)
    
    def get_all_courses(self) -> List[Course]:
        """Get all courses"""
        return self.course_dao.find_all()
    
    def get_course_list(self) -> List[dict]:
        """Get course list for dropdowns"""
        return self.course_dao.get_course_names()
    
    def update_course(self, course_data: dict) -> Tuple[bool, str]:
        """Update an existing course"""
        # Validate data
        is_valid, error_msg = Validators.validate_course_data(course_data)
        if not is_valid:
            return False, error_msg
        
        # Check if course exists
        existing = self.course_dao.find_by_id(course_data['course_id'])
        if not existing:
            return False, "Course not found!"
        
        # Update course object
        course = Course(
            course_id=course_data['course_id'],
            course_name=course_data['course_name'],
            duration=course_data['duration'],
            fees=float(course_data.get('fees', 0))
        )
        
        # Update in database
        if self.course_dao.update(course):
            return True, "Course updated successfully!"
        return False, "Failed to update course. Please try again."
    
    def delete_course(self, course_id: int) -> Tuple[bool, str]:
        """Delete a course"""
        # Check if course exists
        course = self.course_dao.find_by_id(course_id)
        if not course:
            return False, "Course not found!"
        
        # Check if students are enrolled
        student_count = self.student_dao.count_by_course(course_id)
        if student_count > 0:
            return False, f"Cannot delete! {student_count} students are enrolled in this course."
        
        # Delete from database
        if self.course_dao.delete(course_id):
            return True, "Course deleted successfully!"
        return False, "Failed to delete course. Please try again."
    
    def search_courses(self, keyword: str) -> List[Course]:
        """Search courses by keyword"""
        return self.course_dao.search(keyword)