from logic.preprocess import preprocess, expand_genz_language, correct_common_spelling
from logic.domain_check import is_domain_valid
from logic.wh_detection import detect_wh_word
from logic.intent_match import match_intent
from response.answer_builder import build_response


def chatbot():
    print("Chatbot is running. Type 'exit' to stop.\n")
    print("💡 Tip: I understand Gen Z language (y, u, r) and can handle typos!\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot stopped.")
            break

        # Store original input for comparison
        original_input = user_input

        # 0. Expand Gen Z language and correct spelling (before WH detection)
        expanded_input = expand_genz_language(user_input)
        corrected_input = correct_common_spelling(expanded_input)
        
        # Show correction if significant changes were made
        if corrected_input.lower() != original_input.lower():
            # Check if it's a Gen Z conversion
            if expanded_input.lower() != original_input.lower():
                print(f"💬 (Understood: '{corrected_input}')")
            # Check if it's a spelling correction
            elif corrected_input.lower() != expanded_input.lower():
                print(f"✓ (Corrected spelling: '{corrected_input}')")

        # 1. Detect WH-word BEFORE preprocessing (use corrected input)
        wh_word = detect_wh_word(corrected_input)

        # 2. Preprocess input (this will use the corrected input)
        words = preprocess(corrected_input)

        # 3. Domain validation
        if not is_domain_valid(words):
            print("Bot: I can answer only questions related to Spheruler Solutions.\n")
            continue

        # 4. Intent matching - NOW PASSES WH_WORD FOR BETTER MATCHING
        intent, score = match_intent(words, wh_word)

        # 5. Handle no-intent or weak intent
        if intent is None or score == 0:
            print("Bot: I could not clearly understand your question. Please be more specific.\n")
            continue

        # 6. Build WH-aware response
        response = build_response(intent, wh_word)

        # 7. Output response
        if response["type"] == "text":
            print("Bot:", response["answer"])
            
            # Display patent image if available
            if response.get("has_image"):
                print("\n📊 Patent Diagram Available:")
                print("   [Note: In a GUI version, the patent diagram would be displayed here]")
                print("   The diagram shows the Four-Circle Image Format structure.")
            
            if response.get("followups"):
                print("Bot: You may also ask about:", ", ".join(response["followups"]))
            print()
        else:
            print("Bot:", response["message"], "\n")


if __name__ == "__main__":
    chatbot()
