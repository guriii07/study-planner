import json
from google import genai
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def chat_with_companion(user_message, chat_history):
    history_text = ""
    for msg in chat_history:
        role = "User" if msg['role'] == 'user' else "Companion"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""
    You are 'Study Cozy', an empathetic, Gen-Z AI study companion. You are a genius at computer science (like Java, DAA, OS) but act like a supportive friend.
    
    Here is the conversation so far:
    {history_text}
    User/System: {user_message}

    INSTRUCTIONS:
    1. Chat warmly and build a smart study schedule based on the topics and time they mention. 
    2. Extract the 'Goal Name' and 'Days Left' from the conversation. BE INTUITIVE: If they say "plan me a week to study Java", the name is "Java" and days left is 7. If they say "DAA exam in 3 days", name is "DAA" and days left is 3.
    3. The user can mark tasks as completed. If a message says "System Update: User completed...", cheer them on!
    4. If the user says they are falling behind or missed a day, recalculate the remaining topics into a new, stress-free schedule. Do not scold them.

    You MUST return ONLY a raw JSON object matching this exact structure:
    {{
      "reply": "Your conversational response.",
      "exam_metadata": {{
         "name": "Goal/Exam Name (e.g., Java Polymorphism)",
         "days_left": 7
      }},
      "has_schedule": true/false,
      "schedule": [
        {{
          "day": 1,
          "topics": ["Topic 1"],
          "estimated_hours": 2.5,
          "vibe": "Super short motivational note."
        }}
      ]
    }}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        raw_text = response.text.strip()
        if raw_text.startswith('```json'):
            raw_text = raw_text[7:]
        if raw_text.endswith('```'):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return {
            "reply": "My brain glitched for a second! 🌧️ Try that again?", 
            "exam_metadata": {"name": "TBD", "days_left": "-"},
            "has_schedule": False, 
            "schedule": []
        }