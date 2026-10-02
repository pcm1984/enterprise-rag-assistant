import psycopg
import requests


query = "How should Kafka consumers handle duplicate messages?"


# --------------------------------------------------
# 1. Create query embedding
# --------------------------------------------------

response = requests.post(
    "http://localhost:11434/api/embed",
    json={
        "model": "nomic-embed-text",
        "input": query
    }
)

query_embedding = response.json()["embeddings"][0]


# --------------------------------------------------
# 2. Connect to PostgreSQL
# --------------------------------------------------

connection = psycopg.connect(
    "dbname=enterprise_rag"
)


# --------------------------------------------------
# 3. Search for the most similar chunks
# --------------------------------------------------

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
        LIMIT 5
        """,
        (
            query_embedding,
            query_embedding
        )
    )

    results = cursor.fetchall()


# --------------------------------------------------
# 4. Display results
# --------------------------------------------------

for document, section, content, distance in results:

    print("\nDistance:", distance)
    print("Document:", document)
    print("Section:", section)
    print("Content:")
    print(content)


connection.close()
