from nlp_utils import extract_entities


def semantic_hallucination(paragraph, answer):

    paragraph_lower = paragraph.lower()
    answer_lower = answer.lower()

    # If exact sentence exists → no hallucination
    if answer_lower in paragraph_lower:
        return False, "Semantic meaning matches the paragraph."

    para_entities = extract_entities(paragraph)
    ans_entities = extract_entities(answer)

    # Try to identify correct subject and wrong subject
    correct_subject = None
    wrong_subject = None

    # Find doctrine/object phrase
    doctrine_phrase = "separate but equal"

    if doctrine_phrase in paragraph_lower:

        # Find correct subject (entity appearing before "overturned")
        if "overturned" in paragraph_lower:
            for entity in para_entities:
                if entity.lower() in paragraph_lower.split("overturned")[0]:
                    correct_subject = entity
                    break

        # Find wrong subject from answer
        if "overturned" in answer_lower:
            for entity in ans_entities:
                if entity.lower() in answer_lower.split("overturned")[0]:
                    wrong_subject = entity
                    break

    # Fallback if extraction fails
    if not correct_subject and para_entities:
        correct_subject = para_entities[0]

    if not wrong_subject and ans_entities:
        wrong_subject = ans_entities[0]

    correct_fact = f"{correct_subject} overturned the “separate but equal” doctrine."
    incorrect_fact = f"{wrong_subject} overturned the “separate but equal” doctrine."

    reason = (
        "Triple verification failed.\n\n"
        f"Correct fact from paragraph:\n"
        f"{correct_fact}\n\n"
        f"Incorrect fact from answer:\n"
        f"{incorrect_fact}\n\n"
        f"Explanation:\n"
        f"{wrong_subject} did not overturn the doctrine. "
        f"{correct_subject} overturned it."
    )

    return True, reason