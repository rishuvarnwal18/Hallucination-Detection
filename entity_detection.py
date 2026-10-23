from nlp_utils import extract_entities, normalize


def entity_hallucination(paragraph, answer):

    para_entities = extract_entities(paragraph)
    answer_entities = extract_entities(answer)

    normalized_para = [normalize(e) for e in para_entities]

    hallucinated = []

    for entity in answer_entities:

        if normalize(entity) not in normalized_para:
            hallucinated.append(entity)

    if hallucinated:

        reason = (
            f'Out-of-context entity detected: "{", ".join(hallucinated)}".\n'
            f'This entity is not present in the paragraph.'
        )

        return True, hallucinated, reason

    return False, [], "All entities are grounded in the paragraph."