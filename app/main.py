import requests

question = input("Ask a question: ")

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3:latest",
        "prompt": question,
        "stream": False
    }
)

result = response.json()

print("\nAnswer:")
print(result["response"])
