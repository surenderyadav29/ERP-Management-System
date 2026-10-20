"""
Login UI
Login screen for the ERP system
"""

import tkinter as tk
from tkinter import ttk, messagebox
from service.auth_service import AuthService


class LoginUI:
    """Login window class"""
    
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth_service = AuthService()
        
        # Configure root window
        self.root.title("ERP Management System - Login")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Center the window
        self.center_window(500, 400)
        
        # Create UI
        self.create_widgets()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create login widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="ERP Management System",
            font=('Helvetica', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Login to continue",
            font=('Helvetica', 12),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login frame
        login_frame = tk.Frame(main_frame, bg='#34495e', padx=30, pady=30)
        login_frame.pack(fill='x')
        
        # Username
        tk.Label(
            login_frame, 
            text="Username:",
            font=('Helvetica', 11),
            bg='#34495e',
            fg='white'
        ).pack(anchor='w')
        
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(
            login_frame, 
            textvariable=self.username_var,
            font=('Helvetica', 11),
            width=30
        )
        username_entry.pack(fill='x', pady=(5, 15))
        username_entry.focus()
        
        # Password
        tk.Label(
            login_frame, 
            text="Password:",
            font=('Helvetica', 11),
            bg='#34495e',
            fg='white'
        ).pack(anchor='w')
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            login_frame, 
            textvariable=self.password_var,
            font=('Helvetica', 11),
            width=30,
            show='*'
        )
        password_entry.pack(fill='x', pady=(5, 20))
        
        # Login button
        login_btn = tk.Button(
            login_frame,
            text="Login",
            font=('Helvetica', 12, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            cursor='hand2',
            command=self.handle_login
        )
        login_btn.pack(fill='x', ipady=8)
        
        # Bind Enter key
        password_entry.bind('<Return>', lambda e: self.handle_login())
        username_entry.bind('<Return>', lambda e: password_entry.focus())
        
        # Default credentials hint
        hint_label = tk.Label(
            main_frame,
            text="Default: admin / admin123",
            font=('Helvetica', 10),
            bg='#2c3e50',
            fg='#7f8c8d'
        )
        hint_label.pack(pady=(20, 0))
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        success, message, user = self.auth_service.login(username, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", message)
            self.password_var.set("")