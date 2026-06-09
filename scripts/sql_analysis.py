import pandas as pd
import sqlite3

conn = sqlite3.connect(
    "database/startup_funding.db"
)

# Query 1
query = """
SELECT COUNT(*) AS Total_Records
FROM funding
"""

result = pd.read_sql(query, conn)

print(result)

# Query 2
query = """
SELECT
SUM(InvestmentAmount_USD) AS Total_Funding
FROM funding
"""

result = pd.read_sql(query, conn)

print(result)

# Query 3
query = """
SELECT
City,
SUM(InvestmentAmount_USD) AS Funding
FROM funding
GROUP BY City
ORDER BY Funding DESC
LIMIT 10
"""

result = pd.read_sql(query, conn)

print(result)


# Query 4
query = """
SELECT
    City,
    SUM(InvestmentAmount_USD) AS Funding
FROM funding
GROUP BY City
ORDER BY City ASC
"""
result = pd.read_sql(query, conn)
print("\nFUNDING BY CITY (ASCENDING)")
print(result)

# Query 5
query = """
SELECT
    CASE
        WHEN InvestmentType IN ('Series A', 'Series B')
        THEN 'Series A & B'
        ELSE InvestmentType
    END AS Funding_Type,

    SUM(InvestmentAmount_USD) AS Total_Funding

FROM funding

GROUP BY Funding_Type

ORDER BY Total_Funding DESC;


"""
result = pd.read_sql(query, conn)
print("\nFUNDING BY INVESTMENT TYPE")   
print(result)

# Query 6
query = """
SELECT
    CASE
        WHEN InvestmentType IN ('Series A', 'Series B')
        THEN 'Series A & B'
        ELSE InvestmentType
    END AS Funding_Type,

    COUNT(*) AS Total_Deals

FROM funding

GROUP BY Funding_Type

ORDER BY Total_Deals DESC;

"""
result = pd.read_sql(query, conn)
print("\nTOTAL DEALS BY INVESTMENT TYPE")
print(result)

# Query 7   
query = """
SELECT DISTINCT City
FROM funding
ORDER BY City;
"""
result = pd.read_sql(query, conn)
print("\nDISTINCT CITIES IN FUNDING DATA")
print(result)

# Query 8
query = """
SELECT
    City,
    SUM(InvestmentAmount_USD) AS Total_Funding
FROM funding
WHERE City IN (
    'Bengaluru',
    'Chennai',
    'Hyderabad'
)
GROUP BY City
ORDER BY Total_Funding DESC;
"""
result = pd.read_sql(query, conn)
print("\nFUNDING BY CITY (SELECTED CITIES)")
print(result)

# CLOSE ONLY AT THE END
conn.close()

print("SQL Analysis Completed")
