"""
Reports UI
Generate and display various reports
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from service.student_service import StudentService
from service.course_service import CourseService
from service.employee_service import EmployeeService
from service.fee_service import FeeService
from service.attendance_service import AttendanceService


class ReportsUI:
    """Reports window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.student_service = StudentService()
        self.course_service = CourseService()
        self.employee_service = EmployeeService()
        self.fee_service = FeeService()
        self.attendance_service = AttendanceService()
        
        # Create Toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Reports")
        self.window.geometry("900x650")
        self.window.configure(bg='#ecf0f1')
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets"""
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title
        tk.Label(
            main_frame,
            text="📊 Reports Dashboard",
            font=('Helvetica', 18, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        # Report buttons frame
        btn_frame = tk.Frame(main_frame, bg='#ecf0f1')
        btn_frame.pack(fill='x', pady=(0, 15))
        
        reports = [
            ("Student Report", self.student_report, '#3498db'),
            ("Fee Collection", self.fee_report, '#27ae60'),
            ("Attendance Report", self.attendance_report, '#9b59b6'),
            ("Course Stats", self.course_report, '#e67e22'),
            ("Employee Report", self.employee_report, '#1abc9c')
        ]
        
        for i, (text, command, color) in enumerate(reports):
            btn = tk.Button(
                btn_frame,
                text=text,
                font=('Helvetica', 10, 'bold'),
                bg=color,
                fg='white',
                activebackground=color,
                cursor='hand2',
                width=15,
                command=command
            )
            btn.grid(row=0, column=i, padx=5)
        
        # Report display area
        display_frame = tk.Frame(main_frame, bg='white', padx=15, pady=15)
        display_frame.pack(fill='both', expand=True)
        
        # Title label for specific report
        self.report_title = tk.Label(
            display_frame,
            text="Select a report button above to generate data",
            font=('Helvetica', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        self.report_title.pack(anchor='w', pady=(0, 10))
        
        # Treeview for reports
        self.columns = ('Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6')
        self.tree = ttk.Treeview(display_frame, columns=self.columns, show='headings', height=22)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Summary frame
        self.summary_frame = tk.Frame(main_frame, bg='#bdc3c7', padx=15, pady=10)
        self.summary_frame.pack(fill='x', pady=(15, 0))
        
        self.summary_label = tk.Label(
            self.summary_frame,
            text="Summary will appear here after generating a report",
            font=('Helvetica', 11),
            bg='#bdc3c7',
            fg='#2c3e50'
        )
        self.summary_label.pack(anchor='w')
    
    def clear_tree(self):
        """Clear treeview and reset columns"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for col in self.columns:
            self.tree.heading(col, text='')
            self.tree.column(col, width=0)
    
    def student_report(self):
        """Generate student report"""
        self.clear_tree()
        self.report_title.config(text="📚 Student Report")
        
        columns = ('ID', 'Name', 'Course', 'Phone', 'Email', 'Total Fees')
        widths = [60, 180, 150, 100, 180, 100]
        
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        students = self.student_service.get_all_students()
        total_fees = 0
        
        for s in students:
            course_name = ''
            if s.course_id:
                course = self.course_service.get_course(s.course_id)
                course_name = course.course_name if course else ''
            
            self.tree.insert('', 'end', values=(
                s.student_id,
                s.student_name,
                course_name,
                s.phone,
                s.email,
                f"₹{s.total_fees:,.2f}"
            ))
            total_fees += s.total_fees
        
        self.summary_label.config(
            text=f"Total Students: {len(students)} | Total Expected Fees: ₹{total_fees:,.2f}"
        )
    
    def fee_report(self):
        """Generate fee collection report"""
        self.clear_tree()
        self.report_title.config(text="💰 Fee Collection Report")
        
        columns = ('Receipt', 'Student', 'Amount', 'Date', '', '')
        widths = [80, 200, 120, 120, 0, 0]
        
        for i, (col, width) in enumerate(zip(columns, widths)):
            self.tree.heading(self.columns[i], text=col)
            self.tree.column(self.columns[i], width=width, anchor='center')
        
        payments = self.fee_service.get_all_payments()
        total_collected = 0
        
        for p in payments:
            self.tree.insert('', 'end', values=(
                p.receipt_id,
                p.student_name,
                f"₹{p.amount_paid:,.2f}",
                p.payment_date,
                '',
                ''
            ))
            total_collected += p.amount_paid
        
        self.summary_label.config(
            text=f"Total Transactions: {len(payments)} | Total Collected: ₹{total_collected:,.2f}"
        )
    
    def attendance_report(self):
        """Generate attendance report"""
        self.clear_tree()
        self.report_title.config(text="📋 Attendance Statistics")
        
        columns = ('Student', 'Total Days', 'Present', 'Absent', 'Percentage', '')
        widths = [200, 100, 100, 100, 100, 0]
        
        for i, (col, width) in enumerate(zip(columns, widths)):
            self.tree.heading(self.columns[i], text=col)
            self.tree.column(self.columns[i], width=width, anchor='center')
        
        students = self.student_service.get_all_students()
        total_present = 0
        total_absent = 0
        
        for s in students:
            report = self.attendance_service.get_attendance_report(s.student_id)
            if report and report['total_days'] > 0:
                self.tree.insert('', 'end', values=(
                    report['student_name'],
                    report['total_days'],
                    report['present_days'],
                    report['absent_days'],
                    f"{report['percentage']}%",
                    ''
                ))
                total_present += report['present_days']
                total_absent += report['absent_days']
        
        overall = (total_present / (total_present + total_absent) * 100) if (total_present + total_absent) > 0 else 0
        self.summary_label.config(
            text=f"Overall Attendance: {overall:.1f}% | Total Present: {total_present} | Total Absent: {total_absent}"
        )
    
    def course_report(self):
        """Generate course statistics report"""
        self.clear_tree()
        self.report_title.config(text="📖 Course Statistics")
        
        columns = ('ID', 'Course Name', 'Duration', 'Fees', 'Enrolled', '')
        widths = [60, 200, 120, 120, 100, 0]
        
        for i, (col, width) in enumerate(zip(columns, widths)):
            self.tree.heading(self.columns[i], text=col)
            self.tree.column(self.columns[i], width=width, anchor='center')
        
        courses = self.course_service.get_all_courses()
        total_students = 0
        total_revenue = 0
        
        for c in courses:
            students = self.student_service.get_students_by_course(c.course_id)
            count = len(students)
            revenue = count * c.fees
            
            self.tree.insert('', 'end', values=(
                c.course_id,
                c.course_name,
                c.duration,
                f"₹{c.fees:,.2f}",
                count,
                ''
            ))
            total_students += count
            total_revenue += revenue
        
        self.summary_label.config(
            text=f"Total Courses: {len(courses)} | Total Enrollments: {total_students} | Potential Revenue: ₹{total_revenue:,.2f}"
        )
    
    def employee_report(self):
        """Generate employee report"""
        self.clear_tree()
        self.report_title.config(text="👨‍💼 Employee Report")
        
        columns = ('ID', 'Name', 'Department', 'Phone', 'Email', '')
        widths = [60, 180, 120, 120, 180, 0]
        
        for i, (col, width) in enumerate(zip(columns, widths)):
            self.tree.heading(self.columns[i], text=col)
            self.tree.column(self.columns[i], width=width, anchor='center')
        
        employees = self.employee_service.get_all_employees()
        departments = {}
        
        for e in employees:
            self.tree.insert('', 'end', values=(
                e.employee_id,
                e.name,
                e.department,
                e.phone,
                e.email,
                ''
            ))
            
            if e.department:
                departments[e.department] = departments.get(e.department, 0) + 1
        
        dept_str = ' | '.join([f"{k}: {v}" for k, v in departments.items()])
        self.summary_label.config(text=f"Total Employees: {len(employees)} | {dept_str if dept_str else 'No departments'}")