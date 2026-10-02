import psycopg


connection = psycopg.connect(
    "dbname=enterprise_rag"
)

print("Connected to PostgreSQL")

connection.close()

print("Connection closed")
