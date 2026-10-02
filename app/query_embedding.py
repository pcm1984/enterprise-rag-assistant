import requests


query = "How should Kafka consumers handle duplicate messages?"


response = requests.post(
    "http://localhost:11434/api/embed",
    json={
        "model": "nomic-embed-text",
        "input": query
    }
)


embedding = response.json()["embeddings"][0]


print("Embedding dimensions:", len(embedding))
print(embedding[:5])
