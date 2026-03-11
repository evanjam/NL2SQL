import os
import pyodbc
from google import genai
from google.genai import types

#----------
#Database Layer
#----------

def run_query(sql: str) -> list[dict]:
    # connect
    # execute
    # return rows as list of dicts
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

def list_tables() -> str:
    # hardcoded SQL
    # call run_query()
    sql = """
    SELECT
        t.name AS TableName
    FROM sys.tables t
    ORDER BY t.name;    
    """

    rows = run_query(sql)

    table_names = [row["TableName"] for row in rows]

    return ", ".join(table_names)

def describe_table(table_name: str) -> str:
    allowed_tables = list_tables().split(", ")
    if table_name not in allowed_tables:
        return f"Table '{table_name}' not found."
    
    sql = f"""
    SELECT
       COLUMN_NAME,
       DATA_TYPE,
       IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}'
    ORDER BY ORDINAL_POSITION;
    """

    rows = run_query(sql)

    if not rows:
        return f"No columns found for table '{table_name}'."
    
    lines = [f"Schema for {table_name}:"]
    for row in rows:
        lines.append(
            f"{row['COLUMN_NAME']} {row['DATA_TYPE']} NULLABLE={row['IS_NULLABLE']}"
        )

    return "\n".join(lines)

def sample_table_rows(table_name: str, n: int = 5) -> str:
    allowed_tables = list_tables().split(", ")
    if table_name not in allowed_tables:
        return f"Table '{table_name}' not found."
    
    if n < 1:
        n = 1
    if n > 10:
        n = 10

    #get columns from schema and drop Photo column
    schema = run_query(f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION                   
    """)

    columns = [
        row["COLUMN_NAME"]
        for row in schema
        if row["COLUMN_NAME"] not in {"Photo"}
    ]

    column_list = ", ".join(columns)

    sql = f"""
    SELECT TOP ({n}) {column_list}
    FROM dbo.[{table_name}]
    """

    rows = run_query(sql)

    if not rows:
        return f"No rows found in table '{table_name}'."
    
    lines = [f"Sample rows from {table_name}:"]
    for row in rows:
        lines.append(str(row))

    return "\n".join(lines)

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
    api_key = os.getenv("GeminiKey")
    if not api_key:
        raise RuntimeError("GeminiKey environment variable is missing")
    
    client = genai.Client(api_key=api_key)

    #"chat" is just our own container including client+conversation history
    return {
        "client": client,
        "history": []
    }

def send_message(chat, user_text: str) -> str:
    chat["history"].append(user_text)

    resp = chat["client"].models.generate_content(
        model="gemini-2.5-flash",
        contents=chat["history"],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            tools=[list_tables, describe_table, sample_table_rows],
            temperature=0,
        ),
    )

    #keep the conversation going
    if resp.text:
        chat["history"].append(resp.text)

    return resp.text or ""

#----------
#Entry Point
#----------

def main():
    chat = create_chat()

    while True:
        user_input  = input("Enter prompt to be sent to Gemini: (or type quit/exit)\n").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        response = send_message(chat, user_input)
        print("\n" + response + "\n")

if __name__ == "__main__":
    main()

#TEMP TEST BLOCK: demonstrate the tool wrapper works correctly and put the describe_table tool to use
#if __name__ == "__main__":
#    print(describe_table("Employees"))

#TEMP TEST BLOCK:
#if __name__ == "__main__":
#    print(sample_table_rows("Employees", 1))