import pyodbc
import os

DRIVER_NAME = "ODBC Driver 18 for SQL Server"
SERVER = os.getenv("NorthwindSVR")
DATABASE = os.getenv("NorthwindDB")
USER = os.getenv("NorthwindUID")    
PASSWORD = os.getenv("NorthwindPWD")

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
    #cur.execute("SELECT TOP 1 * FROM Employees")
    cur.execute("""
    SELECT TOP (10)
        EmployeeID,
        FirstName,
        LastName,
        Title,
        City,
        Country
    FROM dbo.Employees
    ORDER BY EmployeeID
    """)
    rows = cur.fetchall()

print(f"Returned {len(rows)} rows.")
for row in rows:
    print(row)