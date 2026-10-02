from pathlib import Path
import math
import requests


def create_chunks():
    knowledge_directory = Path("knowledge")
    chunks = []

    for file in knowledge_directory.glob("*.md"):
        content = file.read_text()
        document_name = file.name

        sections = content.split("## ")

        for section in sections:
            if not section.strip():
                continue

            lines = section.strip().splitlines()

            section_name = lines[0]
            section_content = "\n".join(lines[1:]).strip()

            if not section_content:
                continue

            chunk_text = (
                f"{document_name}\n"
                f"{section_name}\n\n"
                f"{section_content}"
            )

            chunk = {
                "document": document_name,
                "section": section_name,
                "content": section_content,
                "text": chunk_text
            }

            chunks.append(chunk)

    return chunks


def create_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text
        }
    )

    result = response.json()

    return result["embeddings"][0]


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)


# --------------------------------------------------
# 1. Create chunks
# --------------------------------------------------

chunks = create_chunks()

print("Number of chunks:", len(chunks))


# --------------------------------------------------
# 2. Create an embedding for every chunk
# --------------------------------------------------

for chunk in chunks:
    chunk["embedding"] = create_embedding(chunk["text"])


# --------------------------------------------------
# 3. Create the user's query embedding
# --------------------------------------------------

query = "How should Kafka consumers handle duplicate messages?"

query_embedding = create_embedding(query)


# --------------------------------------------------
# 4. Compare the query with every chunk
# --------------------------------------------------

results = []

for chunk in chunks:
    similarity = cosine_similarity(
        query_embedding,
        chunk["embedding"]
    )

    results.append(
        {
            "chunk": chunk,
            "similarity": similarity
        }
    )


# --------------------------------------------------
# 5. Rank chunks by similarity
# --------------------------------------------------

results.sort(
    key=lambda result: result["similarity"],
    reverse=True
)


# --------------------------------------------------
# 6. Display retrieval results
# --------------------------------------------------

top_k = 9

print("\n=== TOP", top_k, "RETRIEVAL RESULTS ===")

for result in results[:top_k]:
    chunk = result["chunk"]

    print("\nSimilarity:", result["similarity"])
    print("Document:", chunk["document"])
    print("Section:", chunk["section"])
    print("Content:")
    print(chunk["content"])
