import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect Database
conn = sqlite3.connect(
    "database/startup_funding.db"
)

print("Database Connected")

# =====================================================
# 1. Funding Trend by Year
# =====================================================

query = """
SELECT
    Year,
    SUM(InvestmentAmount_USD) AS Funding
FROM funding
GROUP BY Year
ORDER BY Year
"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(10,5))
plt.plot(df["Year"], df["Funding"], marker="o")

plt.title("Startup Funding Trend by Year")
plt.xlabel("Year")
plt.ylabel("Funding (USD)")

plt.tight_layout()

plt.savefig(
    "visuals/funding_trend.png"
)

plt.show()

# =====================================================
# 2. Top 10 Cities
# =====================================================

query = """
SELECT
    City,
    SUM(InvestmentAmount_USD) AS Funding
FROM funding
GROUP BY City
ORDER BY Funding DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(10,5))

plt.bar(
    df["City"],
    df["Funding"]
)

plt.title("Top 10 Cities by Funding")
plt.xlabel("City")
plt.ylabel("Funding (USD)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "visuals/top_cities.png"
)

plt.show()

# =====================================================
# 3. Top 10 Industries
# =====================================================

query = """
SELECT
    Industry,
    SUM(InvestmentAmount_USD) AS Funding
FROM funding
GROUP BY Industry
ORDER BY Funding DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(12,6))

plt.bar(
    df["Industry"],
    df["Funding"]
)

plt.title("Top 10 Industries by Funding")
plt.xlabel("Industry")
plt.ylabel("Funding (USD)")

plt.xticks(rotation=60)

plt.tight_layout()

plt.savefig(
    "visuals/top_industries.png"
)

plt.show()

# =====================================================
# 4. Most Active Investors
# =====================================================

query = """
SELECT
    Investors,
    COUNT(*) AS Deals
FROM funding
GROUP BY Investors
ORDER BY Deals DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(12,6))

plt.bar(
    df["Investors"],
    df["Deals"]
)

plt.title("Most Active Investors")
plt.xlabel("Investors")
plt.ylabel("Number of Deals")

plt.xticks(rotation=75)

plt.tight_layout()

plt.savefig(
    "visuals/top_investors.png"
)

plt.show()

# =====================================================
# 5. Investment Type Distribution
# =====================================================

query = """
SELECT
    InvestmentType,
    SUM(InvestmentAmount_USD) AS Funding
FROM funding
GROUP BY InvestmentType
ORDER BY Funding DESC
"""

df = pd.read_sql(query, conn)

plt.figure(figsize=(8,8))

plt.pie(
    df["Funding"],
    labels=df["InvestmentType"],
    autopct="%1.1f%%"
)

plt.title("Investment Type Distribution")

plt.tight_layout()

plt.savefig(
    "visuals/investment_type_distribution.png"
)

plt.show()

# =====================================================
# Close Database
# =====================================================

conn.close()

print("All Visualizations Created Successfully")