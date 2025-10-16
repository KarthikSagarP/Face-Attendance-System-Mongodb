import cv2
import numpy as np
import os
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

# Paths to models and data
EMBEDDINGS_PATH = 'C:\\Users\\Karthik Sagar P\\OneDrive\\Desktop\\COLLEGE\\capstone\\facerecogsys\\facerecogsys\\face_embeddings.npz'
IMAGES_FOLDER = 'C:\\Users\\Karthik Sagar P\\OneDrive\\Desktop\\COLLEGE\\capstone\\facerecogsys\\facerecogsys\\class images'
OUTPUT_FOLDER = 'C:\\Users\\Karthik Sagar P\\OneDrive\\Desktop\\COLLEGE\\capstone\\facerecogsys\\facerecogsys\\annotated_images'
SIMILARITY_THRESHOLD = 0.7  # You can adjust this value

# Set up MTCNN and FaceNet (InceptionResnetV1)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device=device)
facenet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Load embeddings and student IDs
embeddings_data = np.load(EMBEDDINGS_PATH)
embeddings = embeddings_data['embeddings']
labels = embeddings_data['labels']

# Helper: cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Create output folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Process images
for img_name in os.listdir(IMAGES_FOLDER):
    img_path = os.path.join(IMAGES_FOLDER, img_name)
    img = cv2.imread(img_path)
    if img is None:
        continue
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    boxes, probs = mtcnn.detect(pil_img)
    faces = mtcnn(pil_img)
    if boxes is not None and faces is not None:
        if faces.ndim == 3:
            faces = faces.unsqueeze(0)
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = [int(b) for b in box]
            face_tensor = faces[i].to(device)
            emb = facenet(face_tensor.unsqueeze(0))
            embedding = emb.detach().cpu().numpy()[0]
            similarities = [cosine_similarity(embedding, embd) for embd in embeddings]
            best_match_idx = np.argmax(similarities)
            best_similarity = similarities[best_match_idx]
            if best_similarity >= SIMILARITY_THRESHOLD:
                student_id = labels[best_match_idx]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, str(student_id), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                # Optionally, draw a box without label or in a different color
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    out_path = os.path.join(OUTPUT_FOLDER, img_name)
    cv2.imwrite(out_path, img)

print(f"Processed images saved in '{OUTPUT_FOLDER}' folder.")
