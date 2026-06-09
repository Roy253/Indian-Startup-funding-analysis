import pandas as pd
import sqlite3

conn = sqlite3.connect(
    "database/startup_funding.db"
)

df = pd.read_sql(
    "SELECT * FROM funding",
    conn
)

df.to_csv(
    "reports/dashboard_data.csv",
    index=False
)

print("Dashboard Data Exported")

conn.close()