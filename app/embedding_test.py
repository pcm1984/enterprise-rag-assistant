import requests
import math


texts = [
    "Kafka should be used for asynchronous event communication.",
    "Synchronous REST APIs are preferred when an immediate response is required.",
    "AWS Lambda is a serverless compute service."
]

query = "When should we use Kafka?"

response = requests.post(
    "http://localhost:11434/api/embed",
    json={
        "model": "nomic-embed-text",
        "input": texts + [query]
    }
)

result = response.json()

embeddings = result["embeddings"]

document_embeddings = embeddings[:3]
query_embedding = embeddings[3]

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)

for text, embedding in zip(texts, document_embeddings):
    similarity = cosine_similarity(query_embedding, embedding)

    print("\nDocument:", text)
    print("Similarity:", similarity)

