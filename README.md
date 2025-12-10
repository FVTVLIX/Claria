# CLARIA

### Align Your Mind.

Claria is a holistic mental health companion designed to provide a sanctuary for self-reflection, emotional tracking, and immediate support. Unlike traditional journaling apps that merely record data, Claria acts as an interactive mirror, helping you understand the constellation of your emotions through analytics, AI-assisted guidance, and curated professional resources.

---

## The Claria Effect

Understanding the impact of Claria requires looking at the journey of two distinct paths:

### Without Claria
For many, managing mental health is a fragmented and isolating experience. Emotions are felt but rarely understood; patterns remain hidden in the chaos of daily life. A person might feel overwhelmed by anxiety on Tuesdays but never realize it stems from a recurring Monday work meeting. When crises strike, they scramble to find phone numbers or coping mechanisms, often feeling paralyzed by the lack of immediate, judgment-free support. The journey is often reactive—dealing with the storm only after it has already caused damage.

### With Claria
The Claria user creates a living map of their inner world. By logging moods and tagging specific triggers, they begin to see the invisible threads connecting their experiences. That Tuesday anxiety is no longer a mystery; it is a data point that allows them to prepare grounding techniques in advance. When they feel unheard, The Oracle provides an immediate, compassionate ear 24/7. When panic rises, the Grounding module offers instant, actionable steps to return to center. The journey becomes proactive—building resilience and self-awareness before the storm hits.

---

## Core Modules

### 1. Mood Tracking & Analytics
Claria moves beyond simple "good" or "bad" days. Users log their emotional state on a granular scale, adding context through notes and tags. The Dashboard wraps this data in a sophisticated analytics engine, visualizing emotional trends over time. This allows users to identify specific triggers, track improvements, and objectively view their mental health progression.

### 2. The Oracle
At the heart of Claria lies The Oracle—an advanced AI companion powered by OpenAI. It is fine-tuned to listen without judgment, validate feelings, and offer gentle, non-medical coping strategies. It serves as a first line of support for those moments when speaking to another human feels too difficult or inaccessible. It includes built-in safety rails to detect crisis keywords and direct users to professional emergency services immediately.

### 3. The Grimoire
A comprehensive library of mental health knowledge. The Grimoire contains professional resources, crisis hotlines, and educational materials. It serves as a reference point for users to learn about their conditions, find external help, and build a toolkit of long-term coping strategies.

### 4. Grounding
A specialized module designed for immediate intervention. When a user is overwhelmed, the Grounding section provides rapid-access techniques (such as the 5-4-3-2-1 method, box breathing, and sensory awareness exercises) to de-escalate panic and anchor the mind in the present moment.

---

## Design Philosophy

Information without aesthetics can be sterile and uninviting. Claria is built on the belief that the environment in which you heal matters. The interface utilizes a "Paper & Ink" aesthetic—tactile, organic, and grounded.

- **Visuals**: High-contrast typography (Space Mono, Inter), organic "torn paper" dividers, and calming sine-wave animations.
- **Interaction**: Micro-interactions and floating elements create a sense of life and fluidity, reminding the user that mental health is a dynamic, not static, process.
- **Accessibility**: High readability and clear navigation ensure that users in distress can find what they need without friction.

---

## Technical Stack

Claria is built on a robust, lightweight stack designed for reliability and ease of deployment.

- **Backend**: Python / Flask
- **Database**: SQLite (via SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3 (Custom Design System), Vanilla JavaScript
- **AI Integration**: OpenAI API (GPT-3.5 Turbo)
- **Visualization**: Chart.js

---

## Installation & Setup

Follow these steps to deploy Claria locally.

### Prerequisites
- Python 3.8 or higher
- pip (Python Package Installer)
- An OpenAI API Key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/claria.git
cd claria
```

### 2. Set Up Virtual Environment
It is highly recommended to run Claria in an isolated environment.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory to store your secrets.
```bash
touch .env
```
Add the following configuration to `.env`:
```text
SECRET_KEY=your-secure-secret-key
DATABASE_URL=sqlite:///app.db
OPENAI_API_KEY=your-openai-api-key-here
```

### 5. Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the Application
```bash
python app.py
```
Access the application at `http://127.0.0.1:5000`.

---
