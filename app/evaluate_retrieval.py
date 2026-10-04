from evaluation_dataset import evaluation_dataset
from retriever import retrieve


def evaluate_question(test_case, top_k):

    question = test_case["question"]

    expected_document = test_case["expected_document"]
    expected_section = test_case["expected_section"]

    results = retrieve(
        question,
        roles=["developer", "architect", "security"],
        top_k=top_k
    )

    if expected_document is None:
        return {
            "question": question,
            "expected": None,
            "found": None,
            "passed": True
        }

    found = any(
        result["document"] == expected_document
        and result["section"] == expected_section
        for result in results
    )

    return {
        "question": question,
        "expected": f"{expected_document} / {expected_section}",
        "found": found,
        "passed": found
    }


def evaluate(top_k):

    print(f"\n=== Recall@{top_k} Evaluation ===")

    passed = 0
    answerable_questions = 0

    for test_case in evaluation_dataset:

        result = evaluate_question(
            test_case,
            top_k
        )

        print(f"\nQuestion: {result['question']}")

        if result["expected"] is None:
            print("Expected: No answer in documentation")
            print("Result:   Unknown question test")
            continue

        answerable_questions += 1

        print(f"Expected: {result['expected']}")
        print(f"Found:    {result['found']}")

        if result["passed"]:
            passed += 1

    recall = passed / answerable_questions

    print(f"\nRecall@{top_k}: {recall:.2%}")


evaluate(3)
evaluate(5)
