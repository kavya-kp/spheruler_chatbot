def build_response(intent, wh_word):
    if intent is None:
        return {
            "type": "error",
            "message": "I could not clearly understand your question. Please rephrase."
        }

    # Normalize WH-word
    wh_word = wh_word.lower() if wh_word else "unknown"

    # Try to get WH-specific answer (what / why / how / where)
    answer = intent.get(wh_word)

    # Fallback to 'what' if specific WH answer is missing
    if answer is None:
        answer = intent.get("what")

    # If still no answer, respond safely
    if answer is None:
        return {
            "type": "error",
            "message": "I do not have enough information to answer that question."
        }

    # Check if this intent has an image (like patent diagram)
    has_image = intent.get("image") == "Yes, patent diagram available for display"

    response = {
        "type": "text",
        "answer": answer,
        "followups": intent.get("followups", [])
    }

    # Add image flag if available — supports both IMAGE_FILES (multi) and IMAGE_FILE (single)
    if has_image:
        response["has_image"] = True
        response["image_type"] = "patent_diagram"

        image_files_raw = intent.get("image_files", "")
        if image_files_raw:
            files = [f.strip() for f in image_files_raw.split(",") if f.strip()]
            response["image_files"] = files
        else:
            single = intent.get("image_file", "patent_diagram.png")
            response["image_files"] = [single]

    # Add link if available
    link = intent.get("link")
    if link:
        response["link"] = link
        response["link_label"] = intent.get("link_label", "Visit Website")

    return response