from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3
import streamlit as st
import google.generativeai as genai

from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain



# Initialize OpenAI with proper configuration
llm = ChatOpenAI(temperature=0.3, api_key=os.getenv("OPENAI_API_KEY"), model = 'gpt-3.5-turbo')

def openai_response(input_query, response, content):
    prompt_text = f"""
    You are an AI assistant trained to convert English questions into SQL queries for a given database with various tables and columns. Here’s how you should formulate the SQL queries based on the questions asked:

    - For counting the number of records in a table, you would write:
    Example: "How many entries of records are present in the student table?"
    SQL Query: SELECT COUNT(*) FROM student;

    - For querying specific data from a table based on a certain condition, you would write:
    Example: "Tell me all the students studying in the Data Science class."
    SQL Query: SELECT * FROM student WHERE class='Data Science';

    Remember, the SQL code should not include triple backticks (```) at the beginning or end, nor should it explicitly contain the word 'SQL' in the output. 
    Below is the question for which you need to generate an SQL query:
    
    Table schema: {response}
    
    Contents of the Table : {content}
    
    Input Query: {input_query}
    
    important notes
    Note1: Generate the commands in capital letters only.
    Note2: generate the command by understanding the table schema and table content
    for example if the user gives input generate the command by clearly understand the 
    contents of the table and Table schema of the table and mainly generate the commands
    in the capital letters only 
    Note 3: Generate only the command dont add anything to the command 
    """

    prompt = PromptTemplate(
        input_variables=['input_query', 'response', 'content'],
        template=prompt_text
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run({'input_query': input_query, 'response': response,'content' : content})

    return result

def get_table_info(table_name, db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        cursor.execute(f"SELECT * FROM {table_name};")
        content = cursor.fetchall()
    return schema, content

def sql_db(command, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(command)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows


# Setting up the Streamlit page
st.set_page_config(page_title="Advanced Database")
st.sidebar.title('Database Options')

# Database selection
db_options = {'Student': 'student.db', 'Faculty': 'faculty.db'}
database_choice = st.sidebar.selectbox('Select Database:', list(db_options.keys()))

if database_choice:
    db_path = db_options[database_choice]
    # Ensure the database keys are correctly referred
    tables = {'student.db': ['STUDENT', 'STUDENT2', 'STUDENT3'], 
              'faculty.db': ['FACULTY', 'FACULTY2', 'FACULTY3']}
    table_choice = st.sidebar.selectbox('Choose a Table:', tables[db_path])

    if table_choice:
        schema, content = get_table_info(table_choice, db_path)
        

# User query input
question = st.text_input("Input your question:")
submit = st.button("Ask the question")

if submit and question:
    if not schema or not content:
        st.error("Please select a table to query.")
    else:
        try:
            response_text = openai_response(question, schema, content)
            st.write("SQL Query:", response_text)
            
            # Execute and display SQL query results
            result = sql_db(response_text, db_path)
            st.subheader("Query Results:")
            for row in result:
                st.markdown(f"<h3 style='text-align: left; color: White;'>{row}</h3>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error executing query: {e}")
