from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from config import Config
from datetime import datetime
import json
import random

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# --- MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    mood_entries = db.relationship('MoodEntry', backref='author', lazy='dynamic')
    messages = db.relationship('ChatMessage', backref='author', lazy='dynamic')

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    role = db.Column(db.String(20)) # 'user' or 'assistant' or 'system'
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_crisis = db.Column(db.Boolean, default=False)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False) # 1-5 scale
    note = db.Column(db.String(500))
    tags = db.Column(db.String(200)) # stored as comma-separated string
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# --- ROUTES ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    moods = current_user.mood_entries.order_by(MoodEntry.timestamp.desc()).limit(15).all() # Increased limit for better analytics view
    
    # Analytics: Average Mood per Tag
    all_moods = current_user.mood_entries.all()
    tag_scores = {}
    tag_counts = {}
    
    for m in all_moods:
        if m.tags:
            # Split tags by comma, strip whitespace
            tags_list = [t.strip() for t in m.tags.split(',') if t.strip()]
            for tag in tags_list:
                tag = tag.lower() # Normalize case
                if tag not in tag_scores:
                    tag_scores[tag] = 0
                    tag_counts[tag] = 0
                tag_scores[tag] += m.score
                tag_counts[tag] += 1
                
    # Calculate averages
    analytics_labels = []
    analytics_data = []
    
    for tag in tag_scores:
        avg = tag_scores[tag] / tag_counts[tag]
        analytics_labels.append(tag.title())
        analytics_data.append(round(avg, 2))
        
    tag_analytics = {
        'labels': analytics_labels,
        'data': analytics_data
    }
    
    return render_template('dashboard.html', moods=moods, tag_analytics=tag_analytics)

@app.route('/log_mood', methods=['POST'])
@login_required
def log_mood():
    score = request.form.get('score')
    note = request.form.get('note')
    tags = request.form.get('tags')
    
    entry = MoodEntry(score=score, note=note, tags=tags, author=current_user)
    db.session.add(entry)
    db.session.commit()
    flash('Mood logged successfully!')
    return redirect(url_for('dashboard'))

@app.route('/chat')
@login_required
def chat():
    # Load last 50 messages
    history = current_user.messages.order_by(ChatMessage.timestamp.asc()).limit(50).all()
    return render_template('chat.html', history=history)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    data = request.json
    user_message = data.get('message', '')
    
    # Save User Message
    user_msg_db = ChatMessage(content=user_message, role='user', author=current_user)
    db.session.add(user_msg_db)
    db.session.commit()

    # 1. Safety / Crisis Check (Rule-based First Line of Defense)
    crisis_keywords = ['suicide', 'kill myself', 'hurt myself', 'end it all', 'die', 'overdose']
    if any(keyword in user_message.lower() for keyword in crisis_keywords):
        response_text = "CRITICAL: I'm very concerned about what you're saying. Please know that you're not alone. If you're in immediate danger, please call emergency services (911 in the U.S.) or the National Suicide Prevention Lifeline at 988. I am an AI and cannot provide professional help."
        
        ai_msg_db = ChatMessage(content=response_text, role='assistant', author=current_user, is_crisis=True)
        db.session.add(ai_msg_db)
        db.session.commit()
        
        return jsonify({
            'response': response_text,
            'is_crisis': True
        })

    # 2. OpenAI Integration
    try:
        from openai import OpenAI
        client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
        
        if not app.config['OPENAI_API_KEY']:
            return jsonify({
                'response': "System Error: OpenAI API Key not configured. Please check your settings.",
                'is_crisis': False
            })

        # Build Context (System prompt + last 10 messages)
        recent_history = current_user.messages.order_by(ChatMessage.timestamp.desc()).limit(10).all()
        recent_history.reverse() # Oldest to newest
        
        messages_payload = [
            {"role": "system", "content": "You are Claria, a compassionate, supportive, and non-judgmental mental health companion. Your goal is to listen, validate feelings, and offer gentle coping strategies. You are NOT a licensed therapist and should not diagnose or prescribe. If a user seems to be in severe distress, kindly suggest they seek professional help. Keep your responses concise (under 100 words), warm, and encouraging. Use a calm, soothing tone. Use logical markdown formatting like bolding for key terms."}
        ]
        
        for msg in recent_history:
            # We already added the current user message at the top of this function, 
            # so it might be in recent_history if we committed earlier.
            # However, we want to ensure we don't duplicate it if logic overlaps.
            # Simple approach: Trust the DB query.
            messages_payload.append({"role": "user" if msg.role == 'user' else "assistant", "content": msg.content})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_payload
        )
        
        ai_response = completion.choices[0].message.content
        
        # Save AI Response
        ai_msg_db = ChatMessage(content=ai_response, role='assistant', author=current_user)
        db.session.add(ai_msg_db)
        db.session.commit()
        
        return jsonify({
            'response': ai_response,
            'is_crisis': False
        })
        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        # Fallback responses if API fails
        fallback_responses = [
            "I'm having trouble connecting to my thought process right now, but I'm still here with you.",
            "I hear you, but I'm experiencing a technical hiccup. Please try again in a moment.",
            "It seems I can't reach the server. Just know that your feelings are valid."
        ]
        resp = random.choice(fallback_responses)
        ai_msg_db = ChatMessage(content=resp, role='assistant', author=current_user)
        db.session.add(ai_msg_db)
        db.session.commit()
        
        return jsonify({
            'response': resp,
            'is_crisis': False
        })

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
