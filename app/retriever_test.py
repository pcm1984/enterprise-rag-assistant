from retriever import retrieve


query = "How should Kafka consumers handle duplicate messages?"

roles = ["developer", "architect"]

results = retrieve(
    query,
    roles=roles,
    top_k=5
)

print(f"\n=== RESULTS FOR ROLES: {roles} ===")

for result in results:
    print("\nDistance:", result["distance"])
    print("Document:", result["document"])
    print("Section:", result["section"])
    print("Content:")
    print(result["content"])
