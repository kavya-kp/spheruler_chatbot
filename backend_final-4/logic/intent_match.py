import os

def load_intents():
    intents = []
    intent = {}

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data', 'intents.txt')

    with open(data_path, "r") as f:
        for line in f:
            line = line.strip()

            # Empty line means intent block ended
            if not line:
                if intent:
                    intents.append(intent)
                    intent = {}
                continue

            # Split only on first colon
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "INTENT":
                intent["name"] = value

            elif key == "KEYWORDS":
                intent["keywords"] = [k.strip() for k in value.split(",")]

            elif key == "FOLLOWUPS":
                intent["followups"] = [f.strip() for f in value.split(",")]

            else:
                # WHAT, WHY, HOW, WHERE, LINK, LINK_LABEL, IMAGE answers
                intent[key.lower()] = value

        # Append last intent if file doesn't end with blank line
        if intent:
            intents.append(intent)

    return intents


def match_intent(words, wh_word=None):
    """
    Match user input to the best intent with WH-word priority.
    
    Args:
        words: List of preprocessed words from user input
        wh_word: The detected WH-word (what/where/why/how/who)
    
    Returns:
        tuple: (best_intent, best_score)
    """
    intents = load_intents()
    best_intent = None
    best_score = 0

    for intent in intents:
        score = 0
        intent_keywords = intent.get("keywords", [])

        # Count keyword matches
        for word in words:
            if word in intent_keywords:
                score += 1
            # Check for partial matches or multi-word keywords
            else:
                for kw in intent_keywords:
                    if kw in word or word in kw:
                        score += 0.5
        
        # CRITICAL FIX: Give massive priority to WH-word matches
        if wh_word and wh_word != "unknown":
            if wh_word in intent_keywords:
                score += 5  # Strong boost for WH-word match
        
        # Update best intent if this score is higher
        if score > best_score:
            best_score = score
            best_intent = intent
        elif score == best_score and score > 0:
            # Prefer intent with fewer keywords (more specific)
            if best_intent and len(intent.get("keywords", [])) < len(best_intent.get("keywords", [])):
                best_intent = intent

    return best_intent, best_score