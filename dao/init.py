"""
DAO Package
Contains all Data Access Objects
"""

from dao.student_dao import StudentDAO
from dao.course_dao import CourseDAO
from dao.employee_dao import EmployeeDAO
from dao.enquiry_dao import EnquiryDAO
from dao.fee_dao import FeeDAO
from dao.attendance_dao import AttendanceDAO
from dao.user_dao import UserDAO

__all__ = [
    'StudentDAO',
    'CourseDAO',
    'EmployeeDAO',
    'EnquiryDAO',
    'FeeDAO',
    'AttendanceDAO',
    'UserDAO'
]