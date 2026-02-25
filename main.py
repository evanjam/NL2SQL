import os
import pyodbc
from google import genai

#Database Layer

def run_query(sql: str) -> list[dict]:
    # connect
    # execute
    # return rows as list of dicts
    # mostly in the dbtest.py proof of concept
    pass

def list_tables() -> list[dict]:
    # hardcoded SQL
    # call run_query()
    pass

#Gemini Layer

SYSTEM_INSTRUCTIONS = """
You are a database assistant.
You have access to tools.
Always call tools instead of guessing.
"""

def create_chat():
    # instantiate model with tools=[list_tables]
    # enable automatic function calling
    # evolved version of phase0's "prompt_gemini" function that's used to instantiate persistent chats instead of sending one-off 1:1 prompt->response
    pass

#Entry Point

def main():
    chat = create_chat()

    while True:
        user_input  = input("Enter prompt to be sent to Gemini: (or type quit/exit)\n").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        response = chat.send_message(user_input)
        print(response.text)