import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[Google API key not set]")
        return
    genai.configure(api_key=api_key)
    models = genai.list_models()
    print("Available Gemini models:")
    for model in models:
        print(model)

if __name__ == "__main__":
    main() 