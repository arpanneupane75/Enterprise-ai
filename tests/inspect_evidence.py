from app.ingestion.storage import load_chunks
from tests.evaluation_dataset import EVALUATION_DATASET


def inspect_evidence():
    chunks = load_chunks()

    for item in EVALUATION_DATASET:

        question = item["question"]
        expected_pages = set(item["expected_pages"])

        print("\n" + "=" * 80)
        print("QUESTION:")
        print(question)

        print(
            "\nEXPECTED PAGES:",
            sorted(expected_pages),
        )

        print("\nCANDIDATE CHUNKS:")

        for chunk in chunks:

            page = chunk.metadata.get("page")

            if page not in expected_pages:
                continue

            chunk_id = chunk.metadata.get(
                "chunk_id"
            )

            content = " ".join(
                chunk.page_content.split()
            )

            print(
                f"\n{chunk_id} | Page {page}"
            )

            print(content)


if __name__ == "__main__":
    inspect_evidence()