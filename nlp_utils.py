import spacy

# Load NLP model once
nlp = spacy.load("en_core_web_sm")


def extract_entities(text):

    doc = nlp(text)

    return [ent.text.strip() for ent in doc.ents]


def normalize(text):

    return text.lower().replace("inc.", "").replace("inc", "").strip()


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