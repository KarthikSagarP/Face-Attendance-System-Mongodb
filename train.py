from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import torch
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm
from facenet_pytorch import MTCNN, InceptionResnetV1

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="TRAIN MODEL", font=('times new roman', 35, 'bold'), bg='white', fg='darkgreen')
        title_lbl.place(x=0, y=0, width=1530, height=45)

        img_top = Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\facialrecognition.png")
        img_top = img_top.resize((1530, 325), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=325)

        b1_1 = Button(self.root, text=' TRAIN MODEL', command=self.train_classifier, cursor='hand2',
                      font=('times new roman', 15, 'bold'), bg='green', fg='white')
        b1_1.place(x=0, y=380, width=1530, height=60)

        img_btm = Image.open(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\college_images\Photos.jpg")
        img_btm = img_btm.resize((1530, 325), Image.Resampling.LANCZOS)
        self.photoimg_btm = ImageTk.PhotoImage(img_btm)
        f_lbl = Label(self.root, image=self.photoimg_btm)
        f_lbl.place(x=0, y=440, width=1530, height=325)

    def train_classifier(self):
        # ========== Set up MTCNN + FaceNet ==========
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        mtcnn = MTCNN(image_size=160, margin=20, keep_all=False, device=device)
        model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

        # ========== 1. Train on local student images ==========
        student_dir = r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\data"
        student_embeddings = []
        student_labels = []

        for img_name in tqdm(os.listdir(student_dir), desc="[Student Dataset]"):
            path = os.path.join(student_dir, img_name)
            try:
                img = Image.open(path).convert('RGB')
                face = mtcnn(img)

                if face is not None:
                    emb = model(face.unsqueeze(0).to(device))
                    student_embeddings.append(emb.detach().cpu().numpy()[0])
                    # Robust label extraction for format: user.<student_id>.<img_id>.jpg
                    parts = img_name.split('.')
                    if len(parts) >= 3:
                        label = parts[1]  # student_id
                        student_labels.append(label)
            except Exception:
                pass  # Skip silently on any error

        # Save embeddings and labels as npz file
        np.savez(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\face_embeddings.npz",
                 embeddings=np.array(student_embeddings),
                 labels=np.array(student_labels))
        print("[✓] Saved: facerecogsys/face_embeddings.npz")
'''
        # ========== 2. Train on SCface mugshots ==========
        scface_dir = r"facerecogsys/scface_train_images"
        sc_embeddings = []
        sc_labels = []

        for img_name in tqdm(os.listdir(scface_dir), desc="[SCface Dataset]"):
            path = os.path.join(scface_dir, img_name)
            try:
                img = Image.open(path).convert('RGB')
                face = mtcnn(img)

                if face is not None:
                    emb = model(face.unsqueeze(0).to(device))
                    sc_embeddings.append(emb.detach().cpu().numpy()[0])

                    # Extract numeric ID from filename (e.g., 001_L1 → 1)
                    label_str = img_name.split("_")[0]
                    label = int(label_str)
                    sc_labels.append(label)
            except Exception as e:
                print(f"[SCface] Skipping {img_name}: {e}")

        np.savez("facerecogsys/scface_embeddings.npz",
                 embeddings=np.array(sc_embeddings),
                 labels=np.array(sc_labels))
        print("[✓] Saved: facerecogsys/embeddings/scface_embeddings.npz")

        messagebox.showinfo("Training Complete", "Face embeddings for both datasets have been saved.")
'''
if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
