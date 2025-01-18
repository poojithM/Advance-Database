

import os
import sqlite3
import streamlit as st

# Connect to SQLite database
connection1 = sqlite3.connect("student.db")
cursor = connection1.cursor()


#Faculty database
connection2 = sqlite3.connect("Faculty.db")

fac_cursor = connection2.cursor()



drop_table_command = "DROP TABLE IF EXISTS student;"

# Execute the command
cursor.execute(drop_table_command)
connection1.commit() 




drop_faculty_command = "DROP TABLE IF EXISTS FACULTY;"

# Execute the command
fac_cursor.execute(drop_faculty_command)
connection2.commit() 


# Create table only if it doesn't exist to avoid errors on subsequent runs
cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(30),
    COURSE VARCHAR(30),
    SECTION VARCHAR(15),
    MARKS INT
)
""")

# Fix the SQL insertion syntax by ensuring all strings are properly quoted
cursor.execute("""
INSERT INTO STUDENT VALUES
    ('POOJITH', 'AI', 'A', 100),
    ('RYAN', 'PSYCOLOGY', 'A', 100),  
    ('MIKE', 'DATA SCIENCE', 'A', 100),
    ('ANDREW', 'ML', 'B', 90)
    
""")

# Commit the changes to the database
connection1.commit()

print("Inserted records are:")

# Correct the SELECT statement syntax
data = cursor.execute("SELECT * FROM STUDENT")

# Fetch all rows and print them
rows = data.fetchall()  # fetchall to ensure all rows are retrieved
for row in rows:
    print(row)

# Commit is not necessary after SELECT, but is good practice to close the connection
connection1.close()




fac_cursor.execute(
    """CREATE TABLE IF NOT EXISTS FACULTY (
    Name VARCHAR(30),
    SUBJECT VARCHAR(30),
    SALARY VARCHAR(15),
    DEPARTMENT VARCHAR(30)
)
    """
)

fac_cursor.execute(
    """
    INSERT INTO FACULTY VALUES
    ('RAMESH', 'DATA STRUCTURES', 5000, 'COMPUTER SCIENCE'),
    ('ZHOU', 'BIG DATA', 6000, 'BIO MEDICAL'),  
    ('SHA', 'PREDICTIVE MODELING', 8000, 'MATHIMATICAL'),
    ('LAURA', 'INTRODUCTION TO DATA SCIENCE', 8000, 'DATA SCIENCE')
    """
)

connection2.commit()

rows = fac_cursor.execute('SELECT * from FACULTY')

for row in rows.fetchall():
    print(row)


connection2.close()