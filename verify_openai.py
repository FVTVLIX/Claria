import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')

print(f"Checking for API Key...")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in environment or .env file.")
    exit(1)

print(f"API Key found (starts with {api_key[:7]}...)")

client = OpenAI(api_key=api_key)

print("Attempting to connect to OpenAI...")
try:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello! Are you working?"}
        ]
    )
    print("SUCCESS! OpenAI responded:")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"ERROR: Failed to connect to OpenAI.")
    print(e)
