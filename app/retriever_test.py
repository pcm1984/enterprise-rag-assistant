from retriever import retrieve


query = "How should Kafka consumers handle duplicate messages?"

results = retrieve(query, top_k=3)

for result in results:
    print("\nDistance:", result["distance"])
    print("Document:", result["document"])
    print("Section:", result["section"])
    print("Content:")
    print(result["content"])
