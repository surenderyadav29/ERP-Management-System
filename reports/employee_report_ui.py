from tkinter import *
from tkinter import ttk


class EmployeeReportUI:

    def __init__(self):

        self.root = Toplevel()
        self.root.title("Employee Report")
        self.root.geometry("700x400")

        Label(self.root,text="EMPLOYEE REPORT",
              font=("Arial",16,"bold")).pack(pady=10)

        frame = Frame(self.root)
        frame.pack()

        table = ttk.Treeview(frame,
                             columns=("id","name","role"),
                             show="headings")

        table.heading("id",text="Employee ID")
        table.heading("name",text="Name")
        table.heading("role",text="Role")

        table.pack()

        data = [
            (101,"Ravi","Teacher"),
            (102,"Sonia","Admin"),
            (103,"Arjun","Accountant")
        ]

        for d in data:
            table.insert("",END,values=d)