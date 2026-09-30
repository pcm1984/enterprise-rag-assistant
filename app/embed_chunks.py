from pathlib import Path
import requests


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


chunks = create_chunks()

for chunk in chunks:
    chunk["embedding"] = create_embedding(chunk["text"])

print("Number of chunks:", len(chunks))

for chunk in chunks:
    print("\n--- CHUNK ---")
    print("Document:", chunk["document"])
    print("Section:", chunk["section"])
    print("Embedding dimensions:", len(chunk["embedding"]))
    print("First 5 values:", chunk["embedding"][:5])



