from langchain_huggingface import HuggingFaceEmbeddings

model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vector = model.embed_query("HSRP Priority 110")

print("--- EMBEDDING PROOF ---")
print(f"Vector Dimensions: {len(vector)}")
print(f"First 10 values of the vector:\n{vector[:10]}")