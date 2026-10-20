"""
Student UI
Student management interface with CRUD operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
from service.student_service import StudentService
from service.course_service import CourseService
from model.student import Student


class StudentUI:
    """Student management window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.student_service = StudentService()
        self.course_service = CourseService()
        
        # Create Toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Student Management")
        self.window.geometry("1100x600")
        self.window.configure(bg='#ecf0f1')
        
        # Variables
        self.student_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.fees_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        self.selected_student_id = None
        self.courses_dict = {}
        
        # Create UI
        self.create_widgets()
        self.load_courses()
        self.load_students()
    
    def create_widgets(self):
        """Create all widgets"""
        # Main container
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Form
        left_frame = tk.Frame(main_frame, bg='white', padx=15, pady=15)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Form title
        tk.Label(
            left_frame,
            text="Student Form",
            font=('Helvetica', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        # Form fields
        fields = [
            ("Student ID:", self.student_id_var, 'readonly'),
            ("Name *:", self.name_var, 'normal'),
            ("Phone:", self.phone_var, 'normal'),
            ("Email:", self.email_var, 'normal'),
            ("Total Fees:", self.fees_var, 'normal')
        ]
        
        for label_text, var, state in fields:
            frame = tk.Frame(left_frame, bg='white')
            frame.pack(fill='x', pady=5)
            
            tk.Label(
                frame,
                text=label_text,
                font=('Helvetica', 10),
                bg='white',
                fg='#2c3e50',
                width=12,
                anchor='w'
            ).pack(side='left')
            
            entry = ttk.Entry(frame, textvariable=var, state=state, width=25)
            entry.pack(side='left', padx=5)
        
        # Course dropdown
        course_frame = tk.Frame(left_frame, bg='white')
        course_frame.pack(fill='x', pady=5)
        
        tk.Label(
            course_frame,
            text="Course:",
            font=('Helvetica', 10),
            bg='white',
            fg='#2c3e50',
            width=12,
            anchor='w'
        ).pack(side='left')
        
        self.course_combo = ttk.Combobox(course_frame, textvariable=self.course_var, width=23)
        self.course_combo.pack(side='left', padx=5)
        
        # Buttons
        btn_frame = tk.Frame(left_frame, bg='white')
        btn_frame.pack(fill='x', pady=20)
        
        buttons = [
            ("Add", self.add_student, '#27ae60'),
            ("Update", self.update_student, '#3498db'),
            ("Delete", self.delete_student, '#e74c3c'),
            ("Clear", self.clear_form, '#95a5a6')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=text,
                font=('Helvetica', 10),
                bg=color,
                fg='white',
                activebackground=color,
                cursor='hand2',
                width=8,
                command=command
            )
            btn.grid(row=0, column=i, padx=3)
        
        # Right panel - Table
        right_frame = tk.Frame(main_frame, bg='white', padx=15, pady=15)
        right_frame.pack(side='left', fill='both', expand=True)
        
        # Search bar
        search_frame = tk.Frame(right_frame, bg='white')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="Search:",
            font=('Helvetica', 10),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.search_students())
        
        tk.Button(
            search_frame,
            text="Refresh",
            font=('Helvetica', 10),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.load_students
        ).pack(side='right')
        
        # Treeview
        columns = ('ID', 'Name', 'Course', 'Phone', 'Email', 'Fees')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        widths = [60, 150, 150, 100, 180, 80]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def load_courses(self):
        """Load courses into dropdown"""
        courses = self.course_service.get_course_list()
        course_names = [''] + [f"{c['course_id']} - {c['course_name']}" for c in courses]
        self.course_combo['values'] = course_names
        
        # Create mapping
        for c in courses:
            self.courses_dict[c['course_id']] = c['course_name']
    
    def load_students(self):
        """Load students into table"""
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load students
        students = self.student_service.get_all_students()
        
        for student in students:
            course_name = self.courses_dict.get(student.course_id, '')
            self.tree.insert('', 'end', values=(
                student.student_id,
                student.student_name,
                course_name,
                student.phone,
                student.email,
                f"₹{student.total_fees:,.2f}"
            ))
    
    def search_students(self):
        """Search students"""
        keyword = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if keyword:
            students = self.student_service.search_students(keyword)
        else:
            students = self.student_service.get_all_students()
        
        for student in students:
            course_name = self.courses_dict.get(student.course_id, '')
            self.tree.insert('', 'end', values=(
                student.student_id,
                student.student_name,
                course_name,
                student.phone,
                student.email,
                f"₹{student.total_fees:,.2f}"
            ))
    
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_student_id = values[0]
            self.student_id_var.set(str(values[0]))
            self.name_var.set(values[1])
            self.phone_var.set(values[3])
            self.email_var.set(values[4])
            
            # Extract fees
            fees_str = values[5].replace('₹', '').replace(',', '')
            self.fees_var.set(fees_str)
            
            # Set course
            course_name = values[2]
            for key, value in self.courses_dict.items():
                if value == course_name:
                    self.course_var.set(f"{key} - {course_name}")
                    break
    
    def get_form_data(self):
        """Get form data as dictionary"""
        course_val = self.course_var.get()
        course_id = None
        if course_val and ' - ' in course_val:
            course_id = int(course_val.split(' - ')[0])
        
        return {
            'student_id': self.selected_student_id,
            'student_name': self.name_var.get().strip(),
            'course_id': course_id,
            'phone': self.phone_var.get().strip(),
            'email': self.email_var.get().strip(),
            'total_fees': self.fees_var.get().strip() or '0'
        }
    
    def add_student(self):
        """Add new student"""
        data = self.get_form_data()
        success, message = self.student_service.add_student(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Error", message)
    
    def update_student(self):
        """Update student"""
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Please select a student to update!")
            return
        
        data = self.get_form_data()
        success, message = self.student_service.update_student(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Error", message)
    
    def delete_student(self):
        """Delete student"""
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            success, message = self.student_service.delete_student(self.selected_student_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_students()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        """Clear form fields"""
        self.student_id_var.set('')
        self.name_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.fees_var.set('')
        self.course_var.set('')
        self.selected_student_id = None