from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from logic.preprocess import preprocess, expand_genz_language, correct_common_spelling
from logic.domain_check import is_domain_valid
from logic.wh_detection import detect_wh_word
from logic.intent_match import match_intent
from response.answer_builder import build_response
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({
                'error': 'No message provided',
                'response': 'Please type a question.'
            }), 400
        
        original_input = user_input
        expanded_input = expand_genz_language(user_input)
        corrected_input = correct_common_spelling(expanded_input)
        
        correction_made = corrected_input.lower() != original_input.lower()
        correction_type = None
        
        if correction_made:
            if expanded_input.lower() != original_input.lower():
                correction_type = "genz"
            elif corrected_input.lower() != expanded_input.lower():
                correction_type = "spelling"
        
        wh_word = detect_wh_word(corrected_input)
        words = preprocess(corrected_input)
        
        # IMPROVED: Pass original corrected input to domain validation
        if not is_domain_valid(words, corrected_input):
            return jsonify({
                'response': 'I can answer only questions related to Spheruler Solutions. Please ask about our company, products, services, patents, founders, or location.',
                'error': 'out_of_domain'
            })
        
        intent, score = match_intent(words, wh_word)
        
        if intent is None or score == 0:
            return jsonify({
                'response': 'I could not clearly understand your question. Please try asking about our products, services, patents, founders, location, or company information.',
                'error': 'no_intent'
            })
        
        response = build_response(intent, wh_word)
        
        result = {
            'response': response.get('answer', response.get('message', '')),
            'followups': response.get('followups', []),
            'has_image': response.get('has_image', False),
            'image_type': response.get('image_type', None),
            'link': response.get('link', None),
            'link_label': response.get('link_label', None)
        }
        
        # Add image URLs — supports multiple images (e.g. both Indian & US patents)
        if result['has_image']:
            image_files = response.get('image_files', ['patent_diagram.png'])
            base_url = 'http://localhost:5000/api/images/'
            result['image_urls'] = [base_url + f for f in image_files]
            # Keep legacy single image_url pointing to first image for backwards compat
            result['image_url'] = result['image_urls'][0] if result['image_urls'] else None

        
        if correction_made:
            result['corrected'] = corrected_input
            result['correction_type'] = correction_type
            result['original'] = original_input
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'server_error',
            'response': 'An error occurred while processing your request. Please try again.'
        }), 500


@app.route('/api/images/<filename>', methods=['GET'])
def serve_image(filename):
    """Serve patent images"""
    try:
        images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
        return send_from_directory(images_dir, filename)
    except Exception as e:
        print(f"Error serving image: {str(e)}") 
        return jsonify({'error': 'Image not found'}), 404


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Chatbot API is running'})


if __name__ == '__main__':
    print("🚀 Chatbot API Server Starting...")
    print("📡 Server running on http://localhost:5000")
    print("💬 Frontend can connect to http://localhost:5000/api/chat")
    print("🖼️  Images available at http://localhost:5000/api/images/")
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)