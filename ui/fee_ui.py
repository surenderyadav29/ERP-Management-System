"""
Fee UI
Fee payment management interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from service.fee_service import FeeService
from service.student_service import StudentService
from model.fee import FeePayment


class FeeUI:
    """Fee payment management window"""
    
    def __init__(self, parent):
        self.parent = parent
        self.fee_service = FeeService()
        self.student_service = StudentService()
        
        # Create Toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("Fee Management")
        self.window.geometry("1000x650")
        self.window.configure(bg='#ecf0f1')
        
        # Variables
        self.receipt_id_var = tk.StringVar()
        self.student_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar(value=str(date.today()))
        self.search_var = tk.StringVar()
        
        self.selected_receipt_id = None
        self.students_dict = {}
        
        # Create UI
        self.create_widgets()
        self.load_students()
        self.load_payments()
    
    def create_widgets(self):
        """Create all widgets"""
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title
        tk.Label(
            main_frame,
            text="💰 Fee Management",
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
            text="Payment Details",
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        fields = [
            ("Receipt ID:", self.receipt_id_var, 'readonly'),
            ("Amount (₹) *:", self.amount_var, 'normal'),
            ("Payment Date:", self.date_var, 'normal')
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
        
        # Student dropdown
        student_frame = tk.Frame(left_frame, bg='white')
        student_frame.pack(fill='x', pady=8)
        
        tk.Label(
            student_frame,
            text="Student *:",
            font=('Helvetica', 10),
            bg='white',
            fg='#2c3e50',
            width=15,
            anchor='w'
        ).pack(side='left')
        
        self.student_combo = ttk.Combobox(
            student_frame, 
            textvariable=self.student_var, 
            width=23
        )
        self.student_combo.pack(side='left', padx=5)
        
        # Payment summary
        summary_frame = tk.Frame(left_frame, bg='#f8f9fa', padx=10, pady=10)
        summary_frame.pack(fill='x', pady=15)
        
        self.summary_label = tk.Label(
            summary_frame,
            text="Select a student to view payment summary",
            font=('Helvetica', 9),
            bg='#f8f9fa',
            fg='#7f8c8d',
            justify='left'
        )
        self.summary_label.pack(anchor='w')
        
        # Bind student selection
        self.student_combo.bind('<<ComboboxSelected>>', self.on_student_select)
        
        # Buttons
        btn_frame = tk.Frame(left_frame, bg='white')
        btn_frame.pack(fill='x', pady=15)
        
        buttons = [
            ("Record", self.record_payment, '#27ae60'),
            ("Update", self.update_payment, '#3498db'),
            ("Delete", self.delete_payment, '#e74c3c'),
            ("Receipt", self.generate_receipt, '#9b59b6'),
            ("Clear", self.clear_form, '#95a5a6')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=text,
                font=('Helvetica', 9),
                bg=color,
                fg='white',
                activebackground=color,
                cursor='hand2',
                width=8,
                command=command
            )
            btn.grid(row=0, column=i, padx=2)
        
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
        
        tk.Button(
            search_frame,
            text="Refresh",
            font=('Helvetica', 10),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.load_payments
        ).pack(side='right')
        
        columns = ('Receipt', 'Student', 'Amount', 'Date')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=22)
        
        widths = [70, 200, 120, 120]
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
            self.students_dict[s.student_id] = {
                'name': s.student_name,
                'total_fees': s.total_fees
            }
    
    def load_payments(self):
        """Load payments"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        payments = self.fee_service.get_all_payments()
        
        for payment in payments:
            self.tree.insert('', 'end', values=(
                payment.receipt_id,
                payment.student_name,
                f"₹{payment.amount_paid:,.2f}",
                payment.payment_date
            ))
    
    def on_student_select(self, event):
        """Handle student selection"""
        student_val = self.student_var.get()
        if student_val and ' - ' in student_val:
            student_id = int(student_val.split(' - ')[0])
            summary = self.fee_service.get_payment_summary(student_id)
            
            if summary:
                summary_text = (
                    f"Student: {summary['student_name']}\n"
                    f"Total Fees: ₹{summary['total_fees']:,.2f}\n"
                    f"Total Paid: ₹{summary['total_paid']:,.2f}\n"
                    f"Balance: ₹{summary['balance']:,.2f}"
                )
                self.summary_label.config(text=summary_text)
    
    def on_select(self, event):
        """Handle selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_receipt_id = values[0]
            self.receipt_id_var.set(str(values[0]))
            
            # Set student
            student_name = values[1]
            for sid, info in self.students_dict.items():
                if info['name'] == student_name:
                    self.student_var.set(f"{sid} - {student_name}")
                    break
            
            # Set amount
            amount_str = values[2].replace('₹', '').replace(',', '')
            self.amount_var.set(amount_str)
            
            self.date_var.set(str(values[3]))
    
    def get_form_data(self):
        """Get form data"""
        student_val = self.student_var.get()
        student_id = None
        if student_val and ' - ' in student_val:
            student_id = int(student_val.split(' - ')[0])
        
        return {
            'receipt_id': self.selected_receipt_id,
            'student_id': student_id,
            'amount_paid': self.amount_var.get().strip(),
            'payment_date': self.date_var.get().strip()
        }
    
    def record_payment(self):
        """Record payment"""
        data = self.get_form_data()
        success, message = self.fee_service.record_payment(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_payments()
        else:
            messagebox.showerror("Error", message)
    
    def update_payment(self):
        """Update payment"""
        if not self.selected_receipt_id:
            messagebox.showwarning("Warning", "Please select a payment to update!")
            return
        
        data = self.get_form_data()
        success, message = self.fee_service.update_payment(data)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_payments()
        else:
            messagebox.showerror("Error", message)
    
    def delete_payment(self):
        """Delete payment"""
        if not self.selected_receipt_id:
            messagebox.showwarning("Warning", "Please select a payment to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this payment record?"):
            success, message = self.fee_service.delete_payment(self.selected_receipt_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.load_payments()
            else:
                messagebox.showerror("Error", message)
    
    def generate_receipt(self):
        """Generate and show receipt"""
        if not self.selected_receipt_id:
            messagebox.showwarning("Warning", "Please select a payment to generate receipt!")
            return
        
        receipt = self.fee_service.generate_receipt(self.selected_receipt_id)
        
        if receipt:
            # Create receipt window
            receipt_window = tk.Toplevel(self.window)
            receipt_window.title(f"Receipt - #{receipt['receipt_id']}")
            receipt_window.geometry("400x350")
            receipt_window.configure(bg='white')
            
            # Receipt content
            frame = tk.Frame(receipt_window, bg='white', padx=30, pady=30)
            frame.pack(fill='both', expand=True)
            
            tk.Label(
                frame,
                text="PAYMENT RECEIPT",
                font=('Helvetica', 16, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(pady=(0, 20))
            
            receipt_text = f"""
Receipt No: {receipt['receipt_id']}
Date: {receipt['payment_date']}

Student ID: {receipt['student_id']}
Student Name: {receipt['student_name']}

Amount Paid: ₹{receipt['amount_paid']:,.2f}
-----------------------------------
Total Fees: ₹{receipt['total_fees']:,.2f}
Total Paid: ₹{receipt['total_paid']:,.2f}
Balance Due: ₹{receipt['balance']:,.2f}

Thank you for your payment!
            """
            
            tk.Label(
                frame,
                text=receipt_text,
                font=('Courier', 10),
                bg='white',
                fg='#2c3e50',
                justify='left'
            ).pack()
        else:
            messagebox.showerror("Error", "Could not generate receipt!")
    
    def clear_form(self):
        """Clear form"""
        self.receipt_id_var.set('')
        self.student_var.set('')
        self.amount_var.set('')
        self.date_var.set(str(date.today()))
        self.selected_receipt_id = None
        self.summary_label.config(text="Select a student to view payment summary")