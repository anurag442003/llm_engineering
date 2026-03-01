import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {'Yes' if api_key else 'No'}")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

try:
    response = model.generate_content("Hello, this is a test.")
    print("Success:", response.text)
except Exception as e:
    print("Error:", e)