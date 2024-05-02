import sqlite3

# Create a database connection
conn = sqlite3.connect('mydatabase.db')  # Replace with your desired database name

# Create a cursor object
c = conn.cursor()

# Create a table (if it doesn't exist)
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE
                )''')

# Insert data into the table
c.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("admin", "admin@example.com"))
conn.commit()  # Save changes

# Select data from the table
c.execute("SELECT * FROM users")
rows = c.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[2]}")

# Update data in the table
c.execute("UPDATE users SET email = ? WHERE username = ?", ("new_email@example.com", "admin"))
conn.commit()

# Delete data from the table
c.execute("DELETE FROM users WHERE username = ?", ("admin",))
conn.commit()

# Close the connection
conn.close()
