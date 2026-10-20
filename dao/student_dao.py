"""
Student DAO
Data Access Object for Student entity
"""

from typing import List, Optional
from database.db_connection import get_db
from model.student import Student


class StudentDAO:
    """Data Access Object for Student operations"""
    
    def __init__(self):
        self.db = get_db()
    
    def insert(self, student: Student) -> Optional[int]:
        """Insert a new student into the database"""
        query = """
            INSERT INTO students (student_name, course_id, phone, email, total_fees)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            student.student_name,
            student.course_id,
            student.phone,
            student.email,
            student.total_fees
        )
        return self.db.execute_query(query, params)
    
    def find_by_id(self, student_id: int) -> Optional[Student]:
        """Find a student by ID"""
        query = "SELECT * FROM students WHERE student_id = %s"
        results = self.db.execute_query(query, (student_id,), fetch=True)
        if results and len(results) > 0:
            return Student.from_dict(results[0])
        return None
    
    def find_all(self) -> List[Student]:
        """Get all students"""
        query = """
            SELECT s.*, c.course_name 
            FROM students s 
            LEFT JOIN courses c ON s.course_id = c.course_id 
            ORDER BY s.student_id DESC
        """
        results = self.db.execute_query(query, fetch=True)
        return [Student.from_dict(row) for row in results] if results else []
    
    def update(self, student: Student) -> bool:
        """Update an existing student"""
        query = """
            UPDATE students 
            SET student_name = %s, course_id = %s, phone = %s, email = %s, total_fees = %s
            WHERE student_id = %s
        """
        params = (
            student.student_name,
            student.course_id,
            student.phone,
            student.email,
            student.total_fees,
            student.student_id
        )
        result = self.db.execute_query(query, params)
        return result is not None
    
    def delete(self, student_id: int) -> bool:
        """Delete a student by ID"""
        query = "DELETE FROM students WHERE student_id = %s"
        result = self.db.execute_query(query, (student_id,))
        return result is not None
    
    def search(self, keyword: str) -> List[Student]:
        """Search students by name, email, or phone"""
        query = """
            SELECT s.*, c.course_name 
            FROM students s 
            LEFT JOIN courses c ON s.course_id = c.course_id 
            WHERE s.student_name LIKE %s OR s.email LIKE %s OR s.phone LIKE %s
            ORDER BY s.student_id DESC
        """
        search_term = f"%{keyword}%"
        results = self.db.execute_query(query, (search_term, search_term, search_term), fetch=True)
        return [Student.from_dict(row) for row in results] if results else []
    
    def count_by_course(self, course_id: int) -> int:
        """Count students enrolled in a course"""
        query = "SELECT COUNT(*) as count FROM students WHERE course_id = %s"
        result = self.db.execute_query(query, (course_id,), fetch=True)
        return result[0]['count'] if result else 0