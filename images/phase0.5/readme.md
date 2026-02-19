Phase 0.5 is represented by the two separate functioning proof-of-concept programs main.py and dbtest.py

Whereas

main.py represents the Python -> Gemini communication pipeline, and
dbtest.py represents the Python -> Local SQL DB communication pipeline

Phase 0.5 succeeds in hiding the secrets in environment variables using the same method as the GeminiAPIToken from Phase0

Phase 0.5 also showed an interesting "feature" of the sample database which is that some fields contain binary image data. 

SQLdbQueryTest.png shows the functional local SQL database, populated with sample data and query-able via standard SQL queries, demonstrated with the statement "SELECT TOP 10 * FROM dbo.Employees;"
pythondbtest1.png shows the same query performed via a hardcoded function in python, returning the results to the terminal. 
pythondbtest2.png shows a "cleaner" output where we only show certain fields as an example but also the 

to do next: connect them all together (ie, Python -> Gemini -> SQL)
#look for a python package that makes the production of MCP toolbox functions easier#