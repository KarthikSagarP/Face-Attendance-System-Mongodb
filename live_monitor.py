from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from pymongo import MongoClient
import cv2
import os
import numpy as np
from datetime import datetime
import threading
import time
import csv
from recognition_engine import recognize_faces_from_frame

class Live:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        #========== MongoDB Connection Setup =============
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["face_recognizer"]
            self.collection = self.db["student"]
        except Exception as es:
            messagebox.showerror("Error", f"Could not connect to database: {str(es)}", parent=self.root)
            self.root.destroy()

        #=================variables====================
        self.var_atten_id=StringVar()
        self.var_atten_status=StringVar()
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_dep=StringVar()
        self.var_time=StringVar()
        self.var_date=StringVar()
        self.csv_file_path = None
        self.present_count_dict = {}
        self.total_rounds = 0
        self.current_round = 0
        self.monitoring_active = False

        #first image
        img=Image.open(r"college_images\imgref3_orig.jpg")
        img=img.resize((800,300),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=800,height=200)

        #second image
        img1=Image.open(r"college_images\IMG_1183_augmented_reality_faces1.jpg")
        img1=img1.resize((800,300),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=800,y=0,width=800,height=200)

        #bg image
        img3=Image.open(r"college_images\wp2551980.jpg")
        img3=img3.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=200,width=1530,height=710)

        title_lbl=Label(bg_img,text="LIVE MONITORING SYSTEM",font=('times new roman',35,'bold'),bg='white',fg='blue')
        title_lbl.place(x=0,y=0,width=1530,height=45)

        main_frame=Frame(bg_img,bd=2)
        main_frame.place(x=20,y=50,width=1480,height=600)

        #left label frame
        Left_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text='Current Class Details',font=('times new roman',12,'bold'))
        Left_frame.place(x=10,y=10,width=730,height=580)

        img_left=Image.open(r"college_images\teaser.png")
        img_left=img_left.resize((720,250),Image.Resampling.LANCZOS)
        self.photoimg_left=ImageTk.PhotoImage(img_left)

        f_lbl=Label(Left_frame,image=self.photoimg_left)
        f_lbl.place(x=5,y=0,width=720,height=130)

        left_inside_frame=Frame(Left_frame,bd=2,relief=RIDGE,bg="white")
        left_inside_frame.place(x=0,y=135,width=720,height=370)

        # ====== CLASS DETAILS ======
        subject_label = Label(left_inside_frame, text="Subject:", bg="white", font=('times new roman', 13, 'bold'))
        subject_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_subject = StringVar()
        subject_entry = ttk.Entry(left_inside_frame, textvariable=self.var_subject, width=20, font=('times new roman', 13, 'bold'))
        subject_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        faculty_label = Label(left_inside_frame, text="Faculty Name:", bg="white", font=('times new roman', 13, 'bold'))
        faculty_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        self.var_faculty = StringVar()
        faculty_entry = ttk.Entry(left_inside_frame, textvariable=self.var_faculty, width=20, font=('times new roman', 13, 'bold'))
        faculty_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        division_label = Label(left_inside_frame, text="Section:", bg="white", font=('times new roman', 13, 'bold'))
        division_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        self.var_division = StringVar()
        division_combo = ttk.Combobox(left_inside_frame, textvariable=self.var_division, font=('times new roman', 12, 'bold'), state="readonly", width=18)
        division_combo["values"] = ("Select", "A", "B", "C", "D", "E")
        division_combo.current(0)
        division_combo.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        duration_label = Label(left_inside_frame, text="Class Duration (min):", bg="white", font=('times new roman', 13, 'bold'))
        duration_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        self.var_duration = StringVar(value="45")
        duration_entry = ttk.Entry(left_inside_frame, textvariable=self.var_duration, width=20, font=('times new roman', 13, 'bold'))
        duration_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        interval_label = Label(left_inside_frame, text="Interval (min):", bg="white", font=('times new roman', 13, 'bold'))
        interval_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        self.var_interval = StringVar(value="5")
        interval_entry = ttk.Entry(left_inside_frame, textvariable=self.var_interval, width=20, font=('times new roman', 13, 'bold'))
        interval_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        date_label = Label(left_inside_frame, text="Date:", bg="white", font=('times new roman', 13, 'bold'))
        date_label.grid(row=5, column=0, padx=10, pady=5, sticky=W)

        self.var_class_date = StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        date_entry = ttk.Entry(left_inside_frame, textvariable=self.var_class_date, font=('times new roman', 13, 'bold'), width=20, state='readonly')
        date_entry.grid(row=5, column=1, padx=10, pady=5, sticky=W)

        # ========== Buttons ==========
        start_btn = Button(left_inside_frame, text="Start Monitoring",command=self.start_monitoring, width=20, font=('times new roman', 13, 'bold'), bg="green", fg="white")
        start_btn.grid(row=6, column=0, padx=10, pady=15)

        stop_btn = Button(left_inside_frame, text="Stop Monitoring",command=self.stop_monitoring, width=20, font=('times new roman', 13, 'bold'), bg="red", fg="white")
        stop_btn.grid(row=6, column=1, padx=10, pady=15)

        # ========== RIGHT FRAME for TreeView ==========
        Right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text='Live Attendance Tracker', font=('times new roman', 12, 'bold'))
        Right_frame.place(x=750, y=10, width=700, height=580)

        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=5, width=680, height=540)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.liveAttendanceTable = ttk.Treeview(
            table_frame,
            columns=("id", "name", "department", "count", "status"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.liveAttendanceTable.xview)
        scroll_y.config(command=self.liveAttendanceTable.yview)

        self.liveAttendanceTable.heading("id", text="Student ID")
        self.liveAttendanceTable.heading("name", text="Name")
        self.liveAttendanceTable.heading("department", text="Department")
        self.liveAttendanceTable.heading("count", text="Rounds Present")
        self.liveAttendanceTable.heading("status", text="Status")

        self.liveAttendanceTable["show"] = "headings"
        self.liveAttendanceTable.column("id", width=100)
        self.liveAttendanceTable.column("name", width=150)
        self.liveAttendanceTable.column("department", width=120)
        self.liveAttendanceTable.column("count", width=100)
        self.liveAttendanceTable.column("status", width=100)

        self.liveAttendanceTable.pack(fill=BOTH, expand=1)

        # Set the protocol for the window close button
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_monitoring(self):
        try:
            duration = int(self.var_duration.get())
            interval = int(self.var_interval.get())
            if interval == 0:
                messagebox.showerror("Error", "Interval cannot be zero.")
                return
            self.total_rounds = duration // interval
            if self.total_rounds == 0:
                 messagebox.showwarning("Warning", "Duration is less than interval. Monitoring will not run.")
                 return
            self.current_round = 0
            self.present_count_dict = {}
            self.monitoring_active = True

            messagebox.showinfo("Monitoring Started", f"Monitoring will run for {self.total_rounds} rounds.")

            monitoring_thread = threading.Thread(target=self.run_monitoring_loop, args=(interval,))
            monitoring_thread.daemon = True
            monitoring_thread.start()
        except ValueError:
            messagebox.showerror("Error", "Invalid duration or interval value. Please enter numbers.")

    def stop_monitoring(self):
        self.monitoring_active = False

    def detect_faces_once(self):
        return recognize_faces_from_frame()

    def run_monitoring_loop(self, interval):
        while self.current_round < self.total_rounds and self.monitoring_active:
            print(f"[INFO] Round {self.current_round + 1} of {self.total_rounds}")

            recognized_ids = self.detect_faces_once()

            for sid in recognized_ids:
                self.present_count_dict[sid] = self.present_count_dict.get(sid, 0) + 1

            self.current_round += 1
            self.root.after(0, self.update_treeview)

            # Wait for the next interval, checking frequently if we need to stop
            for _ in range(interval * 60):
                if not self.monitoring_active:
                    break
                time.sleep(1)

        if self.monitoring_active:
            self.root.after(0, self.finalize_attendance)
        else:
            self.root.after(0, lambda: messagebox.showinfo("Monitoring Stopped", "Live monitoring was stopped by the user."))

    def update_treeview(self):
        if not self.monitoring_active: # Don't update if monitoring has stopped
            return
            
        self.liveAttendanceTable.delete(*self.liveAttendanceTable.get_children())

        if not self.present_count_dict:
            return

        student_ids_as_numbers = list(self.present_count_dict.keys())
        student_ids_as_strings = [str(sid) for sid in student_ids_as_numbers]

        try:
            student_records = self.collection.find({"Student_id": {"$in": student_ids_as_strings}})
            student_details = {record["Student_id"]: record for record in student_records}

            for sid, count in self.present_count_dict.items():
                student_doc = student_details.get(str(sid))

                if student_doc:
                    name = student_doc.get("Name", "N/A")
                    dept = student_doc.get("Department", "N/A")
                else:
                    name, dept = "Unknown", "Unknown"

                status = "Present" if count >= (self.total_rounds / 2) else "Review"
                self.liveAttendanceTable.insert("", "end", values=(sid, name, dept, f"{count}/{self.current_round}", status))

        except Exception as es:
            messagebox.showerror("Database Error", f"Could not fetch student details: {es}")

    def finalize_attendance(self):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time_now = now.strftime("%H:%M:%S")

        subject = self.var_subject.get() or "UnknownSubject"
        division = self.var_division.get() or "UnknownDiv"
        filename = f"{date}_{subject}_{division}_attendance.csv"

        if not os.path.exists("attendance_records"):
            os.makedirs("attendance_records")
        csv_path = os.path.join("attendance_records", filename)

        try:
            with open(csv_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Student_ID", "Name", "Department", "Section", "Time", "Date", "Final_Status", "Rounds_Present", "Total_Rounds"])

                if not self.present_count_dict:
                    self.reset_session()
                    return

                student_ids_as_numbers = list(self.present_count_dict.keys())
                student_ids_as_strings = [str(sid) for sid in student_ids_as_numbers]
                student_records = self.collection.find({"Student_id": {"$in": student_ids_as_strings}})
                student_details = {record["Student_id"]: record for record in student_records}

                for sid, count in self.present_count_dict.items():
                    student_doc = student_details.get(str(sid))
                    if student_doc:
                        name, dept = student_doc.get("Name", "N/A"), student_doc.get("Department", "N/A")
                    else:
                        name, dept = "Unknown", "Unknown"

                    status = "Present" if count >= (self.total_rounds / 2) else "Absent"
                    writer.writerow([sid, name, dept, self.var_division.get(), time_now, date, status, count, self.total_rounds])

            messagebox.showinfo("Session Complete", f"Attendance has been recorded successfully in:\n{csv_path}")

        except Exception as es:
            messagebox.showerror("File Error", f"Could not save attendance file: {es}")

        finally:
            self.reset_session()

    def reset_session(self):
        self.present_count_dict = {}
        self.current_round = 0
        self.total_rounds = 0
        self.monitoring_active = False

        self.var_subject.set("")
        self.var_faculty.set("")
        self.var_division.set("Select")
        self.var_duration.set("45")
        self.var_interval.set("5")
        self.var_class_date.set(datetime.now().strftime("%d/%m/%Y"))

        self.liveAttendanceTable.delete(*self.liveAttendanceTable.get_children())

    def on_closing(self):
        """Handles the window closing event."""
        print("Closing window, stopping monitoring...")
        self.stop_monitoring()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj=Live(root)
    root.mainloop()