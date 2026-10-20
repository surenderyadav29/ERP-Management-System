"""
Service Package
Contains all business logic services
"""

from service.student_service import StudentService
from service.course_service import CourseService
from service.employee_service import EmployeeService
from service.enquiry_service import EnquiryService
from service.fee_service import FeeService
from service.attendance_service import AttendanceService
from service.auth_service import AuthService

__all__ = [
    'StudentService',
    'CourseService',
    'EmployeeService',
    'EnquiryService',
    'FeeService',
    'AttendanceService',
    'AuthService'
]