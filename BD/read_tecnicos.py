import os
import sqlite3

#conn = sqlite3.connect(r'C:\Users\JABA\Desktop\Coursera\SQL\exemplo.db')
#cur = conn.cursor()

# Get the current directory of your Python script
current_directory = os.path.dirname(os.path.abspath(__file__))
#print(current_directory)

# Define the sqlite file path and the sheet name
sqlite_file_name = 'ANI_DB.db' 

# Construct the full path to the SQLite file
file_path = os.path.join(current_directory, sqlite_file_name)
print(file_path)

conn = sqlite3.connect(file_path)
cur = conn.cursor()

# Retrieve data from the table T_TECNICO
cur.execute("SELECT * FROM T_TECNICO")
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()