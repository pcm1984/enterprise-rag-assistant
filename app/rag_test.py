from rag import answer_question


def run_test(name, roles, question):
    print(f"\n{'=' * 60}")
    print(f"TEST: {name}")
    print(f"ROLES: {roles}")
    print(f"QUESTION: {question}")
    print("=" * 60)

    result = answer_question(
        question,
        roles=roles,
        top_k=5
    )

    print("\nANSWER:")
    print(result["answer"])

    print("\nRETRIEVED SOURCES:")

    for source in result["results"]:
        print(
            f"- {source['document']} — "
            f"{source['section']}"
        )


question = "How should Kafka consumers handle duplicate messages?"


run_test(
    "Developer can access Event Design",
    ["developer"],
    question
)


run_test(
    "Architect cannot access Event Design",
    ["architect"],
    question
)


run_test(
    "Security cannot access Kafka guidance",
    ["security"],
    question
)


run_test(
    "Developer + Architect",
    ["developer", "architect"],
    question
)


run_test(
    "User with no roles",
    [],
    question
)
