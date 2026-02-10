import os
from google import genai

def prompt_gemini(prompt: str) -> str:
    api_key = os.getenv("GeminiKey")
    if not api_key:
        raise RuntimeError("GeminiKey environment variable is missing")

    client = genai.Client(api_key=api_key)

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return resp.text or ""

def main():
    while True:
        user_input = input("Enter prompt to be sent to Gemini").strip()
        if user_input.lower() in {'exit', "quit"}:
            break

        response = prompt_gemini(user_input)
        print("\n")
        print(response)
        
main()