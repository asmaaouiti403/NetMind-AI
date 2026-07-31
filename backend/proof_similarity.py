import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# Generate 3 vectors
v_query = np.array(model.embed_query("Routing Protocol")).reshape(1, -1)
v_ospf = np.array(model.embed_query("OSPF dynamic routing configuration")).reshape(1, -1)
v_pizza = np.array(model.embed_query("Italian pizza with extra cheese")).reshape(1, -1)

# Calculate similarity (0 to 1)
sim_networking = cosine_similarity(v_query, v_ospf)[0][0]
sim_noise = cosine_similarity(v_query, v_pizza)[0][0]

print("--- COSINE SIMILARITY PROOF ---")
print(f"Similarity (Query vs OSPF): {sim_networking:.4f}")
print(f"Similarity (Query vs Pizza): {sim_noise:.4f}")