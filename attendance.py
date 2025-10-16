from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import csv
from tkinter import filedialog

mydata=[]
class Attendance:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance Management System")

        #=================variables====================
        self.var_atten_id=StringVar()
        self.var_atten_name=StringVar()
        self.var_atten_dep=StringVar()
        self.var_atten_section=StringVar()
        self.var_atten_time=StringVar()
        self.var_atten_date=StringVar()
        self.var_atten_status=StringVar()
        self.var_atten_rounds_present=StringVar()
        self.var_atten_total_rounds=StringVar()
        self.csv_file_path = None

        #first image
        img=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\smart-attendance.jpg")
        img=img.resize((800,200),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=800,height=200)

        #second image
        img1=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\iStock-182059956_18390_t12.jpg")
        img1=img1.resize((800,200),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=800,y=0,width=800,height=200)

        #bg image
        img3=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\wp2551980.jpg")
        img3=img3.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=200,width=1530,height=710)

        title_lbl=Label(bg_img,text="ATTENDANCE MANAGEMENT SYSTEM",font=('times new roman',35,'bold'),bg='white',fg='darkgreen')
        title_lbl.place(x=0,y=0,width=1530,height=45)

        main_frame=Frame(bg_img,bd=2)
        main_frame.place(x=20,y=50,width=1480,height=600)
        
        #left label frame
        Left_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text='Student Attendance Details',font=('times new roman',12,'bold'))
        Left_frame.place(x=10,y=10,width=730,height=580)

        img_left=Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\AdobeStock_303989091.jpeg")
        img_left=img_left.resize((720,130),Image.Resampling.LANCZOS)
        self.photoimg_left=ImageTk.PhotoImage(img_left)

        f_lbl=Label(Left_frame,image=self.photoimg_left)
        f_lbl.place(x=5,y=0,width=720,height=130)

        left_inside_frame=Frame(Left_frame,bd=2,relief=RIDGE,bg="white")
        left_inside_frame.place(x=0,y=135,width=720,height=370)

        #=================Labels and entry================
        studentID_label=Label(left_inside_frame,text="Student ID:",bg="white",font=('times new roman',13,'bold'))
        studentID_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)
        studentID_entry=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_id,font=('times new roman',13,'bold'))
        studentID_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)

        nameLabel=Label(left_inside_frame,text="Name:",bg="white",font=('times new roman',13,'bold'))
        nameLabel.grid(row=0,column=2,padx=10,pady=5,sticky=W)
        atten_name=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_name,font=('times new roman',13,'bold'))
        atten_name.grid(row=0,column=3,padx=10,pady=5,sticky=W)

        depLabel=Label(left_inside_frame,text="Department:",bg="white",font=('times new roman',13,'bold'))
        depLabel.grid(row=1,column=0,padx=10,pady=5,sticky=W)
        atten_dep=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_dep,font=('times new roman',13,'bold'))
        atten_dep.grid(row=1,column=1,padx=10,pady=5,sticky=W)
        
        sectionLabel=Label(left_inside_frame,text="Section:",bg="white",font=('times new roman',13,'bold'))
        sectionLabel.grid(row=1,column=2,padx=10,pady=5,sticky=W)
        atten_section=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_section,font=('times new roman',13,'bold'))
        atten_section.grid(row=1,column=3,padx=10,pady=5,sticky=W)

        timeLabel=Label(left_inside_frame,text="Time:",bg="white",font=('times new roman',13,'bold'))
        timeLabel.grid(row=2,column=0,padx=10,pady=5,sticky=W)
        atten_time=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_time,font=('times new roman',13,'bold'))
        atten_time.grid(row=2,column=1,padx=10,pady=5,sticky=W)

        dateLabel=Label(left_inside_frame,text="Date:",bg="white",font=('times new roman',13,'bold'))
        dateLabel.grid(row=2,column=2,padx=10,pady=5,sticky=W)
        atten_date=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_date,font=('times new roman',13,'bold'))
        atten_date.grid(row=2,column=3,padx=10,pady=5,sticky=W)

        statusLabel=Label(left_inside_frame,text="Attendance Status:",bg="white",font=('times new roman',13,'bold'))
        statusLabel.grid(row=3,column=0,padx=10,pady=5,sticky=W)
        self.atten_status=ttk.Combobox(left_inside_frame,width=20,textvariable=self.var_atten_status,font=('times new roman',13,'bold'),state="readonly")
        self.atten_status['values']=('Status','Present','Absent')
        self.atten_status.grid(row=3,column=1,pady=8)
        self.atten_status.current(0)
        
        roundsPresentLabel=Label(left_inside_frame,text="Rounds Present:",bg="white",font=('times new roman',13,'bold'))
        roundsPresentLabel.grid(row=4,column=0,padx=10,pady=5,sticky=W)
        atten_rounds_present=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_rounds_present,font=('times new roman',13,'bold'))
        atten_rounds_present.grid(row=4,column=1,padx=10,pady=5,sticky=W)

        totalRoundsLabel=Label(left_inside_frame,text="Total Rounds:",bg="white",font=('times new roman',13,'bold'))
        totalRoundsLabel.grid(row=4,column=2,padx=10,pady=5,sticky=W)
        atten_total_rounds=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_total_rounds,font=('times new roman',13,'bold'))
        atten_total_rounds.grid(row=4,column=3,padx=10,pady=5,sticky=W)
        
        #buttons frame
        btn_frame=Frame(left_inside_frame,bd=2,relief=RIDGE)
        btn_frame.place(x=0,y=300,width=715,height=35)

        import_btn=Button(btn_frame,text="Import csv",command=self.importCsv,width=17,font=('times new roman',13,'bold'),bg="blue",fg="white")
        import_btn.grid(row=0,column=0)

        export_btn=Button(btn_frame,text="Export csv",command=self.exportCsv,width=17,font=('times new roman',13,'bold'),bg="blue",fg="white")
        export_btn.grid(row=0,column=1)

        update_btn=Button(btn_frame,text="Update",command=self.update_data,width=17,font=('times new roman',13,'bold'),bg="blue",fg="white")
        update_btn.grid(row=0,column=2)

        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,width=17,font=('times new roman',13,'bold'),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)

        #right label frame
        Right_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text='Attendance Details',font=('times new roman',12,'bold'))
        Right_frame.place(x=750,y=10,width=720,height=580)
        
        #search system restored
        Search_frame=LabelFrame(Right_frame,bd=2,relief=RIDGE,text='Search System',font=('times new roman',12,'bold'))
        Search_frame.place(x=5,y=5,width=700,height=70)

        search_label=Label(Search_frame,text="Search By:",font=('times new roman',13,'bold'),bg="red",fg="white")
        search_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        self.search_combo=ttk.Combobox(Search_frame,font=('times new roman',12,'bold'),width=15,state="readonly")
        self.search_combo["values"]=("Select","Date","Student ID")
        self.search_combo.current(0)
        self.search_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        self.search_entry=ttk.Entry(Search_frame,width=15,font=('times new roman',12,'bold'))
        self.search_entry.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        search_btn=Button(Search_frame,text="Search",width=12,command=self.search_data,font=('times new roman',12,'bold'),bg="blue",fg="white")
        search_btn.grid(row=0,column=3,padx=4)

        showAll_btn=Button(Search_frame,text="Show All",width=12, command=self.show_all_data,font=('times new roman',12,'bold'),bg="blue",fg="white")
        showAll_btn.grid(row=0,column=4,padx=4)
        
        table_frame=Frame(Right_frame,bd=2,relief=RIDGE,bg="white")
        table_frame.place(x=5,y=80,width=700,height=465)

        #==========scroll bar and table=================
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.AttendanceReportTable=ttk.Treeview(table_frame,columns=("id","name","dep","section","time","date","status","rounds_present","total_rounds"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id",text="Student ID")
        self.AttendanceReportTable.heading("name",text="Name")
        self.AttendanceReportTable.heading("dep",text="Department")
        self.AttendanceReportTable.heading("section",text="Section")
        self.AttendanceReportTable.heading("time",text="Time")
        self.AttendanceReportTable.heading("date",text="Date")
        self.AttendanceReportTable.heading("status",text="Status")
        self.AttendanceReportTable.heading("rounds_present", text="Rounds Present")
        self.AttendanceReportTable.heading("total_rounds", text="Total Rounds")

        self.AttendanceReportTable['show']='headings'
        self.AttendanceReportTable.column("id",width=100)
        self.AttendanceReportTable.column("name",width=120)
        self.AttendanceReportTable.column("dep",width=100)
        self.AttendanceReportTable.column("section",width=80)
        self.AttendanceReportTable.column("time",width=80)
        self.AttendanceReportTable.column("date",width=80)
        self.AttendanceReportTable.column("status",width=80)
        self.AttendanceReportTable.column("rounds_present", width=100)
        self.AttendanceReportTable.column("total_rounds", width=80)

        self.AttendanceReportTable.pack(fill=BOTH,expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)

    def fetch_data(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("",END,values=i)

    def importCsv(self):
        global mydata
        mydata.clear()
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV Files","*.csv"),("ALL File","*.*")),parent=self.root)
        if fln:
            self.csv_file_path = fln
            with open(fln) as myfile:
                csvread=csv.reader(myfile,delimiter=",")
                try:
                    next(csvread) 
                except StopIteration:
                    pass # Handles empty files
                for i in csvread:
                    mydata.append(i)
                self.fetch_data(mydata)

    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No data found to export",parent=self.root)
                return False
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Save CSV",filetypes=(("CSV Files","*.csv"),("ALL File","*.*")),parent=self.root)
            if fln:
                with open(fln,mode="w", newline='') as myfile:
                    export=csv.writer(myfile,delimiter=",")
                    export.writerow(["Student_ID","Name","Department","Section","Time","Date","Final_Status","Rounds_Present","Total_Rounds"])
                    for i in mydata:
                        export.writerow(i)
                    messagebox.showinfo("Data Export","Your data was exported to "+os.path.basename(fln)+" successfully",parent=self.root)
        except Exception as es:
            messagebox.showerror("Error",f"Error due to :{str(es)}",parent=self.root)

    def get_cursor(self ,event=None):
        try:
            cursor_row=self.AttendanceReportTable.focus()
            contents=self.AttendanceReportTable.item(cursor_row)
            row=contents["values"]
            self.var_atten_id.set(row[0])
            self.var_atten_name.set(row[1])
            self.var_atten_dep.set(row[2])
            self.var_atten_section.set(row[3])
            self.var_atten_time.set(row[4])
            self.var_atten_date.set(row[5])
            self.var_atten_status.set(row[6])
            self.var_atten_rounds_present.set(row[7])
            self.var_atten_total_rounds.set(row[8])
        except (IndexError, KeyError):
            self.reset_data()

    def reset_data(self):
        self.var_atten_id.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_section.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_status.set("Status")
        self.var_atten_rounds_present.set("")
        self.var_atten_total_rounds.set("")

    # Restored and updated to work with the 9-column CSV data
    def update_data(self):
        selected_item = self.AttendanceReportTable.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to update.", parent=self.root)
            return

        # Get the Student ID from the selected row (it's the first value)
        selected_id = self.AttendanceReportTable.item(selected_item)['values'][0]

        updated_row = [
            self.var_atten_id.get(), self.var_atten_name.get(),
            self.var_atten_dep.get(), self.var_atten_section.get(),
            self.var_atten_time.get(), self.var_atten_date.get(),
            self.var_atten_status.get(), self.var_atten_rounds_present.get(),
            self.var_atten_total_rounds.get()
        ]

        # Find the corresponding row in mydata and update it
        for i, row in enumerate(mydata):
            if row[0] == selected_id:
                mydata[i] = updated_row
                break

        # Refresh the table and save to the original CSV file
        self.fetch_data(mydata)
        self.save_to_csv()
        messagebox.showinfo("Success", "Record updated successfully.", parent=self.root)

    def save_to_csv(self):
        if not self.csv_file_path:
            messagebox.showerror("Error", "No CSV file is currently loaded to save to.", parent=self.root)
            return
        try:
            with open(self.csv_file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Student_ID","Name","Department","Section","Time","Date","Final_Status","Rounds_Present","Total_Rounds"])
                writer.writerows(mydata)
        except Exception as es:
            messagebox.showerror("File Error", f"Failed to save changes to CSV: {es}", parent=self.root)

    # New search function that works on the loaded CSV data
    def search_data(self):
        search_by = self.search_combo.get()
        search_text = self.search_entry.get().strip()

        if search_by == "Select" or not search_text:
            messagebox.showerror("Error", "Please select a search category and enter text.", parent=self.root)
            return

        results = []
        if search_by == "Date":
            col_index = 5 # Date is the 6th column (index 5)
        elif search_by == "Student ID":
            col_index = 0 # Student ID is the 1st column (index 0)
        else:
            return

        for row in mydata:
            if len(row) > col_index and search_text.lower() in row[col_index].lower():
                results.append(row)

        if results:
            self.fetch_data(results)
        else:
            messagebox.showinfo("No Results", "No matching records found.", parent=self.root)
            self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
            
    def show_all_data(self):
        self.fetch_data(mydata)
        self.search_entry.delete(0, END)
        self.search_combo.current(0)


if __name__ == "__main__":
    root = Tk()
    obj=Attendance(root)
    root.mainloop()