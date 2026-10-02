import psycopg
import requests


# --------------------------------------------------
# 1. Create an embedding
# --------------------------------------------------

text = """
kafka_guidelines.md
Event Design

Events should represent meaningful business events rather than
low-level implementation details.

Event consumers should be idempotent because messages may be
delivered more than once.
""".strip()


response = requests.post(
    "http://localhost:11434/api/embed",
    json={
        "model": "nomic-embed-text",
        "input": text
    }
)

embedding = response.json()["embeddings"][0]

print("Embedding dimensions:", len(embedding))


# --------------------------------------------------
# 2. Connect to PostgreSQL
# --------------------------------------------------

connection = psycopg.connect(
    "dbname=enterprise_rag"
)


# --------------------------------------------------
# 3. Insert the chunk
# --------------------------------------------------

with connection.cursor() as cursor:
    cursor.execute(
        """
        INSERT INTO rag_chunks
            (document, section, content, text, embedding)
        VALUES
            (%s, %s, %s, %s, %s)
        """,
        (
            "kafka_guidelines.md",
            "Event Design",
            """Events should represent meaningful business events rather than
low-level implementation details.

Event consumers should be idempotent because messages may be
delivered more than once.""",
            text,
            embedding
        )
    )

connection.commit()

print("Chunk inserted")


# --------------------------------------------------
# 4. Close the connection
# --------------------------------------------------

connection.close()

print("Connection closed")
