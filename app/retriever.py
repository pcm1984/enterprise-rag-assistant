import psycopg
import requests


def create_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text
        }
    )

    return response.json()["embeddings"][0]


def retrieve(query, top_k=5):
    query_embedding = create_embedding(query)

    connection = psycopg.connect(
        "dbname=enterprise_rag"
    )

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                document,
                section,
                content,
                embedding <=> %s::vector AS distance
            FROM rag_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (
                query_embedding,
                query_embedding,
                top_k
            )
        )

        rows = cursor.fetchall()

        connection.close()

        results = []

        for document, section, content, distance in rows:
            results.append(
               { 
                   "document": document,
                   "section": section,
                   "content": content,
                   "distance": distance
               }
            )

        return results
