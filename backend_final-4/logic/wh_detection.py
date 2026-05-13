def detect_wh_word(text):
    wh_words = ["what", "where", "why", "how", "who", "when"]

    text = text.lower()
    # First check for exact word matches (highest priority)
    words = text.lower().split()
    for wh in wh_words:
        if wh in words:
            return wh
            
    # Then check if it starts with the WH word (common in questions)
    for wh in wh_words:
        if text.lower().startswith(wh):
            return wh

    return "unknown"