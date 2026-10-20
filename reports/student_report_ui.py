from tkinter import *
from tkinter import ttk


class StudentReportUI:

    def __init__(self):

        self.root = Toplevel()
        self.root.title("Student Report")
        self.root.geometry("700x400")

        Label(self.root,text="STUDENT REPORT",
              font=("Arial",16,"bold")).pack(pady=10)

        frame = Frame(self.root)
        frame.pack()

        table = ttk.Treeview(frame,
                             columns=("id","name","course"),
                             show="headings")

        table.heading("id",text="Student ID")
        table.heading("name",text="Name")
        table.heading("course",text="Course")

        table.pack()

        data = [
            (1,"Rahul","Python"),
            (2,"Amit","Java"),
            (3,"Neha","Data Science")
        ]

        for d in data:
            table.insert("",END,values=d)