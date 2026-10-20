from tkinter import *
from tkinter import ttk


class FeeReportUI:

    def __init__(self):

        self.root = Toplevel()
        self.root.title("Fee Report")
        self.root.geometry("700x400")

        Label(self.root,text="FEE REPORT",
              font=("Arial",16,"bold")).pack(pady=10)

        frame = Frame(self.root)
        frame.pack()

        table = ttk.Treeview(frame,
                             columns=("sid","name","amount"),
                             show="headings")

        table.heading("sid",text="Student ID")
        table.heading("name",text="Name")
        table.heading("amount",text="Amount")

        table.pack()

        data = [
            (1,"Rahul",5000),
            (2,"Amit",6000),
            (3,"Neha",8000)
        ]

        for d in data:
            table.insert("",END,values=d)