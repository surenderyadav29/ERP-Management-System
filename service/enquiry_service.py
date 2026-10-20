"""
Enquiry Service
Business logic layer for Enquiry operations
"""

from typing import List, Optional, Tuple
from dao.enquiry_dao import EnquiryDAO
from model.enquiry import Enquiry
from util.validators import Validators


class EnquiryService:
    """Service class for Enquiry business logic"""
    
    def __init__(self):
        self.enquiry_dao = EnquiryDAO()
    
    def add_enquiry(self, enquiry_data: dict) -> Tuple[bool, str]:
        """Add a new enquiry with validation"""
        # Validate data
        is_valid, error_msg = Validators.validate_enquiry_data(enquiry_data)
        if not is_valid:
            return False, error_msg
        
        # Create enquiry object
        enquiry = Enquiry(
            name=enquiry_data['name'],
            phone=enquiry_data.get('phone', ''),
            course=enquiry_data.get('course', ''),
            reference=enquiry_data.get('reference', ''),
            status=enquiry_data.get('status', 'Pending')
        )
        
        # Insert into database
        enquiry_id = self.enquiry_dao.insert(enquiry)
        if enquiry_id:
            return True, f"Enquiry added successfully! ID: {enquiry_id}"
        return False, "Failed to add enquiry. Please try again."
    
    def get_enquiry(self, enquiry_id: int) -> Optional[Enquiry]:
        """Get an enquiry by ID"""
        return self.enquiry_dao.find_by_id(enquiry_id)
    
    def get_all_enquiries(self) -> List[Enquiry]:
        """Get all enquiries"""
        return self.enquiry_dao.find_all()
    
    def update_enquiry(self, enquiry_data: dict) -> Tuple[bool, str]:
        """Update an existing enquiry"""
        # Validate data
        is_valid, error_msg = Validators.validate_enquiry_data(enquiry_data)
        if not is_valid:
            return False, error_msg
        
        # Check if enquiry exists
        existing = self.enquiry_dao.find_by_id(enquiry_data['enquiry_id'])
        if not existing:
            return False, "Enquiry not found!"
        
        # Update enquiry object
        enquiry = Enquiry(
            enquiry_id=enquiry_data['enquiry_id'],
            name=enquiry_data['name'],
            phone=enquiry_data.get('phone', ''),
            course=enquiry_data.get('course', ''),
            reference=enquiry_data.get('reference', ''),
            status=enquiry_data.get('status', 'Pending')
        )
        
        # Update in database
        if self.enquiry_dao.update(enquiry):
            return True, "Enquiry updated successfully!"
        return False, "Failed to update enquiry. Please try again."
    
    def delete_enquiry(self, enquiry_id: int) -> Tuple[bool, str]:
        """Delete an enquiry"""
        # Check if enquiry exists
        enquiry = self.enquiry_dao.find_by_id(enquiry_id)
        if not enquiry:
            return False, "Enquiry not found!"
        
        # Delete from database
        if self.enquiry_dao.delete(enquiry_id):
            return True, "Enquiry deleted successfully!"
        return False, "Failed to delete enquiry. Please try again."
    
    def search_enquiries(self, keyword: str) -> List[Enquiry]:
        """Search enquiries by keyword"""
        return self.enquiry_dao.search(keyword)
    
    def get_enquiries_by_status(self, status: str) -> List[Enquiry]:
        """Get enquiries by status"""
        return self.enquiry_dao.find_by_status(status)