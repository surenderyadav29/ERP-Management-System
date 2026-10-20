from tkinter import *
from tkinter import ttk


class AttendanceReportUI:

    def __init__(self):

        self.root = Toplevel()
        self.root.title("Attendance Report")
        self.root.geometry("700x400")

        Label(self.root,text="ATTENDANCE REPORT",
              font=("Arial",16,"bold")).pack(pady=10)

        frame = Frame(self.root)
        frame.pack()

        table = ttk.Treeview(frame,
                             columns=("id","name","date","status"),
                             show="headings")

        table.heading("id",text="Student ID")
        table.heading("name",text="Name")
        table.heading("date",text="Date")
        table.heading("status",text="Status")

        table.pack()

        data = [
            (1,"Rahul","10-03-2026","Present"),
            (2,"Amit","10-03-2026","Absent"),
            (3,"Neha","10-03-2026","Present")
        ]

        for d in data:
            table.insert("",END,values=d)