from app.rag.chains import retrieve_documents
from tests.evaluation_dataset import EVALUATION_DATASET


def evaluate():
    total = len(EVALUATION_DATASET)

    hit_at_1 = 0
    hit_at_3 = 0
    reciprocal_ranks = []

    for item in EVALUATION_DATASET:

        question = item["question"]
        expected_pages = set(
            item["expected_pages"]
        )

        results = retrieve_documents(
            question,
            candidate_k=10,
            final_k=3,
        )

        retrieved_pages = [
            document.metadata.get("page")
            for document, _score in results
        ]

        # -----------------------------
        # Hit@1
        # -----------------------------

        hit1 = (
            len(retrieved_pages) >= 1
            and retrieved_pages[0] in expected_pages
        )

        # -----------------------------
        # Hit@3
        # -----------------------------

        hit3 = any(
            page in expected_pages
            for page in retrieved_pages[:3]
        )

        # -----------------------------
        # MRR
        # -----------------------------

        rr = 0.0

        for rank, page in enumerate(
            retrieved_pages,
            start=1,
        ):
            if page in expected_pages:
                rr = 1 / rank
                break

        # -----------------------------
        # Update metrics
        # -----------------------------

        if hit1:
            hit_at_1 += 1

        if hit3:
            hit_at_3 += 1

        reciprocal_ranks.append(rr)

        # -----------------------------
        # Print question result
        # -----------------------------

        print("\nQuestion:")
        print(question)

        print(
            "Expected pages:",
            sorted(expected_pages),
        )

        print(
            "Retrieved pages:",
            retrieved_pages,
        )

        print(
            f"Hit@1: "
            f"{'YES' if hit1 else 'NO'}"
        )

        print(
            f"Hit@3: "
            f"{'YES' if hit3 else 'NO'}"
        )

        print(
            f"Reciprocal Rank: {rr:.3f}"
        )

    # -----------------------------
    # Final metrics
    # -----------------------------

    mrr = (
        sum(reciprocal_ranks) / total
        if total
        else 0.0
    )

    print(
        "\n================ RESULTS ================\n"
    )

    print(
        f"Hit@1: "
        f"{hit_at_1}/{total} "
        f"({hit_at_1 / total:.2%})"
    )

    print(
        f"Hit@3: "
        f"{hit_at_3}/{total} "
        f"({hit_at_3 / total:.2%})"
    )

    print(
        f"MRR: {mrr:.3f}"
    )


if __name__ == "__main__":
    evaluate()