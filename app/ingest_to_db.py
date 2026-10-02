from pathlib import Path

import psycopg
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

            chunks.append(
                {
                    "document": document_name,
                    "section": section_name,
                    "content": section_content,
                    "text": chunk_text
                }
            )

    return chunks


def create_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text
        }
    )

    return response.json()["embeddings"][0]


chunks = create_chunks()

print("Chunks found:", len(chunks))

connection = psycopg.connect(
    "dbname=enterprise_rag"
)

for index, chunk in enumerate(chunks, start=1):

    print(
        f"Embedding chunk {index}/{len(chunks)}: "
        f"{chunk['document']} / {chunk['section']}"
    )

    embedding = create_embedding(chunk["text"])

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO rag_chunks
                (document, section, content, text, embedding)
            VALUES
                (%s, %s, %s, %s, %s)
            """,
            (
                chunk["document"],
                chunk["section"],
                chunk["content"],
                chunk["text"],
                embedding
            )
        )

connection.commit()
connection.close()

print("Ingestion complete.")
