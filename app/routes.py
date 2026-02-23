from flask import Blueprint, request, jsonify, render_template, send_from_directory
from app.models import StudyPlan
from app.ai_logic import chat_with_companion  # <-- The correct, updated import
from app import db
import json
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def landing():
    # The new aesthetic front door
    return render_template('landing.html')

@bp.route('/dashboard')
def dashboard():
    # The new Bento Box workspace
    return render_template('dashboard.html')

@bp.route('/api/chat', methods=['POST'])
def api_chat():
    # The new conversational endpoint
    data = request.json
    
    user_message = data.get('message')
    chat_history = data.get('history', []) 
    daily_hours = data.get('daily_hours', 3)
    
    if not user_message:
        return jsonify({'error': 'Message is empty'}), 400
        
    # Send the conversation to our newly upgraded Gemini brain
    ai_response = chat_with_companion(user_message, chat_history, daily_hours)
    
    return jsonify({
        'status': 'success',
        'data': ai_response
    }), 200

# --- PWA Routes ---
@bp.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@bp.route('/sw.js')
def serve_sw():
    # We must explicitly set the content type for service workers
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')