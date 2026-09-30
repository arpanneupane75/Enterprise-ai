from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from ragas.llms import LangchainLLMWrapper

from app.rag.chains import ask_question, retrieve_documents
from app.rag.llm import get_llm
from app.retrieval.embeddings import get_embeddings
from tests.evaluation_dataset import EVALUATION_DATASET


def main():
    questions = []
    answers = []
    contexts = []
    references = []

    print("Running RAGAS evaluation...\n")

    for i, item in enumerate(EVALUATION_DATASET, start=1):
        question = item["question"]
        reference = item["expected_answer"]

        print(f"[{i}/{len(EVALUATION_DATASET)}] {question}")

        result = ask_question(question)
        retrieved_documents = retrieve_documents(question)

        questions.append(question)
        answers.append(result.answer)

        contexts.append([
            document.page_content
            for document, _score in retrieved_documents
        ])

        references.append(reference)

    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": references,
    })

    # Use existing Groq LLM
    evaluator_llm = LangchainLLMWrapper(get_llm())

    # Use existing HuggingFace embeddings
    evaluator_embeddings = get_embeddings()

    # Configure RAGAS metrics
    faithfulness.llm = evaluator_llm

    answer_relevancy.llm = evaluator_llm
    answer_relevancy.embeddings = evaluator_embeddings

    context_precision.llm = evaluator_llm

    context_recall.llm = evaluator_llm

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        embeddings=evaluator_embeddings,
    )

    print("\n" + "=" * 60)
    print("RAGAS RESULTS")
    print("=" * 60)

    print(result)


if __name__ == "__main__":
    main()