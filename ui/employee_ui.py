"""
Employee UI
Employee management interface with CRUD operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
from service.employee_service import EmployeeService
from model.employee import Employee


class EmployeeUI:
    """Employee management window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.employee_service = EmployeeService()
        
        # Create Toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Employee Management")
        self.window.geometry("1000x600")
        self.window.configure(bg='#ecf0f1')
        
        # Variables
        self.employee_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        self.selected_employee_id = None
        
        # Create UI
        self.create_widgets()
        self.load_employees()
    
    def create_widgets(self):
        """Create all widgets"""
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title
        tk.Label(
            main_frame,
            text="👨‍💼 Employee Management",
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
            text="Employee Details",
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        fields = [
            ("Employee ID:", self.employee_id_var, 'readonly'),
            ("Name *:", self.name_var, 'normal'),
            ("Department:", self.department_var, 'normal'),
            ("Phone:", self.phone_var, 'normal'),
            ("Email:", self.email_var, 'normal')
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
            ("Add", self.add_employee, '#27ae60'),
            ("Update", self.update_employee, '#3498db'),
            ("Delete", self.delete_employee, '#e74c3c'),
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
        search_entry.bind('<KeyRelease>', lambda e: self.search_employees())
        
        tk.Button(
            search_frame,
            text="Refresh",
            font=('Helvetica', 10),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.load_employees
        ).pack(side='right')
        
        columns = ('ID', 'Name', 'Department', 'Phone', 'Email')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        widths = [60, 180, 120, 120, 180]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def load_employees(self):
        """Load employees"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        employees = self.employee_service.get_all_employees()
        
        for emp in employees:
            self.tree.insert('', 'end', values=(
                emp.employee_id,
                emp.name,
                emp.department,
                emp.phone,
                emp.email
            ))
    
    def search_employees(self):
        """Search employees"""
        keyword = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if keyword:
            employees = self.employee_service.search_employees(keyword)
        else:
            employees = self.employee_service.get_all_employees()
        
        for emp in employees:
            self.tree.insert('', 'end', values=(
                emp.employee_id,
                emp.name,
                emp.department,
                emp.phone,
                emp.email
            ))
    
    def on_select(self, event):
        """Handle selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_employee_id = values[0]
            self.employee_id_var.set(str(values[0]))
            self.name_var.set(values[1])
            self.department_var.set(values[2])
            self.phone_var.set(values[3])
            self.email_var.set(values[4])
    
    def get_form_data(self):
        """Get form data"""
        return {
            'employee_id': self.selected_employee_id,
            'name': self.name_var.get().strip(),
            'department': self.department_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'email': self.email_var.get().strip()
        }
    
    def add_employee(self):
        """Add employee"""
        data = self.get_form_data()
        success, message = self.employee_service.add_employee(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_employees()
        else:
            messagebox.showerror("Error", message)
    
    def update_employee(self):
        """Update employee"""
        if not self.selected_employee_id:
            messagebox.showwarning("Warning", "Please select an employee to update!")
            return
        
        data = self.get_form_data()
        success, message = self.employee_service.update_employee(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_employees()
        else:
            messagebox.showerror("Error", message)
    
    def delete_employee(self):
        """Delete employee"""
        if not self.selected_employee_id:
            messagebox.showwarning("Warning", "Please select an employee to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            success, message = self.employee_service.delete_employee(self.selected_employee_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_employees()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        """Clear form"""
        self.employee_id_var.set('')
        self.name_var.set('')
        self.department_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.selected_employee_id = None