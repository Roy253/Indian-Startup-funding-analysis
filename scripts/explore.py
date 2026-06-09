import pandas as pd

df = pd.read_csv("data/startup_funding.csv")
print(df.head())
print(df.info())
print(df.describe())
print(df.shape)

# Missing values
print(df.isnull().sum())

#remove duplicates
df.drop_duplicates(inplace=True)
print(df.shape)

#statistical summary
print ("\nStatistical Summary:")
print(df.describe())

#total Record

print("\nTotal Records:", len(df))

#top10 cities with most startups
print("\nTop 10 Cities with Most Startups:")
print(df['City'].value_counts().head(10))

#top 10 industries with most startups
print("\nTop 10 Industries with Most Startups:")
print(df['Industry'].value_counts().head(10))

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

print(df["Date"].head())

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Quarter"] = df["Date"].dt.quarter
df["Day"] = df["Date"].dt.day

print(df.head())

#clean city names
df["City"] = (
    df["City"]
      .astype(str)
      .str.strip()
)

df["City"] = df["City"].replace({
    "Bangalore":"Bengaluru",
    "New Delhi":"Delhi"
})


#TOTAL FUNDING BY CITY
city_funding = (
    df.groupby("City")
      ["InvestmentAmount_USD"]
      .sum()
      .sort_values(ascending=False)
)

print(city_funding.head(10))

#Total Funding by Industry
industry_funding = (
    df.groupby("Industry")
      ["InvestmentAmount_USD"]
      .sum()
      .sort_values(ascending=False)
)

print(industry_funding.head(10))

#yearly funding trends
yearly_funding = (
    df.groupby("Year")
      ["InvestmentAmount_USD"]
      .sum()
)
print(yearly_funding)

#funding round count by year
funding_rounds = (
    df.groupby("Year")
      ["InvestmentAmount_USD"]
      .count()
)
print(funding_rounds)

#top investors
top_investors = (
    df.groupby("Investors")
      ["InvestmentAmount_USD"]
      .sum()
      .sort_values(ascending=False)
)
print(top_investors.head(10))

#investment type analysis
investment_type_funding = (
    df.groupby("InvestmentType")
      ["InvestmentAmount_USD"]
      .sum()
      .sort_values(ascending=False)
)
print(investment_type_funding.head(10))

#INVESTMENT TYPE ANALYSIS
investment_type_count = (
    df.groupby("InvestmentType")
      ["InvestmentAmount_USD"]
      .count()
      .sort_values(ascending=False)
)
print(investment_type_count.head(10))

#SAVE CLEANED DATASET
df.to_csv("data/cleaned_startup_funding.csv", index=False)

print("\nData exploration completed. Cleaned dataset saved as 'cleaned_startup_funding.csv'.")