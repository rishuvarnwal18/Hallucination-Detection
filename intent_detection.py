from nlp_utils import extract_verbs


def intent_hallucination(paragraph, answer):

    para_verbs = extract_verbs(paragraph)
    answer_verbs = extract_verbs(answer)

    hallucinated = []

    for verb in answer_verbs:

        if verb not in para_verbs:
            hallucinated.append(verb)

    if hallucinated:

        reason = (
            f'Out-of-context intent detected: "{", ".join(hallucinated)}".\n'
            f'This relation is not supported by the paragraph.'
        )

        return True, hallucinated, reason

    return False, [], "Intent matches the paragraph."