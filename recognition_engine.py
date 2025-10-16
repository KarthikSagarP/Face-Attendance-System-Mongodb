# recognition_engine.py

import cv2
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity
import torch
import time

# Load face detector (MTCNN) and FaceNet
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(image_size=160, margin=20, keep_all=False, device=device)
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Load known embeddings and labels
data = np.load(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\face_embeddings.npz")
known_embeddings = data['embeddings']
known_labels = data['labels']

def recognize_faces_from_frame(threshold=0.6):
    recognized_ids = set()
    video_cap = cv2.VideoCapture(0)
    #address = "http://192.0.0.2:8080/video"
    #video_cap = cv2.VideoCapture(address)
    start_time = time.time()

    if not video_cap.isOpened():
        print("Webcam error")
        return []

    while True:
        ret, frame = video_cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        boxes, _ = mtcnn.detect(img_pil)

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = [int(b) for b in box]
                face_img = img_rgb[y1:y2, x1:x2]

                try:
                    face_pil = Image.fromarray(face_img)
                    face_tensor = mtcnn(face_pil)

                    if face_tensor is not None:
                        with torch.no_grad():
                            embedding = model(face_tensor.unsqueeze(0).to(device)).cpu().numpy()

                        sims = cosine_similarity(embedding, known_embeddings)[0]
                        best_match_idx = np.argmax(sims)
                        best_score = sims[best_match_idx]

                        if best_score >= threshold:
                            matched_id = int(known_labels[best_match_idx])
                            recognized_ids.add(matched_id)
                            label = f"ID: {matched_id}"
                            color = (0, 255, 0)
                        else:
                            label = "Unknown"
                            color = (0, 0, 255)

                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                except Exception as e:
                    print(f"[WARN] Skipping face due to error: {e}")

        else:
            cv2.putText(frame, "No faces detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Live Monitoring Feed", frame)

        if cv2.waitKey(1) == 13 or (time.time() - start_time > 10):  # Press Enter or timeout
            break

    video_cap.release()
    cv2.destroyAllWindows()

    return list(recognized_ids)
