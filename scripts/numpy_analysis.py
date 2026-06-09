import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("Data/cleaned_startup_funding.csv")

print("=" * 60)
print("STARTUP FUNDING - NUMPY STATISTICAL ANALYSIS")
print("=" * 60)

# Total Funding
print("\n1. TOTAL FUNDING RAISED")

total_funding = np.sum(
    df["InvestmentAmount_USD"]
)

print(total_funding)

# Average Funding
print("\n2. AVERAGE FUNDING")

average_funding = np.mean(
    df["InvestmentAmount_USD"]
)

print(average_funding)

# Median Funding
print("\n3. MEDIAN FUNDING")

median_funding = np.median(
    df["InvestmentAmount_USD"]
)

print(median_funding)

# Maximum Funding
print("\n4. MAXIMUM FUNDING")

max_funding = np.max(
    df["InvestmentAmount_USD"]
)

print(max_funding)

# Minimum Funding
print("\n5. MINIMUM FUNDING")

min_funding = np.min(
    df["InvestmentAmount_USD"]
)

print(min_funding)

# Funding Range
print("\n6. FUNDING RANGE")

funding_range = (
    max_funding - min_funding
)

print(funding_range)

# Standard Deviation
print("\n7. STANDARD DEVIATION")

std_funding = np.std(
    df["InvestmentAmount_USD"]
)

print(std_funding)

# Variance
print("\n8. VARIANCE")

variance_funding = np.var(
    df["InvestmentAmount_USD"]
)

print(variance_funding)

# Percentiles
print("\n9. PERCENTILES")

print(
    "25th Percentile:",
    np.percentile(
        df["InvestmentAmount_USD"],
        25
    )
)

print(
    "50th Percentile:",
    np.percentile(
        df["InvestmentAmount_USD"],
        50
    )
)

print(
    "75th Percentile:",
    np.percentile(
        df["InvestmentAmount_USD"],
        75
    )
)

# Total Records
print("\n10. TOTAL FUNDING RECORDS")

print(
    np.size(
        df["InvestmentAmount_USD"]
    )
)

# Unique Funding Amounts
print("\n11. UNIQUE FUNDING AMOUNTS")

print(
    len(
        np.unique(
            df["InvestmentAmount_USD"]
        )
    )
)

# Mean vs Median
print("\n12. MEAN VS MEDIAN")

print("Mean :", average_funding)
print("Median :", median_funding)

# Top 10 Funding Average
print("\n13. AVERAGE OF TOP 10 FUNDING ROUNDS")

top10_avg = np.mean(
    np.sort(
        df["InvestmentAmount_USD"]
    )[-10:]
)

print(top10_avg)

print("\n" + "=" * 60)
print("NUMPY ANALYSIS COMPLETED")
print("=" * 60)  