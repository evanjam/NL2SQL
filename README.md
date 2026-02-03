# NL2SQL
Intelligent Natural Language Interface for Relational Databases using Large Language Models (LLMS) and Model Context Protocol (MCP)

The project focuses on the development of a Natural Language to SQL (NL2SQL) interface. It will be designed to allow non-technical users to query complex relational databases using plain English. This project will operate within an internship capacity and entail significant software development, the application of new technologies like Large Language Models (specifically Google Gemini) and Agentic Function Calling Workflows. 

The core solution involves a Python-based program that facilitates bidirectional communication between the user, the Gemini API, and a local SQL server. By implementing a custom Model Context Protocol (MCP) “toolbox”, the system will enable the LLM to dynamically inspect database scheme, formulate syntactically correct SQL queries, and interpret raw data results into human-readable responses.  

The project will be built using a locally running SQL database populated with sample data from Microsoft’s provided “Northwind Traders” sample data, available at the following link: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/northwind-pubs 

The use of sample data does not affect the overall deliverable of the project and the endgoal would be to apply this system to an existing on-prem production SQL database that contains our employee data. The project doesn’t inherently contain anything specifically suited to the type of data that exists in the SQL database so it can hypothetically be integrated to any SQL database to provide this NL2SQL functionality. 

 

The Data Flow:  

    Input: The user inputs a natural language query into the Python interface 

    Contextualization: Python forwards the query + system context to Gemini 

    Tool Selection (MCP): Gemini analyzes the request and determines if it requires external data. If so, it requests the execution of specific tools (functions) defined in the “MCP Toolbox” (e.g., a function named getSchema or getTopTable) 

    Execution: The Python application acts as the execution agent, running the requested SQL queries against the database 

    Synthesis: Raw SQL results are fed back to Gemini, Gemini sythesizies the data to either (a) refine the query if the initial result was insufficient, or (b) generate the final natural language answer for the user. 

 

 

Architecture Diagram: 

[image.png]

Implementation Strategy (Phased Approach) 

Phase 0: Connect Python to Gemini.  

Goal: Establish the fundamental communication interface between a Python Program and Google Gemini API.  

Deliverable: A python-based terminal program where a user can enter a prompt that is sent to Google Gemini API, a certain amount of API tokens are consumed, and then results are returned in the terminal. 

 

Phase 1: Minimal MCP. 

Goal: Demonstrate the “toolbox” usage capability using “guided” prompts.  

In this phase, the system will utilize a limited “toolbox” of specific functions [e.g., getTopTable]. The user will provide explicitly detailed prompts that contain the necessary technical context [e.g., “Retrieve the top 5 records from the Employee table”]. 

This demonstrates the LLM’s ability to parse natural language, extract specific parameters (identifying “employee” as the target table and “5” as the limit), and map them to the correct tool in the MCP server. It proves that Python-to-Gemini-to-SQL pipeline is functional without yet requiring the model to “guess” or infer the database structure. 

Deliverable: A functional command loop where “tech-literate” prompts successfully trigger specific data retrieval functions and return appropriate and accurate data to the interface. 

 

Phase 2: Expand MCP 

Goal: Expand the system to handle generalized “user-esque” natural language by implementing dynamic SQL generation.  

The “handholding” of Phase 1 is eliminated allowing users to query using normal english language prompts that do not need to contain any special “tip offs” to help Gemini understand what tables to use, etc.  

This should include some expansion of the MCP toolbox to include more broad tools [e.g., getSchema or, runQuery] which will be used in a sort of reasoning loop to allow Gemini to recognize ambiguity and call appropriate functions to understand the data structure, identify relevant tables, and ultimately construct and execute a syntactically correct SQL query. 

Deliverable: An intelligent interface where the LLM independently navigates the database schema to answer novel questions. The gap between vague human intent and precise database logic is bridged. A question like “show me the employee with the highest salary” should be answered by asking for the schema, identifying the appropriate tables needed, and joining them via an SQL statement to answer the question.  

 

Phase 3: Scientific Analysis and Optimization 

Goal: Experimentation and refinement, application of the scientific method to optimize the English -> SQL process while, at the same time, minimizing the cost in terms of LLM API token consumption. E.g., we could give Gemini the entire database schema before every prompt, but that much context isn’t required to answer every question, and the result is overconsumption of LLM API tokens.  

This step will involve running a series of standardized tests where the same prompts will be used against different configurations to determine the minimal amount of context and complexity required in the MCP functions to return results that are still accurate.  

Deliverable: A final report detailing the trade-offs between model version intelligence, MCP functions, and operational cost (token consumption). 
