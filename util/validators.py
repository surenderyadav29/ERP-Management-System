"""
Validators Module
Contains validation functions for input data
"""

import re
from datetime import datetime


class Validators:
    """Utility class for input validation"""
    
    @staticmethod
    def validate_required(value: str, field_name: str) -> tuple:
        """Validate that a field is not empty"""
        if not value or value.strip() == "":
            return False, f"{field_name} is required!"
        return True, ""
    
    @staticmethod
    def validate_phone(phone: str) -> tuple:
        """Validate phone number format"""
        if not phone:
            return True, ""  # Phone can be optional
        
        # Remove any spaces or dashes
        phone = phone.replace(" ", "").replace("-", "")
        
        # Check if it's a valid phone number (10 digits for India)
        pattern = r'^[6-9]\d{9}$'
        if not re.match(pattern, phone):
            return False, "Invalid phone number! Must be 10 digits starting with 6-9"
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> tuple:
        """Validate email format"""
        if not email:
            return True, ""  # Email can be optional
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format! Example: user@domain.com"
        return True, ""
    
    @staticmethod
    def validate_numeric(value: str, field_name: str) -> tuple:
        """Validate that a field contains only numbers"""
        if not value:
            return True, ""
        
        try:
            float(value)
            return True, ""
        except ValueError:
            return False, f"{field_name} must be a valid number!"
    
    @staticmethod
    def validate_positive_number(value: str, field_name: str) -> tuple:
        """Validate that a field is a positive number"""
        if not value:
            return True, ""
        
        try:
            num = float(value)
            if num < 0:
                return False, f"{field_name} must be a positive number!"
            return True, ""
        except ValueError:
            return False, f"{field_name} must be a valid number!"
    
    @staticmethod
    def validate_date(date_str: str) -> tuple:
        """Validate date format (YYYY-MM-DD)"""
        if not date_str:
            return True, ""
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, ""
        except ValueError:
            return False, "Invalid date format! Use YYYY-MM-DD"
    
    @staticmethod
    def validate_length(value: str, min_len: int, max_len: int, field_name: str) -> tuple:
        """Validate string length"""
        if not value:
            return True, ""
        
        if len(value) < min_len:
            return False, f"{field_name} must be at least {min_len} characters!"
        if len(value) > max_len:
            return False, f"{field_name} must not exceed {max_len} characters!"
        return True, ""
    
    @staticmethod
    def validate_student_data(data: dict) -> tuple:
        """Validate complete student data"""
        errors = []
        
        # Name validation
        valid, msg = Validators.validate_required(data.get('student_name', ''), 'Student Name')
        if not valid:
            errors.append(msg)
        
        # Phone validation
        valid, msg = Validators.validate_phone(data.get('phone', ''))
        if not valid:
            errors.append(msg)
        
        # Email validation
        valid, msg = Validators.validate_email(data.get('email', ''))
        if not valid:
            errors.append(msg)
        
        # Fees validation
        valid, msg = Validators.validate_positive_number(data.get('total_fees', '0'), 'Total Fees')
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, "\n".join(errors)
    
    @staticmethod
    def validate_employee_data(data: dict) -> tuple:
        """Validate complete employee data"""
        errors = []
        
        # Name validation
        valid, msg = Validators.validate_required(data.get('name', ''), 'Employee Name')
        if not valid:
            errors.append(msg)
        
        # Phone validation
        valid, msg = Validators.validate_phone(data.get('phone', ''))
        if not valid:
            errors.append(msg)
        
        # Email validation
        valid, msg = Validators.validate_email(data.get('email', ''))
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, "\n".join(errors)
    
    @staticmethod
    def validate_course_data(data: dict) -> tuple:
        """Validate complete course data"""
        errors = []
        
        # Name validation
        valid, msg = Validators.validate_required(data.get('course_name', ''), 'Course Name')
        if not valid:
            errors.append(msg)
        
        # Duration validation
        valid, msg = Validators.validate_required(data.get('duration', ''), 'Duration')
        if not valid:
            errors.append(msg)
        
        # Fees validation
        valid, msg = Validators.validate_positive_number(data.get('fees', '0'), 'Fees')
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, "\n".join(errors)
    
    @staticmethod
    def validate_enquiry_data(data: dict) -> tuple:
        """Validate complete enquiry data"""
        errors = []
        
        # Name validation
        valid, msg = Validators.validate_required(data.get('name', ''), 'Name')
        if not valid:
            errors.append(msg)
        
        # Phone validation
        valid, msg = Validators.validate_phone(data.get('phone', ''))
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, "\n".join(errors)
    
    @staticmethod
    def validate_fee_data(data: dict) -> tuple:
        """Validate fee payment data"""
        errors = []
        
        # Student ID validation
        if not data.get('student_id'):
            errors.append("Student is required!")
        
        # Amount validation
        valid, msg = Validators.validate_required(data.get('amount_paid', ''), 'Amount')
        if not valid:
            errors.append(msg)
        else:
            valid, msg = Validators.validate_positive_number(data.get('amount_paid', '0'), 'Amount')
            if not valid:
                errors.append(msg)
        
        # Date validation
        valid, msg = Validators.validate_date(data.get('payment_date', ''))
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, "\n".join(errors)
    
    @staticmethod
    def validate_attendance_data(data: dict) -> tuple:
        """Validate attendance data"""
        errors = []
        
        # Student ID validation
        if not data.get('student_id'):
            errors.append("Student is required!")
        
        # Date validation
        valid, msg = Validators.validate_date(data.get('attendance_date', ''))
        if not valid:
            errors.append(msg)
        
        # Status validation
        if data.get('status') not in ['Present', 'Absent']:
            errors.append("Status must be 'Present' or 'Absent'!")
        
        return len(errors) == 0, "\n".join(errors)