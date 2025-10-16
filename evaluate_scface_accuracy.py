import os
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from facenet_pytorch import MTCNN, InceptionResnetV1

# Load trained embeddings
data = np.load(r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\scface_embeddings.npz")
train_embeddings = data["embeddings"]
train_labels = data["labels"]

# Init MTCNN + FaceNet
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(image_size=160, margin=20, keep_all=False, device=device)
model = InceptionResnetV1(pretrained="vggface2").eval().to(device)

# Test root directory
test_root = r"C:\Users\Karthik Sagar P\OneDrive\Desktop\COLLEGE\capstone\facerecogsys\facerecogsys\scface_test_images"
distances = ["distance_1", "distance_2", "distance_3"]
cams = ["cam_1", "cam_2", "cam_3", "cam_4", "cam_5"]

# Accuracy table
results = {}

for distance in distances:
    results[distance] = {}
    for cam in cams:
        correct = 0
        total = 0
        folder = os.path.join(test_root, distance, cam)
        for img_name in tqdm(os.listdir(folder), desc=f"{distance}/{cam}"):
            try:
                true_id = int(img_name.split("_")[0])
                path = os.path.join(folder, img_name)
                img = Image.open(path).convert("RGB")

                face = mtcnn(img)
                if face is None:
                    continue

                with torch.no_grad():
                    emb = model(face.unsqueeze(0).to(device)).cpu().numpy()

                sims = cosine_similarity(emb, train_embeddings)[0]
                pred_id = train_labels[np.argmax(sims)]
                if int(pred_id) == true_id:
                    correct += 1
                total += 1
            except Exception as e:
                print(f"Error with {img_name}: {e}")
                continue

        accuracy = (correct / total) * 100 if total > 0 else 0
        results[distance][cam] = accuracy

# Display results as a table
print("\n📊 SCface Accuracy Table (in %)\n")
header = " " * 12 + "".join([f"{cam:^12}" for cam in cams])
print(header)
print("-" * len(header))
for distance in distances:
    row = f"{distance:<12}"
    for cam in cams:
        acc = results[distance].get(cam, 0)
        row += f"{acc:>10.2f}%  "
    print(row)
