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

def retrieve(query, roles, top_k=5):

    if not roles:
        return []

    query_embedding = create_embedding(query)

    placeholders = ", ".join(
        ["%s"] * len(roles)
    )

    connection = psycopg.connect(
        "dbname=enterprise_rag"
    )

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                c.document,
                c.section,
                c.content,
                c.embedding <=> %s::vector AS distance
            FROM rag_chunks c
            WHERE EXISTS (
                SELECT 1
                FROM rag_chunk_roles r
                WHERE r.chunk_id = c.id
                  AND r.role IN ({placeholders})
            )
            ORDER BY c.embedding <=> %s::vector
            LIMIT %s
            """,
            (
                query_embedding,
                *roles,
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
