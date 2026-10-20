"""
Course DAO
Data Access Object for Course entity
"""

from typing import List, Optional
from database.db_connection import get_db
from model.course import Course


class CourseDAO:
    """Data Access Object for Course operations"""
    
    def __init__(self):
        self.db = get_db()
    
    def insert(self, course: Course) -> Optional[int]:
        """Insert a new course into the database"""
        query = """
            INSERT INTO courses (course_name, duration, fees)
            VALUES (%s, %s, %s)
        """
        params = (course.course_name, course.duration, course.fees)
        return self.db.execute_query(query, params)
    
    def find_by_id(self, course_id: int) -> Optional[Course]:
        """Find a course by ID"""
        query = "SELECT * FROM courses WHERE course_id = %s"
        results = self.db.execute_query(query, (course_id,), fetch=True)
        if results and len(results) > 0:
            return Course.from_dict(results[0])
        return None
    
    def find_all(self) -> List[Course]:
        """Get all courses"""
        query = "SELECT * FROM courses ORDER BY course_id DESC"
        results = self.db.execute_query(query, fetch=True)
        return [Course.from_dict(row) for row in results] if results else []
    
    def update(self, course: Course) -> bool:
        """Update an existing course"""
        query = """
            UPDATE courses 
            SET course_name = %s, duration = %s, fees = %s
            WHERE course_id = %s
        """
        params = (course.course_name, course.duration, course.fees, course.course_id)
        result = self.db.execute_query(query, params)
        return result is not None
    
    def delete(self, course_id: int) -> bool:
        """Delete a course by ID"""
        query = "DELETE FROM courses WHERE course_id = %s"
        result = self.db.execute_query(query, (course_id,))
        return result is not None
    
    def search(self, keyword: str) -> List[Course]:
        """Search courses by name"""
        query = "SELECT * FROM courses WHERE course_name LIKE %s ORDER BY course_id DESC"
        search_term = f"%{keyword}%"
        results = self.db.execute_query(query, (search_term,), fetch=True)
        return [Course.from_dict(row) for row in results] if results else []
    
    def get_course_names(self) -> List[dict]:
        """Get all course names and IDs for dropdowns"""
        query = "SELECT course_id, course_name FROM courses ORDER BY course_name"
        return self.db.execute_query(query, fetch=True) or []