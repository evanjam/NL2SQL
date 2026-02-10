import os #need this to get the env variable from OS
from google import genai #need this to use the genai client.models.generate_content() 

#define a function to pass a string as a prompt to Gemini
def prompt_gemini(prompt: str) -> str: #type hint, this function returns a string
    api_key = os.getenv("GeminiKey") #gets our GeminiAPIKey from OS env variable
    if not api_key:
        raise RuntimeError("GeminiKey environment variable is missing")

    client = genai.Client(api_key=api_key) #thisis my authenticated connection to Gemini

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return resp.text or "" #resp can contain other data which we are ignoring for now by just returning it as plain text

#entry point of program
def main():
    while True:
        user_input  = input("Enter prompt to be sent to Gemini: (or type quit/exit)\n").strip()
        if user_input.lower() in {'exit', "quit"}:
            break

        response = prompt_gemini(user_input)
        print("\nGemini's response: " + response)
        
main()