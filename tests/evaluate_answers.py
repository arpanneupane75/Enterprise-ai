from app.rag.chains import ask_question
from tests.evaluation_dataset import EVALUATION_DATASET


def evaluate():
    total = len(EVALUATION_DATASET)

    answer_results = []

    for index, item in enumerate(EVALUATION_DATASET, start=1):

        question = item["question"]
        expected_answer = item["expected_answer"]

        print("\n" + "=" * 80)
        print(f"QUESTION {index}/{total}")
        print("=" * 80)
        print(question)

        try:
            result = ask_question(question)

            print("\nGENERATED ANSWER:")
            print(result.answer)

            print("\nEXPECTED ANSWER:")
            print(expected_answer)

            print("\nSOURCES:")
            for source in result.sources:
                print(
                    f"- {source.source} | "
                    f"Page {source.page} | "
                    f"Chunk {source.chunk_id}"
                )

            answer_results.append(
                {
                    "question": question,
                    "generated_answer": result.answer,
                    "expected_answer": expected_answer,
                    "sources": result.sources,
                }
            )

        except Exception as exc:
            print("\nERROR:")
            print(exc)

            answer_results.append(
                {
                    "question": question,
                    "generated_answer": None,
                    "expected_answer": expected_answer,
                    "sources": [],
                    "error": str(exc),
                }
            )

    successful = sum(
        1
        for result in answer_results
        if result["generated_answer"] is not None
    )

    print("\n" + "=" * 80)
    print("ANSWER GENERATION RESULTS")
    print("=" * 80)

    print(
        f"Successful answers: "
        f"{successful}/{total} "
        f"({successful / total:.2%})"
    )


if __name__ == "__main__":
    evaluate()