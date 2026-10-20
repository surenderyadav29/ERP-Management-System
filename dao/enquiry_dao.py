"""
Enquiry DAO
Data Access Object for Enquiry entity
"""

from typing import List, Optional
from database.db_connection import get_db
from model.enquiry import Enquiry


class EnquiryDAO:
    """Data Access Object for Enquiry operations"""
    
    def __init__(self):
        self.db = get_db()
    
    def insert(self, enquiry: Enquiry) -> Optional[int]:
        """Insert a new enquiry into the database"""
        query = """
            INSERT INTO enquiries (name, phone, course, reference, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            enquiry.name, 
            enquiry.phone, 
            enquiry.course, 
            enquiry.reference, 
            enquiry.status
        )
        return self.db.execute_query(query, params)
    
    def find_by_id(self, enquiry_id: int) -> Optional[Enquiry]:
        """Find an enquiry by ID"""
        query = "SELECT * FROM enquiries WHERE enquiry_id = %s"
        results = self.db.execute_query(query, (enquiry_id,), fetch=True)
        if results and len(results) > 0:
            return Enquiry.from_dict(results[0])
        return None
    
    def find_all(self) -> List[Enquiry]:
        """Get all enquiries"""
        query = "SELECT * FROM enquiries ORDER BY enquiry_id DESC"
        results = self.db.execute_query(query, fetch=True)
        return [Enquiry.from_dict(row) for row in results] if results else []
    
    def update(self, enquiry: Enquiry) -> bool:
        """Update an existing enquiry"""
        query = """
            UPDATE enquiries 
            SET name = %s, phone = %s, course = %s, reference = %s, status = %s
            WHERE enquiry_id = %s
        """
        params = (
            enquiry.name, 
            enquiry.phone, 
            enquiry.course, 
            enquiry.reference, 
            enquiry.status, 
            enquiry.enquiry_id
        )
        result = self.db.execute_query(query, params)
        return result is not None
    
    def delete(self, enquiry_id: int) -> bool:
        """Delete an enquiry by ID"""
        query = "DELETE FROM enquiries WHERE enquiry_id = %s"
        result = self.db.execute_query(query, (enquiry_id,))
        return result is not None
    
    def search(self, keyword: str) -> List[Enquiry]:
        """Search enquiries by name, phone, or course"""
        query = """
            SELECT * FROM enquiries 
            WHERE name LIKE %s OR phone LIKE %s OR course LIKE %s
            ORDER BY enquiry_id DESC
        """
        search_term = f"%{keyword}%"
        results = self.db.execute_query(query, (search_term, search_term, search_term), fetch=True)
        return [Enquiry.from_dict(row) for row in results] if results else []
    
    def find_by_status(self, status: str) -> List[Enquiry]:
        """Get enquiries by status"""
        query = "SELECT * FROM enquiries WHERE status = %s ORDER BY enquiry_id DESC"
        results = self.db.execute_query(query, (status,), fetch=True)
        return [Enquiry.from_dict(row) for row in results] if results else []