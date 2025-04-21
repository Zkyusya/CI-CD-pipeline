from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
import os
import logging

app = Flask(__name__)
CORS(app)

# Initialize Firestore client
db = firestore.Client()

def get_response(user_message):
    """Simple response logic - can be expanded with more complex NLP"""
    user_message = user_message.lower().strip()
    
    # Default responses
    responses = {
        "hi": "Hello! Welcome to University Helpdesk. How can I assist you today?",
        "hello": "Hello! Welcome to University Helpdesk. How can I assist you today?",
        "courses": "We offer undergraduate and postgraduate programs in various fields. Visit our academics page for details.",
        "admission": "Admission requirements vary by program. Please check our admissions portal for specific criteria.",
        "contact": "You can reach us at info@university.edu or call +1 (555) 123-4567.",
        "location": "Our main campus is located at 123 University Avenue, Education City.",
        "hours": "Our visitor center is open Monday-Friday, 9AM-5PM.",
        "default": "I'm sorry, I didn't understand that. Could you rephrase or ask about admissions, courses, contact info, or location?"
    }
    
    # Check for keywords
    for keyword in responses:
        if keyword in user_message and keyword != "default":
            return responses[keyword]
    
    return responses["default"]

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Get response
        bot_response = get_response(user_message)
        
        # Log conversation to Firestore
        chat_ref = db.collection('conversations').document(session_id)
        chat_ref.set({
            'last_message': user_message,
            'last_response': bot_response,
            'timestamp': firestore.SERVER_TIMESTAMP
        }, merge=True)
        
        return jsonify({
            'response': bot_response,
            'session_id': session_id
        })
    
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))