import numpy as np

data = np.load("C:\\Users\\Karthik Sagar P\\OneDrive\\Desktop\\COLLEGE\\capstone\\facerecogsys\\facerecogsys\\face_embeddings.npz")
embeddings = data['embeddings']
labels = data['labels']

print("Embeddings shape:", embeddings.shape)
print("Labels shape:", labels.shape)
print("Number of embeddings:", len(embeddings))
print("Number of labels:", len(labels))
print("First few labels:", labels[:5])

if len(embeddings) == 0 or len(labels) == 0:
    print("Error: One or both arrays are empty.")
elif len(embeddings) != len(labels):
    print("Error: Number of embeddings and labels do not match.")
else:
    print("NPZ file looks fine.")