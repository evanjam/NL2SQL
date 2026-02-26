import os
import pyodbc
from google import genai

#----------
#Database Layer
#----------

def run_query(sql: str) -> list[dict]:
    # connect
    # execute
    # return rows as list of dicts
    # mostly in the dbtest.py proof of concept
    DRIVER_NAME = "ODBC Driver 18 for SQL Server"
    SERVER = os.getenv("NorthwindSVR")
    DATABASE = os.getenv("NorthwindDB")
    USER = os.getenv("NorthwindUID")
    PASSWORD = os.getenv("NorthwindPWD")

    if not all([SERVER, DATABASE, USER, PASSWORD]):
        raise RuntimeError("Database environment variables are not set properly.")
    
    conn_str = (
    f"DRIVER={{{DRIVER_NAME}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USER};"
    f"PWD={PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)
    
    with pyodbc.connect(conn_str) as conn:
        cur = conn.cursor()
        cur.execute(sql)

        columns = [column[0] for column in cur.description]
        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))

        return results

def list_tables() -> list[dict]:
    # hardcoded SQL
    # call run_query()
    sql = """
    SELECT
        s.name AS SchemaName,
        t.name AS TableName,
        t.create_date AS CreatedDate
    FROM sys.tables t
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_ID
    ORDER BY s.name, t.name;    
    """
    return run_query(sql)

#----------
#Gemini Layer
#----------

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

#----------
#Entry Point
#----------

def main():
    chat = create_chat()

    while True:
        user_input  = input("Enter prompt to be sent to Gemini: (or type quit/exit)\n").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        response = chat.send_message(user_input)
        print(response.text)

#TEMP TEST BLOCK: python can still execute sql (whew)
if __name__ == "__main__":
    data = run_query("""
        SELECT TOP (5)
            EmployeeID,
            FirstName,
            LastName
        FROM dbo.Employees
    """)
    print(data)

#TEMP TEST BLOCK2: demonstrate the tool wrapper works correctly and put the list_tables() tool to use
if __name__ == "__main__":
    data = list_tables()
    for row in data[:10]:
        print(row)