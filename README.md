# Advanced Database Query Assistant

This application is an advanced tool designed to assist users in querying databases by converting natural language questions into SQL queries. It utilizes Streamlit for the user interface, SQLite for database interactions, and OpenAI's GPT-3.5-turbo model to generate SQL queries from English text.

## Features

- **Interactive Web Interface**: Built with Streamlit, providing a user-friendly web interface.
- **Support for Multiple Databases**: Handles multiple predefined databases with the ability to select different tables.
- **Natural Language to SQL**: Uses OpenAI's language model to convert natural language queries into SQL commands.
- **Real-time SQL Execution**: Executes the generated SQL queries and displays the results.

## How It Works

### Database and Table Selection

- Users select a database and a table from the sidebar. Supported databases include 'Student' and 'Faculty', each containing multiple tables.

### Query Input

- Users input their question in natural language format. For example, "How many entries are in the student table?"

### SQL Generation and Execution

- The application uses the OpenAI model to generate a SQL query based on the user's natural language question.
- The generated SQL is executed against the selected database table, and the results are displayed on the interface.

## Components

### OpenAI Integration

- **Language Model**: Utilizes OpenAI's GPT-3.5-turbo model configured to generate SQL queries from English descriptions.
- **Custom Prompts**: The model is prompted with specific instructions to ensure the SQL commands are generated in capital letters and are based on the table schema and contents.

### SQLite Database Management

- **Schema and Content Fetching**: Retrieves the schema and content of the selected table to inform the model about the database structure.
- **SQL Execution**: Executes the generated SQL queries against the SQLite database and fetches the results.

### Streamlit Web Interface

- **Sidebar for Options**: Allows users to choose the database and table they want to query.
- **Input and Button**: A text input for the query and a button to submit the question.
- **Results Display**: Outputs both the generated SQL query and the query results.
