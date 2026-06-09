import pandas as pd
import sqlite3
from sklearn.linear_model import LinearRegression
import numpy as np

# Connect database
conn = sqlite3.connect(
    "database/startup_funding.db"
)

query = """
SELECT
Year,
SUM(InvestmentAmount_USD) AS Funding
FROM funding
GROUP BY Year
ORDER BY Year
"""

df = pd.read_sql(query, conn)

print(df)

# Features
X = df[["Year"]]

# Target
y = df["Funding"]

# Train Model
model = LinearRegression()

model.fit(X, y)

# Future Years
future_years = pd.DataFrame({
    "Year": [2026, 2027, 2028, 2029, 2030]
})

predictions = model.predict(
    future_years
)

future_years["Predicted_Funding"] = predictions

print("\nFuture Funding Forecast")
print(future_years)

query = """
SELECT
    Year,
    SUM(InvestmentAmount_USD) AS Funding
FROM funding
GROUP BY Year
ORDER BY Year
"""

result = pd.read_sql(query, conn)
print(result)

conn.close()