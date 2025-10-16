from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from pymongo import MongoClient  # Replaced mysql.connector with pymongo
import cv2
import os

class Student:
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
            self.root.destroy() # Close the app if DB connection fails


        #==========variables=============
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()
        self.var_searchBy = StringVar()
        self.var_searchText = StringVar()



        #first image
        img=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\face-recognition.png")
        img=img.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)

        #second image
        img1=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\smart-attendance.jpg")
        img1=img1.resize((500,130),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=500,y=0,width=500,height=130)

        #third image
        img2=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\iStock-182059956_18390_t12.jpg")
        img2=img2.resize((550,130),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        f_lbl=Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1000,y=0,width=550,height=130)

        #bg image
        img3=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\wp2551980.jpg")
        img3=img3.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)

        title_lbl=Label(bg_img,text="STUDENT MANAGEMENT SYSTEM",font=('times new roman',35,'bold'),bg='white',fg='darkgreen')
        title_lbl.place(x=0,y=0,width=1530,height=45)

        main_frame=Frame(bg_img,bd=2)
        main_frame.place(x=20,y=50,width=1480,height=600)

        #left label frame
        Left_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text='Student Details',font=('times new roman',12,'bold'))
        Left_frame.place(x=10,y=10,width=730,height=580)

        img_left=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\AdobeStock_303989091.jpeg")
        img_left=img_left.resize((720,130),Image.Resampling.LANCZOS)
        self.photoimg_left=ImageTk.PhotoImage(img_left)

        f_lbl=Label(Left_frame,image=self.photoimg_left)
        f_lbl.place(x=5,y=0,width=720,height=130)


        #current course
        current_course_frame=LabelFrame(Left_frame,bd=2,relief=RIDGE,text='Current Course Info',font=('times new roman',12,'bold'))
        current_course_frame.place(x=5,y=135,width=720,height=115)

        #Department
        dep_label=Label(current_course_frame,text="Department",font=('times new roman',12,'bold'))
        dep_label.grid(row=0,column=0,padx=10)

        dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_dep,font=('times new roman',12,'bold'),width=17,state="readonly")
        dep_combo["values"]=("Select Department","Comp Sci","Mechanical","Civil","IT")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        #COURSe
        course_label=Label(current_course_frame,text="Course",font=('times new roman',12,'bold'))
        course_label.grid(row=0,column=2,padx=10,sticky=W)

        course_combo=ttk.Combobox(current_course_frame,textvariable=self.var_course,font=('times new roman',12,'bold'),width=17,state="readonly")
        course_combo["values"]=("Select Course","FE","SE","TE","BE")
        course_combo.current(0)
        course_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)

        #year
        year_label=Label(current_course_frame,text="Year",font=('times new roman',13,'bold'))
        year_label.grid(row=1,column=0,padx=10,sticky=W)

        year_combo=ttk.Combobox(current_course_frame,textvariable=self.var_year,font=('times new roman',13,'bold'),width=17,state="readonly")
        year_combo["values"]=("Select year","2020-21","2021-22","2022-23","2023-24")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)

        #semester
        semester_label=Label(current_course_frame,text="Semester",font=('times new roman',13,'bold'))
        semester_label.grid(row=1,column=2,padx=10,sticky=W)

        semester_combo=ttk.Combobox(current_course_frame,textvariable=self.var_semester,font=('times new roman',13,'bold'),width=17,state="readonly")
        semester_combo["values"]=("Select semester","Sem-1","Sem-2")
        semester_combo.current(0)
        semester_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)

        # Class student info
        class_Student_frame=LabelFrame(Left_frame,bd=2,relief=RIDGE,text='Current Student Info',font=('times new roman',12,'bold'))
        class_Student_frame.place(x=5,y=250,width=720,height=300)
        

        #studentID
        studentID_label=Label(class_Student_frame,text="StudentID:",font=('times new roman',13,'bold'))
        studentID_label.grid(row=0,column=0,padx=10,sticky=W)

        studentID_entry=ttk.Entry(class_Student_frame,textvariable=self.var_std_id,width=20,font=('times new roman',13,'bold'))        
        studentID_entry.grid(row=0,column=1,padx=10,sticky=W)

        #student name
        studentName_label=Label(class_Student_frame,text="Student name:",font=('times new roman',13,'bold'))
        studentName_label.grid(row=0,column=2,padx=10,sticky=W)

        studentName_entry=ttk.Entry(class_Student_frame,textvariable=self.var_std_name,width=20,font=('times new roman',13,'bold'))        
        studentName_entry.grid(row=0,column=3,padx=10,sticky=W)

        #class division
        class_div_label=Label(class_Student_frame,text="Class Division:",font=('times new roman',13,'bold'))
        class_div_label.grid(row=1,column=0,padx=10,pady=5,sticky=W)

        div_combo=ttk.Combobox(class_Student_frame,textvariable=self.var_div,font=('times new roman',13,'bold'),width=18,state="readonly")
        div_combo["values"]=("A","B","C")
        div_combo.current(0)
        div_combo.grid(row=1,column=1,padx=10,pady=10,sticky=W)

        #roll no
        roll_no_label=Label(class_Student_frame,text="Roll No:",font=('times new roman',13,'bold'))
        roll_no_label.grid(row=1,column=2,padx=10,pady=5,sticky=W)

        roll_no_entry=ttk.Entry(class_Student_frame,textvariable=self.var_roll,width=20,font=('times new roman',13,'bold'))        
        roll_no_entry.grid(row=1,column=3,padx=10,pady=5,sticky=W)

        #gender
        gender_label=Label(class_Student_frame,text="Gender:",font=('times new roman',13,'bold'))
        gender_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)

        gender_combo=ttk.Combobox(class_Student_frame,textvariable=self.var_gender,font=('times new roman',13,'bold'),width=18,state="readonly")
        gender_combo["values"]=("Male","Female","Other")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=10,pady=5,sticky=W)

        #DOB
        dob_label=Label(class_Student_frame,text="DoB:",font=('times new roman',13,'bold'))
        dob_label.grid(row=2,column=2,padx=10,pady=5,sticky=W)

        dob_entry=ttk.Entry(class_Student_frame,textvariable=self.var_dob,width=20,font=('times new roman',13,'bold'))        
        dob_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)

        #email
        email_label=Label(class_Student_frame,text="Email:",font=('times new roman',13,'bold'))
        email_label.grid(row=3,column=0,padx=10,pady=5,sticky=W)

        email_entry=ttk.Entry(class_Student_frame,textvariable=self.var_email,width=20,font=('times new roman',13,'bold'))        
        email_entry.grid(row=3,column=1,padx=10,pady=5,sticky=W)

        #phone no
        phone_label=Label(class_Student_frame,text="Phone No:",font=('times new roman',13,'bold'))
        phone_label.grid(row=3,column=2,padx=10,pady=5,sticky=W)

        phone_entry=ttk.Entry(class_Student_frame,textvariable=self.var_phone,width=20,font=('times new roman',13,'bold'))        
        phone_entry.grid(row=3,column=3,padx=10,pady=5,sticky=W)

        #address
        address_label=Label(class_Student_frame,text="Address:",font=('times new roman',13,'bold'))
        address_label.grid(row=4,column=0,padx=10,pady=5,sticky=W)

        address_entry=ttk.Entry(class_Student_frame,textvariable=self.var_address,width=20,font=('times new roman',13,'bold'))        
        address_entry.grid(row=4,column=1,padx=10,pady=5,sticky=W)

        #teacher name
        teacher_label=Label(class_Student_frame,text="Teacher:",font=('times new roman',13,'bold'))
        teacher_label.grid(row=4,column=2,padx=10,pady=5,sticky=W)

        teacher_entry=ttk.Entry(class_Student_frame,textvariable=self.var_teacher,width=20,font=('times new roman',13,'bold'))        
        teacher_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)

        #radio button
        self.var_radio1=StringVar()
        radiobtn1=ttk.Radiobutton(class_Student_frame,variable=self.var_radio1,text="Take photo sameple",value="YES")
        radiobtn1.grid(row=6,column=0)

        radiobtn2=ttk.Radiobutton(class_Student_frame,variable=self.var_radio1,text="No photo sameple",value="NO")
        radiobtn2.grid(row=6,column=1)

        #buttons frame
        btn_frame=Frame(class_Student_frame,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=200,width=715,height=35)

        save_btn=Button(btn_frame,text="Save",command=self.add_data,width=17,font=('times new roman',13,'bold'),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        update_btn=Button(btn_frame,text="Update",command=self.update_data,width=17,font=('times new roman',13,'bold'),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)

        delete_btn=Button(btn_frame,text="Delete",command=self.delete_data,width=17,font=('times new roman',13,'bold'),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)

        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,width=17,font=('times new roman',13,'bold'),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)

        btn_frame1=Frame(class_Student_frame,bd=2,relief=RIDGE)
        btn_frame1.place(x=0,y=230,width=715,height=35)

        take_photo_btn=Button(btn_frame1,text="Take a photo",command=self.generate_dataset,width=35,font=('times new roman',13,'bold'),bg="blue",fg="white")
        take_photo_btn.grid(row=0,column=0)

        update_photo_btn=Button(btn_frame1, text="Update photo", command=self.update_photos, width=35, font=('times new roman',13,'bold'), bg="blue", fg="white")
        update_photo_btn.grid(row=0,column=1)


        #right label frame
        Right_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text='Student Details',font=('times new roman',12,'bold'))
        Right_frame.place(x=780,y=10,width=660,height=580)

        img_right=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\gettyimages-1022573162.jpg")
        img_right=img_right.resize((720,130),Image.Resampling.LANCZOS)
        self.photoimg_right=ImageTk.PhotoImage(img_right)

        f_lbl=Label(Right_frame,image=self.photoimg_right)
        f_lbl.place(x=5,y=0,width=720,height=130)

        #search system
        Search_frame=LabelFrame(Right_frame,bd=2,relief=RIDGE,text='Search System',font=('times new roman',12,'bold'))
        Search_frame.place(x=5,y=135,width=650,height=70)

        search_label=Label(Search_frame,text="Search By:",font=('times new roman',13,'bold'),bg="red",fg="white")
        search_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        self.search_combo=ttk.Combobox(Search_frame,font=('times new roman',12,'bold'),width=15,state="readonly")
        self.search_combo["values"]=("Select","Roll No.","Department")
        self.search_combo.current(0)
        self.search_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        self.search_entry=ttk.Entry(Search_frame,width=15,font=('times new roman',12,'bold'))        
        self.search_entry.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        search_btn=Button(Search_frame,text="Search",width=12,command=self.search_data,font=('times new roman',12,'bold'),bg="blue",fg="white")
        search_btn.grid(row=0,column=3,padx=4)

        showAll_btn=Button(Search_frame,text="Show All",width=12, command=self.show_all,font=('times new roman',12,'bold'),bg="blue",fg="white")
        showAll_btn.grid(row=0,column=4,padx=4)

        #table Frame
        table_frame=Frame(Right_frame,bd=2,relief=RIDGE)
        table_frame.place(x=5,y=210,width=650,height=345)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,columns=("dep","course","year","sem","id","name","div","roll","gender","dob","email","phone","address","teacher","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep",text="Department")
        self.student_table.heading("course",text="Course")
        self.student_table.heading("year",text="Year")
        self.student_table.heading("sem",text="Semester")
        self.student_table.heading("id",text="StudentId")
        self.student_table.heading("name",text="Name")
        self.student_table.heading("div",text="Division")
        self.student_table.heading("roll",text="Roll No.")
        self.student_table.heading("gender",text="Gender")
        self.student_table.heading("dob",text="DOB")
        self.student_table.heading("email",text="Email")
        self.student_table.heading("phone",text="Phone")
        self.student_table.heading("address",text="Address")
        self.student_table.heading("teacher",text="Teacher")
        self.student_table.heading("photo",text="PhotoSampleStatus")
        self.student_table["show"]="headings"

        self.student_table.column("dep",width=100)
        self.student_table.column("course",width=100)
        self.student_table.column("year",width=100)
        self.student_table.column("sem",width=100)
        self.student_table.column("id",width=100)
        self.student_table.column("name",width=100)
        self.student_table.column("div",width=100)
        self.student_table.column("roll",width=100)
        self.student_table.column("gender",width=100)
        self.student_table.column("dob",width=100)
        self.student_table.column("email",width=100)
        self.student_table.column("phone",width=100)
        self.student_table.column("address",width=100)
        self.student_table.column("teacher",width=100)
        self.student_table.column("photo",width=150)


        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()

    #function declaration=====================
    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root) 
        else:
            try:
                # Check if Student ID already exists
                if self.collection.find_one({"Student_id": self.var_std_id.get()}):
                    messagebox.showerror("Error", "This Student ID already exists", parent=self.root)
                    return

                student_data = {
                    "Department": self.var_dep.get(),
                    "Course": self.var_course.get(),
                    "Year": self.var_year.get(),
                    "Semester": self.var_semester.get(),
                    "Student_id": self.var_std_id.get(),
                    "Name": self.var_std_name.get(),
                    "Division": self.var_div.get(),
                    "Roll": self.var_roll.get(),
                    "Gender": self.var_gender.get(),
                    "Dob": self.var_dob.get(),
                    "Email": self.var_email.get(),
                    "Phone": self.var_phone.get(),
                    "Address": self.var_address.get(),
                    "Teacher": self.var_teacher.get(),
                    "PhotoSample": self.var_radio1.get()
                }
                self.collection.insert_one(student_data)
                self.fetch_data()
                messagebox.showinfo("Success","Student details has been added Successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}",parent=self.root)
    
    #=============fetch data============
    def fetch_data(self):
        try:
            data = list(self.collection.find())
            if len(data) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for doc in data:
                    values_tuple = (
                        doc.get("Department", ""), doc.get("Course", ""), doc.get("Year", ""),
                        doc.get("Semester", ""), doc.get("Student_id", ""), doc.get("Name", ""),
                        doc.get("Division", ""), doc.get("Roll", ""), doc.get("Gender", ""),
                        doc.get("Dob", ""), doc.get("Email", ""), doc.get("Phone", ""),
                        doc.get("Address", ""), doc.get("Teacher", ""), doc.get("PhotoSample", "")
                    )
                    self.student_table.insert("", END, values=values_tuple)
        except Exception as es:
            messagebox.showerror("Error", f"Error fetching data: {str(es)}", parent=self.root)


    #==================get cursor===============
    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content.get("values", [])

        if not data:
            return

        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_semester.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_div.set(data[6])
        self.var_roll.set(data[7])
        self.var_gender.set(data[8])
        self.var_dob.set(data[9])
        self.var_email.set(data[10])
        self.var_phone.set(data[11])
        self.var_address.set(data[12])
        self.var_teacher.set(data[13])
        self.var_radio1.set(data[14])
        
    #================update function=============
    def update_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root) 
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update this student details",parent=self.root)
                if Update>0:
                    update_dict = {
                        "Department": self.var_dep.get(), "Course": self.var_course.get(),
                        "Year": self.var_year.get(), "Semester": self.var_semester.get(),
                        "Name": self.var_std_name.get(), "Division": self.var_div.get(),
                        "Dob": self.var_dob.get(), "Roll": self.var_roll.get(),
                        "Gender": self.var_gender.get(), "Email": self.var_email.get(),
                        "Phone": self.var_phone.get(), "Address": self.var_address.get(),
                        "Teacher": self.var_teacher.get(), "PhotoSample": self.var_radio1.get()
                    }
                    self.collection.update_one(
                        {"Student_id": self.var_std_id.get()},
                        {"$set": update_dict}
                    )
                    messagebox.showinfo("Success","Student details successfully update completed",parent=self.root)
                    self.fetch_data()
                else:
                    return
            except Exception as es:
                messagebox.showerror("Error",f"Error:{str(es)}",parent=self.root)
    

    #delete function        
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Error","Student id is required",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Student Delete Page","Do you want to delete this student?",parent=self.root)
                if delete>0:
                    result = self.collection.delete_one({"Student_id": self.var_std_id.get()})
                    if result.deleted_count > 0:
                         messagebox.showinfo("Delete","Student details successfully deleted",parent=self.root)
                    else:
                        messagebox.showwarning("Warning", "No student found with that ID", parent=self.root)
                    self.fetch_data()
                    self.reset_data()
            except Exception as es:
                messagebox.showerror("Error",f"Due to:{str(es)}",parent=self.root)

        #==============reset function==========
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("A")
        self.var_roll.set("")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")

    #=====================search function=====================
    def search_data(self):
        search_by = self.search_combo.get()
        search_value = self.search_entry.get()

        if search_by == "Select" or search_value == "":
            messagebox.showerror("Error", "Please select a search category and enter a value", parent=self.root)
            return

        try:
            query = {}
            if search_by == "Roll No.":
                query = {"Roll": search_value}
            elif search_by == "Department":
                query = {"Department": search_value}
            
            rows = list(self.collection.find(query))
            if len(rows) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for doc in rows:
                    values_tuple = (
                        doc.get("Department", ""), doc.get("Course", ""), doc.get("Year", ""),
                        doc.get("Semester", ""), doc.get("Student_id", ""), doc.get("Name", ""),
                        doc.get("Division", ""), doc.get("Roll", ""), doc.get("Gender", ""),
                        doc.get("Dob", ""), doc.get("Email", ""), doc.get("Phone", ""),
                        doc.get("Address", ""), doc.get("Teacher", ""), doc.get("PhotoSample", "")
                    )
                    self.student_table.insert("", END, values=values_tuple)
            else:
                messagebox.showinfo("Result", "No records found", parent=self.root)
                self.student_table.delete(*self.student_table.get_children())

        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

        #==================reload function====================
    def show_all(self):
        self.search_combo.current(0)
        self.search_entry.delete(0, END)
        self.fetch_data()

    #====================generate data set or take photo sample============
    def generate_dataset(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root) 
        else:
            try:
                student_id = self.var_std_id.get()
                # Update the student data in the database first.
                update_dict = {
                    "Department": self.var_dep.get(), "Course": self.var_course.get(),
                    "Year": self.var_year.get(), "Semester": self.var_semester.get(),
                    "Name": self.var_std_name.get(), "Division": self.var_div.get(),
                    "Dob": self.var_dob.get(), "Roll": self.var_roll.get(),
                    "Gender": self.var_gender.get(), "Email": self.var_email.get(),
                    "Phone": self.var_phone.get(), "Address": self.var_address.get(),
                    "Teacher": self.var_teacher.get(), "PhotoSample": "YES"
                }
                self.collection.update_one(
                    {"Student_id": student_id},
                    {"$set": update_dict},
                    upsert=True # Creates the student record if it does not exist
                )
                self.fetch_data()
                self.reset_data()
                #=============load pre defined data on face frontals from opencv=============
                face_classifier=cv2.CascadeClassifier(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\haarcascade_frontalface_default.xml")
                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)
                    for (x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped
                data_dir = os.path.join(os.getcwd(), r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\data")
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                cap = cv2.VideoCapture(0)
                #address = "http://192.0.0.2:8080/video"
                #video_cap = cv2.VideoCapture(address)
                img_id = 0
                while True:
                    ret,my_frame=cap.read()
                    cropped_face = face_cropped(my_frame)
                    if cropped_face is not None:
                        img_id+=1
                        face=cv2.resize(cropped_face,(450,450))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path=os.path.join(data_dir, f"user.{student_id}.{img_id}.jpg")
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Cropped Face",face)
                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Generating data set completed!!")
            except Exception as es:
                messagebox.showerror("Error",f"Due to:{str(es)}",parent=self.root)
                
    def update_photos(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Please select a student first", parent=self.root)
            return

        try:
            student_id = self.var_std_id.get()

            # Delete old images
            folder_path = r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\data"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            for file in os.listdir(folder_path):
                if file.startswith(f"user.{student_id}."):
                    os.remove(os.path.join(folder_path, file))

            # Load face classifier
            face_classifier = cv2.CascadeClassifier(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y+h, x:x+w]
                return None

            cap = cv2.VideoCapture(0)
            #address = "http://192.0.0.2:8080/video"
            #video_cap = cv2.VideoCapture(address)
            img_id = 0

            while True:
                ret, my_frame = cap.read()
                cropped = face_cropped(my_frame)
                if cropped is not None:
                    img_id += 1
                    face = cv2.resize(cropped, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = os.path.join(folder_path, f"user.{student_id}.{img_id}.jpg")
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Updated Photo", face)

                if cv2.waitKey(1) == 13 or img_id == 100:
                    break

            cap.release()
            cv2.destroyAllWindows()

            # Update PhotoSample to YES
            self.collection.update_one(
                {"Student_id": student_id},
                {"$set": {"PhotoSample": "YES"}}
            )
            self.fetch_data()

            messagebox.showinfo("Success", "Photo update completed!", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj=Student(root)
    root.mainloop()