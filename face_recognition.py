from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
from pymongo import MongoClient # Replaced mysql.connector
import cv2
import torch
import numpy as np
from time import strftime
from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image as PILImage

class Face_Recognition:
    def __init__(self, root):
        self.root = root
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

        title_lbl = Label(self.root, text="FACE RECOGNITION", font=('times new roman', 35, 'bold'), bg='white', fg='darkgreen')
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\face_detector1.jpg").resize((650, 700), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=650, height=700)

        img_btm = Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg").resize((950, 700), Image.Resampling.LANCZOS)
        self.photoimg_btm = ImageTk.PhotoImage(img_btm)
        f_lbl = Label(self.root, image=self.photoimg_btm)
        f_lbl.place(x=650, y=55, width=950, height=700)

        b1_1 = Button(f_lbl, text='Face Recognition', command=self.face_recog, cursor='hand2', font=('times new roman', 18, 'bold'), bg='green', fg='white')
        b1_1.place(x=365, y=620, width=200, height=40)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

        try:
            data = np.load(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\face_embeddings.npz")
            self.known_embeddings = data['embeddings']
            self.known_labels = data['labels']
        except FileNotFoundError:
             messagebox.showerror("Error", "face_embeddings.npz not found. Please train the model first.", parent=self.root)
             self.root.destroy()


    def mark_attendance(self, i, r, n, d):
        file_path = r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\attendance.csv"
        try:
            with open(file_path, "a+", encoding="utf-8") as f:
                f.seek(0)
                myDataList = f.readlines()
                # Check for today's date and student ID to prevent duplicate entries for the same day
                name_list = []
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                for line in myDataList:
                    entry = line.strip().split(',')
                    if len(entry) > 5 and entry[0] == i and entry[5] == d1:
                        name_list.append(entry[0])

                if i not in name_list:
                    dtString = now.strftime("%H:%M:%S")
                    f.write(f"{i},{r},{n},{d},{dtString},{d1},Present\n")
        except Exception as es:
            messagebox.showerror("File Error", f"Could not write to attendance file: {es}", parent=self.root)


    def face_recog(self):
        cap = cv2.VideoCapture(0)
        #address = "http://192.0.0.2:8080/video"
        #video_cap = cv2.VideoCapture(address)
        threshold = 0.8

        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to grab frame from camera.")
                break

            try:
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = PILImage.fromarray(img_rgb)

                faces = self.mtcnn(img_pil)
                boxes, _ = self.mtcnn.detect(img_pil)

                if faces is not None and boxes is not None:
                    for face, box in zip(faces, boxes):
                        with torch.no_grad():
                            emb = self.model(face.unsqueeze(0).to(self.device)).cpu().numpy()

                        sims = cosine_similarity(emb, self.known_embeddings)[0]
                        best_idx = np.argmax(sims)
                        best_score = sims[best_idx]

                        x1, y1, x2, y2 = [int(coord) for coord in box]

                        if best_score >= threshold:
                            student_id_str = str(self.known_labels[best_idx])
                            # --- MongoDB Query ---
                            student_doc = self.collection.find_one({"Student_id": student_id_str})

                            if student_doc:
                                # Safely get data from the document
                                n = student_doc.get("Name", "N/A")
                                r = student_doc.get("Roll", "N/A")
                                d = student_doc.get("Department", "N/A")
                                i_ = student_doc.get("Student_id", "N/A")

                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, f"ID: {i_}", (x1, y1 - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                                cv2.putText(frame, f"Roll: {r}", (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                                cv2.putText(frame, f"Name: {n}", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                                cv2.putText(frame, f"Dept: {d}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                                self.mark_attendance(i_, r, n, d)
                            else:
                                # Student ID from model not found in DB
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                                cv2.putText(frame, "ID Not in DB", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        else:
                            # Face detected but not recognized
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cv2.putText(frame, "Unknown", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                else:
                    cv2.putText(frame, "No face detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow("Face Recognition", frame)

            except Exception as es:
                print(f"An error occurred: {es}") # Print error to console for debugging

            if cv2.waitKey(1) == 13: # 13 is the Enter Key
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()