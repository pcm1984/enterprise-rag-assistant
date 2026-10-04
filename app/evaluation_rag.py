rag_evaluation_dataset = [
    {
        "name": "Known question",
        "question": "When should we use Kafka?",
        "roles": ["developer"],
        "expected_behavior": "answer"
    },
    {
    	"name": "Restricted knowledge",
    	"question": "How should AWS credentials be handled?",
    	"roles": ["developer"],
    	"expected_behavior": "do_not_answer",
    	"forbidden_section": "Security"
    },
    {
        "name": "Unknown question",
        "question": "What database technology should we use for microservices?",
        "roles": ["developer", "architect"],
        "expected_behavior": "do_not_answer"
    }
]


from rag import answer_question


def run_test(test_case):

    result = answer_question(
        test_case["question"],
        roles=test_case["roles"],
        top_k=5
    )

    answer = result["answer"]
    
    if "forbidden_section" in test_case:

        retrieved_sections = [
            source["section"]
            for source in result["results"]
        ]  

        assert test_case["forbidden_section"] not in retrieved_sections

    print("\n" + "=" * 60)
    print(f"TEST: {test_case['name']}")
    print(f"QUESTION: {test_case['question']}")
    print(f"ROLES: {test_case['roles']}")

    print("\nANSWER:")
    print(answer)

    print("\nRETRIEVED CHUNKS:")

    for source in result["results"]:
        print(
            f"- {source['document']} — "
            f"{source['section']}"
        )

    if test_case["expected_behavior"] == "answer":

        assert len(result["results"]) > 0

        print("\nRESULT: PASS")


    elif test_case["expected_behavior"] == "do_not_answer":

        assert "i don't know" in answer.lower()

        print("\nRESULT: PASS")

for test_case in rag_evaluation_dataset:
    run_test(test_case)


