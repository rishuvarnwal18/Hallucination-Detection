# ============================================================
# HALLUCINATION DETECTION MODEL (Continuous Mode)
# Detects:
# 1. Entity Hallucination
# 2. Intent Hallucination
# 3. Semantic Hallucination
# Runs until user chooses to exit
# ============================================================

import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


# ============================================================
# Extract Entities
# ============================================================

def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append(ent.text.strip())

    return entities


# ============================================================
# Normalize entity text
# ============================================================

def normalize(text):

    return text.lower().replace("inc.", "").replace("inc", "").strip()


# ============================================================
# Extract meaningful verbs (Intent)
# ============================================================

def extract_verbs(text):

    doc = nlp(text)

    verbs = []

    ignore_verbs = {
        "be", "have", "do",
        "is", "was", "were", "are", "am",
        "been", "being", "has", "had"
    }

    for token in doc:

        if (
            token.pos_ == "VERB"
            and token.dep_ != "aux"
            and token.lemma_.lower() not in ignore_verbs
            and token.is_alpha
        ):
            verbs.append(token.lemma_.lower())

    return list(set(verbs))


# ============================================================
# Entity Hallucination
# ============================================================

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

    else:

        return False, [], "All entities are grounded in the paragraph."


# ============================================================
# Intent Hallucination
# ============================================================

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

    else:

        return False, [], "Intent matches the paragraph."


# ============================================================
# Semantic Hallucination
# ============================================================

def semantic_hallucination(entity_h, intent_h, bad_entities, bad_verbs):

    if entity_h or intent_h:

        reasons = []

        if bad_entities:
            reasons.append(
                f'Entity "{", ".join(bad_entities)}" is out-of-context.'
            )

        if bad_verbs:
            reasons.append(
                f'Intent "{", ".join(bad_verbs)}" is out-of-context.'
            )

        reasons.append(
            "Entity–Intent combination does not match paragraph facts."
        )

        reason = "\n".join(reasons)

        return True, reason

    else:

        return False, "Semantic meaning matches the paragraph."


# ============================================================
# Detection Function
# ============================================================

def detect_hallucination(paragraph, question, answer):

    entity_h, bad_entities, entity_reason = entity_hallucination(paragraph, answer)

    intent_h, bad_verbs, intent_reason = intent_hallucination(paragraph, answer)

    semantic_h, semantic_reason = semantic_hallucination(
        entity_h, intent_h, bad_entities, bad_verbs
    )

    print("\n==============================")
    print(" HALLUCINATION REPORT")
    print("==============================\n")

    print("Entity Hallucination:", entity_h)

    if entity_h:
        print("\nHallucinated Entities:")
        print(", ".join(bad_entities))

    print("\nReason:")
    print(entity_reason)

    print("\n------------------------------\n")

    print("Intent Hallucination:", intent_h)

    print("\nReason:")
    print(intent_reason)

    print("\n------------------------------\n")

    print("Semantic Hallucination:", semantic_h)

    print("\nReason:")
    print(semantic_reason)

    print("\n==============================")


# ============================================================
# CONTINUOUS LOOP
# ============================================================

while True:

    print("\nEnter Paragraph (or type EXIT to quit):")
    paragraph = input()

    if paragraph.lower() == "exit":
        print("Program terminated.")
        break

    print("\nEnter Question:")
    question = input()

    print("\nEnter Answer:")
    answer = input()

    detect_hallucination(paragraph, question, answer)

    print("\nDo you want to check another example? (yes/no):")
    choice = input().lower()

    if choice != "yes":
        print("Program terminated.")
        break