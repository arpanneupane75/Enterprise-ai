from app.rag.chains import ask_question


def main():
    question = input("\nAsk a question: ")

    response = ask_question(question)

    print("\n================ ANSWER ================\n")
    print(response.answer)

    print("\n================ SOURCES ================\n")

    for source in response.sources:
        print(
            f"- {source.source} "
            f"(Page {source.page}, "
            f"Chunk {source.chunk_id}, "
            f"Score: {source.relevance_score})"
        )


if __name__ == "__main__":
    main()