"""
Dashboard UI
Main dashboard with navigation to all modules
"""

import tkinter as tk
from tkinter import ttk


class DashboardUI:
    """Dashboard window class"""
    
    def __init__(self, root, user, callbacks):
        self.root = root
        self.user = user
        self.callbacks = callbacks
        
        # Configure root window
        self.root.title("ERP Management System - Dashboard")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        self.root.configure(bg='#ecf0f1')
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        """Create dashboard widgets"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="ERP Management System",
            font=('Helvetica', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=20)
        
        # User info
        user_frame = tk.Frame(header_frame, bg='#2c3e50')
        user_frame.pack(side='right', padx=20)
        
        user_label = tk.Label(
            user_frame,
            text=f"Welcome, {self.user.username}",
            font=('Helvetica', 11),
            bg='#2c3e50',
            fg='white'
        )
        user_label.pack(side='left', padx=10)
        
        logout_btn = tk.Button(
            user_frame,
            text="Logout",
            font=('Helvetica', 10),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            cursor='hand2',
            command=self.callbacks.get('logout')
        )
        logout_btn.pack(side='left')
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Module buttons frame
        modules_label = tk.Label(
            main_frame,
            text="Modules",
            font=('Helvetica', 16, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        modules_label.pack(anchor='w', pady=(0, 15))
        
        # Buttons grid
        buttons_frame = tk.Frame(main_frame, bg='#ecf0f1')
        buttons_frame.pack(fill='both', expand=True)
        
        # Module configurations
        modules = [
            ("📚 Students", 'student', '#3498db'),
            ("👨‍💼 Employees", 'employee', '#9b59b6'),
            ("📖 Courses", 'course', '#2ecc71'),
            ("📞 Enquiries", 'enquiry', '#e67e22'),
            ("💰 Fees", 'fee', '#1abc9c'),
            ("📋 Attendance", 'attendance', '#34495e'),
            ("📊 Reports", 'reports', '#e74c3c')
        ]
        
        # Create module buttons in a grid
        for i, (text, module, color) in enumerate(modules):
            row = i // 4
            col = i % 4
            
            btn_frame = tk.Frame(buttons_frame, bg=color, padx=20, pady=20)
            btn_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            btn = tk.Button(
                btn_frame,
                text=text,
                font=('Helvetica', 14, 'bold'),
                bg=color,
                fg='white',
                activebackground=color,
                activeforeground='white',
                cursor='hand2',
                width=15,
                height=4,
                command=lambda m=module: self.open_module(m)
            )
            btn.pack()
            
            buttons_frame.grid_columnconfigure(col, weight=1)
        
        # Quick Stats Frame
        stats_frame = tk.Frame(main_frame, bg='#bdc3c7', padx=20, pady=15)
        stats_frame.pack(fill='x', pady=(20, 0))
        
        stats_label = tk.Label(
            stats_frame,
            text="Quick Statistics",
            font=('Helvetica', 12, 'bold'),
            bg='#bdc3c7',
            fg='#2c3e50'
        )
        stats_label.pack(anchor='w')
        
        # Stats will be loaded dynamically
        self.stats_content = tk.Frame(stats_frame, bg='#bdc3c7')
        self.stats_content.pack(fill='x', pady=(10, 0))
        
        self.load_quick_stats()
    
    def open_module(self, module):
        """Open a module window"""
        callback = self.callbacks.get(module)
        if callback:
            callback()
    
    def load_quick_stats(self):
        """Load quick statistics"""
        # This would normally fetch from database
        stats = [
            ("Total Students", "0"),
            ("Total Courses", "0"),
            ("Total Employees", "0"),
            ("Today's Enquiries", "0")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = tk.Frame(self.stats_content, bg='#bdc3c7')
            stat_frame.pack(side='left', padx=20)
            
            tk.Label(
                stat_frame,
                text=value,
                font=('Helvetica', 18, 'bold'),
                bg='#bdc3c7',
                fg='#2c3e50'
            ).pack()
            
            tk.Label(
                stat_frame,
                text=label,
                font=('Helvetica', 10),
                bg='#bdc3c7',
                fg='#7f8c8d'
            ).pack()