import requests

from retriever import retrieve


def build_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            f"""Document: {result["document"]}
Section: {result["section"]}

{result["content"]}
"""
        )

    return "\n\n".join(context_parts)


def generate_answer(question, context):

    prompt = f"""
You are an enterprise architecture knowledge assistant.

Answer the user's question using ONLY the provided context.

If the context does not contain enough information to answer the
question, say:

"I don't know based on the available documentation."

Do not invent information.

Answer the question comprehensively but concisely.

Use all relevant information from the context.
Do not omit important conditions or exceptions.

Context:
{context}

User question:
{question}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def answer_question(question, top_k=5):

    results = retrieve(
        question,
        top_k=top_k
    )

    context = build_context(results)

    answer = generate_answer(
        question,
        context
    )

    return {
        "answer": answer,
        "results": results
    }


question = input("Ask a question: ")

result = answer_question(question)

print("\n=== ANSWER ===")
print(result["answer"])

print("\n=== SOURCES ===")

for source in result["results"]:
    print(
        f"- {source['document']} — "
        f"{source['section']}"
    )
