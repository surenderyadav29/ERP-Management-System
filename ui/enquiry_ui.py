"""
Enquiry UI
Enquiry management interface with CRUD operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
from service.enquiry_service import EnquiryService
from model.enquiry import Enquiry


class EnquiryUI:
    """Enquiry management window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.enquiry_service = EnquiryService()
        
        # Create Toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Enquiry Management")
        self.window.geometry("1000x600")
        self.window.configure(bg='#ecf0f1')
        
        # Variables
        self.enquiry_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.reference_var = tk.StringVar()
        self.status_var = tk.StringVar(value='Pending')
        self.search_var = tk.StringVar()
        
        self.selected_enquiry_id = None
        
        # Create UI
        self.create_widgets()
        self.load_enquiries()
    
    def create_widgets(self):
        """Create all widgets"""
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title
        tk.Label(
            main_frame,
            text="📞 Enquiry Management",
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
            text="Enquiry Details",
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        fields = [
            ("Enquiry ID:", self.enquiry_id_var, 'readonly'),
            ("Name *:", self.name_var, 'normal'),
            ("Phone:", self.phone_var, 'normal'),
            ("Course:", self.course_var, 'normal'),
            ("Reference:", self.reference_var, 'normal')
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
        
        # Status dropdown
        status_frame = tk.Frame(left_frame, bg='white')
        status_frame.pack(fill='x', pady=8)
        
        tk.Label(
            status_frame,
            text="Status:",
            font=('Helvetica', 10),
            bg='white',
            fg='#2c3e50',
            width=15,
            anchor='w'
        ).pack(side='left')
        
        status_combo = ttk.Combobox(
            status_frame, 
            textvariable=self.status_var, 
            values=['Pending', 'Contacted', 'Enrolled', 'Not Interested'],
            width=23
        )
        status_combo.pack(side='left', padx=5)
        
        # Buttons
        btn_frame = tk.Frame(left_frame, bg='white')
        btn_frame.pack(fill='x', pady=20)
        
        buttons = [
            ("Add", self.add_enquiry, '#27ae60'),
            ("Update", self.update_enquiry, '#3498db'),
            ("Delete", self.delete_enquiry, '#e74c3c'),
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
        search_entry.bind('<KeyRelease>', lambda e: self.search_enquiries())
        
        tk.Button(
            search_frame,
            text="Refresh",
            font=('Helvetica', 10),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.load_enquiries
        ).pack(side='right')
        
        columns = ('ID', 'Name', 'Phone', 'Course', 'Reference', 'Status')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        widths = [50, 150, 100, 150, 120, 100]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def load_enquiries(self):
        """Load enquiries"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        enquiries = self.enquiry_service.get_all_enquiries()
        
        for enq in enquiries:
            self.tree.insert('', 'end', values=(
                enq.enquiry_id,
                enq.name,
                enq.phone,
                enq.course,
                enq.reference,
                enq.status
            ))
    
    def search_enquiries(self):
        """Search enquiries"""
        keyword = self.search_var.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if keyword:
            enquiries = self.enquiry_service.search_enquiries(keyword)
        else:
            enquiries = self.enquiry_service.get_all_enquiries()
        
        for enq in enquiries:
            self.tree.insert('', 'end', values=(
                enq.enquiry_id,
                enq.name,
                enq.phone,
                enq.course,
                enq.reference,
                enq.status
            ))
    
    def on_select(self, event):
        """Handle selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_enquiry_id = values[0]
            self.enquiry_id_var.set(str(values[0]))
            self.name_var.set(values[1])
            self.phone_var.set(values[2])
            self.course_var.set(values[3])
            self.reference_var.set(values[4])
            self.status_var.set(values[5])
    
    def get_form_data(self):
        """Get form data"""
        return {
            'enquiry_id': self.selected_enquiry_id,
            'name': self.name_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'course': self.course_var.get().strip(),
            'reference': self.reference_var.get().strip(),
            'status': self.status_var.get()
        }
    
    def add_enquiry(self):
        """Add enquiry"""
        data = self.get_form_data()
        success, message = self.enquiry_service.add_enquiry(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_enquiries()
        else:
            messagebox.showerror("Error", message)
    
    def update_enquiry(self):
        """Update enquiry"""
        if not self.selected_enquiry_id:
            messagebox.showwarning("Warning", "Please select an enquiry to update!")
            return
        
        data = self.get_form_data()
        success, message = self.enquiry_service.update_enquiry(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_enquiries()
        else:
            messagebox.showerror("Error", message)
    
    def delete_enquiry(self):
        """Delete enquiry"""
        if not self.selected_enquiry_id:
            messagebox.showwarning("Warning", "Please select an enquiry to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this enquiry?"):
            success, message = self.enquiry_service.delete_enquiry(self.selected_enquiry_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_enquiries()
            else:
                messagebox.showerror("Error", message)
    
    def clear_form(self):
        """Clear form"""
        self.enquiry_id_var.set('')
        self.name_var.set('')
        self.phone_var.set('')
        self.course_var.set('')
        self.reference_var.set('')
        self.status_var.set('Pending')
        self.selected_enquiry_id = None