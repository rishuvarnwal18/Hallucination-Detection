# ============================================================
# MAIN FILE
# Hallucination Detection System
# Detects:
# 1. Entity Hallucination
# 2. Intent Hallucination
# 3. Semantic Hallucination (Triple Verification)
# ============================================================

from entity_detection import entity_hallucination
from intent_detection import intent_hallucination
from semantic_detection import semantic_hallucination


# ============================================================
# Main detection function
# ============================================================

def detect_hallucination(paragraph, question, answer):

    # Entity Hallucination
    entity_h, bad_entities, entity_reason = entity_hallucination(paragraph, answer)

    # Intent Hallucination
    intent_h, bad_verbs, intent_reason = intent_hallucination(paragraph, answer)

    # Semantic Hallucination (Triple Verification)
    semantic_h, semantic_reason = semantic_hallucination(paragraph, answer)

    # Print report
    print("\n==============================")
    print(" HALLUCINATION REPORT")
    print("==============================\n")

    # Entity section
    print("Entity Hallucination:", entity_h)

    if entity_h:
        print("\nHallucinated Entities:")
        print(", ".join(bad_entities))

    print("\nReason:")
    print(entity_reason)

    print("\n------------------------------\n")

    # Intent section
    print("Intent Hallucination:", intent_h)

    if intent_h:
        print("\nHallucinated Intent:")
        print(", ".join(bad_verbs))

    print("\nReason:")
    print(intent_reason)

    print("\n------------------------------\n")

    # Semantic section
    print("Semantic Hallucination:", semantic_h)

    print("\nReason:")
    print(semantic_reason)

    print("\n==============================\n")


# ============================================================
# Continuous program loop
# ============================================================

def main():

    print("===================================")
    print(" Hallucination Detection System")
    print(" Type EXIT anytime to quit")
    print("===================================")

    while True:

        # Paragraph input
        paragraph = input("\nEnter Paragraph:\n")

        if paragraph.lower() == "exit":
            print("\nProgram terminated.")
            break

        # Question input
        question = input("\nEnter Question:\n")

        if question.lower() == "exit":
            print("\nProgram terminated.")
            break

        # Answer input
        answer = input("\nEnter Answer:\n")

        if answer.lower() == "exit":
            print("\nProgram terminated.")
            break

        # Run detection
        detect_hallucination(paragraph, question, answer)

        # Continue or exit
        choice = input("Check another example? (yes/no): ").lower()

        if choice != "yes":
            print("\nProgram terminated.")
            break


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()