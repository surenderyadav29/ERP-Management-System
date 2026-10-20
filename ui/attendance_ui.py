"""
Attendance UI
Attendance management interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from service.attendance_service import AttendanceService
from service.student_service import StudentService
from model.attendance import Attendance


class AttendanceUI:
    """Attendance management window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.attendance_service = AttendanceService()
        self.student_service = StudentService()
        
        # Create Toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Attendance Management")
        self.window.geometry("1000x650")
        self.window.configure(bg='#ecf0f1')
        
        # Variables
        self.attendance_id_var = tk.StringVar()
        self.student_var = tk.StringVar()
        self.date_var = tk.StringVar(value=str(date.today()))
        self.status_var = tk.StringVar(value='Present')
        self.filter_date_var = tk.StringVar(value=str(date.today()))
        
        self.selected_attendance_id = None
        self.students_dict = {}
        
        # Create UI
        self.create_widgets()
        self.load_students()
        self.load_attendance()
    
    def create_widgets(self):
        """Create all widgets"""
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title
        tk.Label(
            main_frame,
            text="📋 Attendance Management",
            font=('Helvetica', 18, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        content_frame = tk.Frame(main_frame, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Form
        left_frame = tk.Frame(content_frame, bg='white', padx=20, pady=20)
        left_frame.pack(side='left', fill='y', padx=(0, 15))
        
        tk.Label(
            left_frame,
            text="Mark Attendance",
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        # Attendance ID (Read Only)
        frame1 = tk.Frame(left_frame, bg='white')
        frame1.pack(fill='x', pady=8)
        tk.Label(frame1, text="Attendance ID:", font=('Helvetica', 10), bg='white', fg='#2c3e50', width=15, anchor='w').pack(side='left')
        ttk.Entry(frame1, textvariable=self.attendance_id_var, state='readonly', width=25).pack(side='left', padx=5)
        
        # Student Dropdown
        student_frame = tk.Frame(left_frame, bg='white')
        student_frame.pack(fill='x', pady=8)
        tk.Label(student_frame, text="Student *:", font=('Helvetica', 10), bg='white', fg='#2c3e50', width=15, anchor='w').pack(side='left')
        self.student_combo = ttk.Combobox(student_frame, textvariable=self.student_var, width=23)
        self.student_combo.pack(side='left', padx=5)
        
        # Date Entry
        date_frame = tk.Frame(left_frame, bg='white')
        date_frame.pack(fill='x', pady=8)
        tk.Label(date_frame, text="Date *:", font=('Helvetica', 10), bg='white', fg='#2c3e50', width=15, anchor='w').pack(side='left')
        ttk.Entry(date_frame, textvariable=self.date_var, width=25).pack(side='left', padx=5)
        
        # Status Dropdown
        status_frame = tk.Frame(left_frame, bg='white')
        status_frame.pack(fill='x', pady=8)
        tk.Label(status_frame, text="Status:", font=('Helvetica', 10), bg='white', fg='#2c3e50', width=15, anchor='w').pack(side='left')
        ttk.Combobox(status_frame, textvariable=self.status_var, values=['Present', 'Absent'], width=23).pack(side='left', padx=5)
        
        # Stats display
        stats_frame = tk.Frame(left_frame, bg='#f8f9fa', padx=10, pady=10)
        stats_frame.pack(fill='x', pady=15)
        self.stats_label = tk.Label(stats_frame, text="Select a student to view attendance stats", font=('Helvetica', 9), bg='#f8f9fa', fg='#7f8c8d', justify='left')
        self.stats_label.pack(anchor='w')
        
        # Bind student selection
        self.student_combo.bind('<<ComboboxSelected>>', self.on_student_select)
        
        # Buttons
        btn_frame = tk.Frame(left_frame, bg='white')
        btn_frame.pack(fill='x', pady=15)
        
        buttons = [
            ("Mark", self.mark_attendance, '#27ae60'),
            ("Update", self.update_attendance, '#3498db'),
            ("Delete", self.delete_attendance, '#e74c3c'),
            ("Clear", self.clear_form, '#95a5a6')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=('Helvetica', 10), bg=color, fg='white', activebackground=color, cursor='hand2', width=8, command=command).grid(row=0, column=i, padx=3)
        
        # Right panel - Table
        right_frame = tk.Frame(content_frame, bg='white', padx=15, pady=15)
        right_frame.pack(side='left', fill='both', expand=True)
        
        # Filter frame
        filter_frame = tk.Frame(right_frame, bg='white')
        filter_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter by Date:", font=('Helvetica', 10), bg='white', fg='#2c3e50').pack(side='left')
        ttk.Entry(filter_frame, textvariable=self.filter_date_var, width=15).pack(side='left', padx=5)
        tk.Button(filter_frame, text="Apply", font=('Helvetica', 9), bg='#3498db', fg='white', cursor='hand2', command=self.filter_by_date).pack(side='left', padx=5)
        tk.Button(filter_frame, text="All", font=('Helvetica', 9), bg='#95a5a6', fg='white', cursor='hand2', command=self.load_attendance).pack(side='left', padx=5)
        
        # Treeview
        columns = ('ID', 'Student', 'Date', 'Status')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=22)
        
        widths = [60, 200, 120, 100]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def load_students(self):
        """Load students into dropdown"""
        students = self.student_service.get_all_students()
        student_names = [f"{s.student_id} - {s.student_name}" for s in students]
        self.student_combo['values'] = student_names
        
        for s in students:
            self.students_dict[s.student_id] = s.student_name
    
    def load_attendance(self):
        """Load all attendance records"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = self.attendance_service.get_all_attendance()
        
        for record in records:
            self.tree.insert('', 'end', values=(
                record.attendance_id,
                record.student_name,
                record.attendance_date,
                record.status
            ))
    
    def filter_by_date(self):
        """Filter attendance by date"""
        date_str = self.filter_date_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if date_str:
            records = self.attendance_service.get_date_attendance(date_str)
            
            for record in records:
                self.tree.insert('', 'end', values=(
                    record.attendance_id,
                    record.student_name,
                    record.attendance_date,
                    record.status
                ))
    
    def on_student_select(self, event):
        """Handle student selection"""
        student_val = self.student_var.get()
        if student_val and ' - ' in student_val:
            student_id = int(student_val.split(' - ')[0])
            report = self.attendance_service.get_attendance_report(student_id)
            
            if report:
                stats_text = (
                    f"Student: {report['student_name']}\n"
                    f"Total Days: {report['total_days']}\n"
                    f"Present: {report['present_days']}\n"
                    f"Absent: {report['absent_days']}\n"
                    f"Percentage: {report['percentage']}%"
                )
                self.stats_label.config(text=stats_text)
    
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_attendance_id = values[0]
            self.attendance_id_var.set(str(values[0]))
            
            # Set student
            student_name = values[1]
            for sid, name in self.students_dict.items():
                if name == student_name:
                    self.student_var.set(f"{sid} - {student_name}")
                    break
            
            self.date_var.set(str(values[2]))
            self.status_var.set(values[3])
    
    def get_form_data(self):
        """Get form data"""
        student_val = self.student_var.get()
        student_id = None
        if student_val and ' - ' in student_val:
            student_id = int(student_val.split(' - ')[0])
        
        return {
            'attendance_id': self.selected_attendance_id,
            'student_id': student_id,
            'attendance_date': self.date_var.get().strip(),
            'status': self.status_var.get()
        }
    
    def mark_attendance(self):
        """Mark attendance"""
        data = self.get_form_data()
        success, message = self.attendance_service.mark_attendance(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_attendance()
        else:
            messagebox.showerror("Error", message)
    
    def update_attendance(self):
        """Update attendance"""
        if not self.selected_attendance_id:
            messagebox.showwarning("Warning", "Please select a record to update!")
            return
        
        data = self.get_form_data()
        success, message = self.attendance_service.update_attendance(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_attendance()
        else:
            messagebox.showerror("Error", message)
    
    def delete_attendance(self):
        """Delete attendance"""
        if not self.selected_attendance_id:
            messagebox.showwarning("Warning", "Please select a record to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            success, message = self.attendance_service.delete_attendance(self.selected_attendance_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_attendance()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        """Clear form"""
        self.attendance_id_var.set('')
        self.student_var.set('')
        self.date_var.set(str(date.today()))
        self.status_var.set('Present')
        self.selected_attendance_id = None
        self.stats_label.config(text="Select a student to view attendance stats")