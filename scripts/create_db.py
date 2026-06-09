import pandas as pd
import sqlite3

print("Loading Dataset...")

# Read cleaned CSV
df = pd.read_csv(
    "Data/cleaned_startup_funding.csv"
)

print("Dataset Loaded Successfully")
print("Rows:", len(df))

# Connect to database inside database folder
conn = sqlite3.connect(
    "database/startup_funding.db"
)

print("Database Connected")

# Create funding table and insert data
df.to_sql(
    "funding",
    conn,
    if_exists="replace",
    index=False
)

print("Data Inserted Successfully")

# Verify table creation
cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM funding"
)

rows = cursor.fetchone()[0]

print("Total Records in Database:", rows)

conn.close()

print("Database Created Successfully")