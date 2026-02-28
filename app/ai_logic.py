import json
from google import genai
from google.genai import types  # <-- Add this import for the config types
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def chat_with_companion(user_message, chat_history, daily_hours):
    history_text = ""
    for msg in chat_history:
        role = "User" if msg['role'] == 'user' else "Companion"
        history_text += f"{role}: {msg['content']}\n"

    # Notice I removed the massive JSON schema from the prompt text
    # because Gemini will handle it natively now!
    prompt = f"""
    You are 'Study Cozy', an empathetic, Gen-Z AI study companion. You are a genius at computer science (like Java, DAA, OS) but act like a supportive friend.
    
    CRITICAL RULE: The user has a STRICT daily study capacity of {daily_hours} hours. You MUST NOT schedule more than {daily_hours} hours of studying on any single day in the schedule array. Break topics across multiple days if needed to stay under this limit.

    Here is the conversation so far:
    {history_text}
    User/System: {user_message}

    INSTRUCTIONS:
    1. Chat warmly and build a smart study schedule based on the topics and time they mention. 
    2. Extract the 'Goal Name' and 'Days Left' from the conversation. BE INTUITIVE: If they say "plan me a week to study Java", the name is "Java" and days left is 7. If they say "DAA exam in 3 days", name is "DAA" and days left is 3.
    3. The user can mark tasks as completed. If a message says "System Update: User completed...", cheer them on!
    4. If the user says they are falling behind or missed a day, recalculate the remaining topics into a new, stress-free schedule. Do not scold them.
    
    Output strictly as a JSON object with keys: "reply" (string), "exam_metadata" (object with "name" and "days_left"), "has_schedule" (boolean), and "schedule" (array of objects with "day", "topics", "estimated_hours", and "vibe").
    """

    try:
        # The Magic Sauce: Force the model to return valid JSON automatically
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        # Look how clean this is! No more .replace() or slicing!
        return json.loads(response.text)
        
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return {
            "reply": "My brain glitched for a second! 🌧️ Try that again?", 
            "exam_metadata": {"name": "TBD", "days_left": "-"},
            "has_schedule": False, 
            "schedule": []
        }