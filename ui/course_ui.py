"""
Course UI
Course management interface with CRUD operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
from service.course_service import CourseService
from model.course import Course


class CourseUI:
    """Course management window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.course_service = CourseService()
        
        # Create Toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Course Management")
        self.window.geometry("900x550")
        self.window.configure(bg='#ecf0f1')
        
        # Variables
        self.course_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.fees_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        self.selected_course_id = None
        
        # Create UI
        self.create_widgets()
        self.load_courses()
    
    def create_widgets(self):
        """Create all widgets"""
        # Main container
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title
        tk.Label(
            main_frame,
            text="📚 Course Management",
            font=('Helvetica', 18, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Form
        left_frame = tk.Frame(content_frame, bg='white', padx=20, pady=20)
        left_frame.pack(side='left', fill='y', padx=(0, 15))
        
        # Form title
        tk.Label(
            left_frame,
            text="Course Details",
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        # Form fields
        fields = [
            ("Course ID:", self.course_id_var, 'readonly'),
            ("Course Name *:", self.name_var, 'normal'),
            ("Duration *:", self.duration_var, 'normal'),
            ("Fees (₹):", self.fees_var, 'normal')
        ]
        
        for label_text, var, state in fields:
            frame = tk.Frame(left_frame, bg='white')
            frame.pack(fill='x', pady=8)
            
            tk.Label(
                frame,
                text=label_text,
                font=('Helvetica', 10),
                bg='white',
                fg='#2c3e50',
                width=15,
                anchor='w'
            ).pack(side='left')
            
            entry = ttk.Entry(frame, textvariable=var, state=state, width=25)
            entry.pack(side='left', padx=5)
        
        # Buttons
        btn_frame = tk.Frame(left_frame, bg='white')
        btn_frame.pack(fill='x', pady=20)
        
        buttons = [
            ("Add", self.add_course, '#27ae60'),
            ("Update", self.update_course, '#3498db'),
            ("Delete", self.delete_course, '#e74c3c'),
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
        right_frame = tk.Frame(content_frame, bg='white', padx=15, pady=15)
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
        search_entry.bind('<KeyRelease>', lambda e: self.search_courses())
        
        tk.Button(
            search_frame,
            text="Refresh",
            font=('Helvetica', 10),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.load_courses
        ).pack(side='right')
        
        # Treeview
        columns = ('ID', 'Course Name', 'Duration', 'Fees')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=18)
        
        widths = [60, 200, 150, 100]
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
        """Load courses into table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        courses = self.course_service.get_all_courses()
        
        for course in courses:
            self.tree.insert('', 'end', values=(
                course.course_id,
                course.course_name,
                course.duration,
                f"₹{course.fees:,.2f}"
            ))
    
    def search_courses(self):
        """Search courses"""
        keyword = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if keyword:
            courses = self.course_service.search_courses(keyword)
        else:
            courses = self.course_service.get_all_courses()
        
        for course in courses:
            self.tree.insert('', 'end', values=(
                course.course_id,
                course.course_name,
                course.duration,
                f"₹{course.fees:,.2f}"
            ))
    
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_course_id = values[0]
            self.course_id_var.set(str(values[0]))
            self.name_var.set(values[1])
            self.duration_var.set(values[2])
            
            fees_str = values[3].replace('₹', '').replace(',', '')
            self.fees_var.set(fees_str)
    
    def get_form_data(self):
        """Get form data"""
        return {
            'course_id': self.selected_course_id,
            'course_name': self.name_var.get().strip(),
            'duration': self.duration_var.get().strip(),
            'fees': self.fees_var.get().strip() or '0'
        }
    
    def add_course(self):
        """Add new course"""
        data = self.get_form_data()
        success, message = self.course_service.add_course(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_courses()
        else:
            messagebox.showerror("Error", message)
    
    def update_course(self):
        """Update course"""
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Please select a course to update!")
            return
        
        data = self.get_form_data()
        success, message = self.course_service.update_course(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_courses()
        else:
            messagebox.showerror("Error", message)
    
    def delete_course(self):
        """Delete course"""
        if not self.selected_course_id:
            messagebox.showwarning("Warning", "Please select a course to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this course?"):
            success, message = self.course_service.delete_course(self.selected_course_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_courses()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        """Clear form"""
        self.course_id_var.set('')
        self.name_var.set('')
        self.duration_var.set('')
        self.fees_var.set('')
        self.selected_course_id = None