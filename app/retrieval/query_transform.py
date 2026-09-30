def transform_query(question: str) -> str:
    question_lower = question.lower()

    if "headquarters" in question_lower:
        return (
            "Headquarters (U.S.) employees. "
            "Employee leave and sick leave policy. "
            + question
        )

    if "international employees" in question_lower:
        return (
            "International employees. "
            "Employee leave and sick leave policy. "
            + question
        )

    return question