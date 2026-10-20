"""
Model Package
Contains all data models for the ERP system
"""

from model.student import Student
from model.course import Course
from model.employee import Employee
from model.enquiry import Enquiry
from model.fee import FeePayment
from model.attendance import Attendance
from model.user import User

__all__ = [
    'Student',
    'Course',
    'Employee',
    'Enquiry',
    'FeePayment',
    'Attendance',
    'User'
]