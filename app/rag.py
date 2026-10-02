import requests

from retriever import retrieve


def build_context(results):
    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"""Source {index}
Document: {result["document"]}
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

             When the context contains a decision rule, explain the
             decision rule rather than quoting only one sentence.

             Cite the supporting source using its document and section.

             If multiple sources contribute to the answer, cite them.

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


question = input("Ask a question: ")

results = retrieve(question, top_k=5)

context = build_context(results)

print("\n=== RETRIEVED CONTEXT ===")
print(context)

answer = generate_answer(question, context)

print("\n=== ANSWER ===")
print(answer)
