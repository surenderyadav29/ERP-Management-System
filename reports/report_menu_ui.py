from tkinter import *
from reports.student_report_ui import StudentReportUI
from reports.employee_report_ui import EmployeeReportUI
from reports.fee_report_ui import FeeReportUI
from reports.attendance_report_ui import AttendanceReportUI


class ReportMenuUI:

    def __init__(self):

        self.root = Toplevel()
        self.root.title("Reports")
        self.root.geometry("450x300")

        Label(self.root,
              text="ERP REPORTS",
              font=("Arial",16,"bold")).pack(pady=20)

        frame = Frame(self.root)
        frame.pack(pady=10)

        Button(frame,text="Student Report",width=18,
               command=self.open_student_report).grid(row=0,column=0,padx=10,pady=10)

        Button(frame,text="Employee Report",width=18,
               command=self.open_employee_report).grid(row=0,column=1,padx=10,pady=10)

        Button(frame,text="Fee Report",width=18,
               command=self.open_fee_report).grid(row=1,column=0,padx=10,pady=10)

        Button(frame,text="Attendance Report",width=18,
               command=self.open_attendance_report).grid(row=1,column=1,padx=10,pady=10)

    def open_student_report(self):
        StudentReportUI()

    def open_employee_report(self):
        EmployeeReportUI()

    def open_fee_report(self):
        FeeReportUI()

    def open_attendance_report(self):
        AttendanceReportUI()