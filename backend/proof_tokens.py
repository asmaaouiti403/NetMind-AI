from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-small-en-v1.5")

text = "OSPF uses Dijkstra's algorithm for shortest path."
tokens = tokenizer.encode(text)
fragments = [tokenizer.decode([t]) for t in tokens]

print("--- Tokenization Proof ---")
print(f"Original Text: {text}")
print(f"Token IDs: {tokens}")
print(f"Decoded Fragments: {fragments}")