"""
ERP Management System - Main Entry Point
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# ---------------------------------------------------------
# This ensures Python can find your folders (ui, dao, etc.)
# ---------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import UI components
from ui.login_ui import LoginUI
from ui.dashboard_ui import DashboardUI
from ui.student_ui import StudentUI
from ui.course_ui import CourseUI
from ui.employee_ui import EmployeeUI
from ui.enquiry_ui import EnquiryUI
from ui.fee_ui import FeeUI
from ui.attendance_ui import AttendanceUI
from ui.reports_ui import ReportsUI

# Import Database
from database.db_connection import get_db


class ERPApplication:
    """Main Application Class"""
    
    def __init__(self):
        # 1. Create the main window
        self.root = tk.Tk()
        self.current_user = None
        
        # 2. Connect to Database
        self.init_database()
        
        # 3. Show the Login Screen
        self.show_login()
    
    def init_database(self):
        """Check database connection on startup"""
        try:
            db = get_db()
            if db.get_connection():
                print("✓ Database Connected Successfully!")
            else:
                messagebox.showerror(
                    "Database Error", 
                    "Could not connect to MySQL.\n\n"
                    "1. Is MySQL running?\n"
                    "2. Did you create the database 'erp_system_db'?\n"
                    "3. Check password in 'database/db_connection.py'."
                )
                sys.exit(1)
        except Exception as e:
            messagebox.showerror("Error", f"Database Error:\n{e}")
            sys.exit(1)
    
    def show_login(self):
        """Display the Login Window"""
        self.clear_root()
        # Pass 'self.on_login_success' so login knows what to do next
        LoginUI(self.root, self.on_login_success)
    
    def on_login_success(self, user):
        """Called when login is successful"""
        self.current_user = user
        self.show_dashboard()
    
    def show_dashboard(self):
        """Display the Main Dashboard"""
        self.clear_root()
        
        # Define what happens when buttons are clicked
        callbacks = {
            'logout': self.logout,
            'student': self.open_student,
            'employee': self.open_employee,
            'course': self.open_course,
            'enquiry': self.open_enquiry,
            'fee': self.open_fee,
            'attendance': self.open_attendance,
            'reports': self.open_reports
        }
        
        DashboardUI(self.root, self.current_user, callbacks)
    
    def logout(self):
        """Log out and return to login"""
        self.current_user = None
        self.show_login()
    
    # --- Methods to open modules ---
    
    def open_student(self):
        StudentUI(self.root)

    def open_employee(self):
        EmployeeUI(self.root)

    def open_course(self):
        CourseUI(self.root)

    def open_enquiry(self):
        EnquiryUI(self.root)

    def open_fee(self):
        FeeUI(self.root)

    def open_attendance(self):
        AttendanceUI(self.root)

    def open_reports(self):
        ReportsUI(self.root)
    
    def clear_root(self):
        """Clear the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        """Start the application loop"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle the X button click"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                db = get_db()
                db.close_connection()
            except:
                pass
            self.root.destroy()


# ---------------------------------------------------------
# Execution starts here
# ---------------------------------------------------------
if __name__ == "__main__":
    print("Starting ERP System...")
    
    try:
        app = ERPApplication()
        app.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        messagebox.showerror("Fatal Error", f"Application crashed:\n{e}")