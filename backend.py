
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "Data"
    / "cleaned_startup_funding.csv"
)

MODEL_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"

MODEL_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


# ==========================================
# LOAD DATA
# ==========================================

def load_data():
    """Load and validate the cleaned funding dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "Startup",
        "Industry",
        "Investors",
        "InvestmentAmount_USD",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Dataset is missing columns: {missing}"
        )

    for column in [
        "City",
        "InvestmentType",
        "Date",
    ]:
        if column not in df.columns:
            df[column] = "Unknown"

    if "Year" not in df.columns:
        date_column = (
            "Date_Parsed"
            if "Date_Parsed" in df.columns
            else "Date"
        )

        if date_column in df.columns:
            df["Year"] = pd.to_datetime(
                df[date_column],
                errors="coerce",
            ).dt.year
        else:
            df["Year"] = np.nan

    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce",
    )

    df["InvestmentAmount_USD"] = pd.to_numeric(
        df["InvestmentAmount_USD"],
        errors="coerce",
    )

    for column in [
        "Startup",
        "Industry",
        "Investors",
        "City",
        "InvestmentType",
    ]:
        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    return df


# ==========================================
# BACKEND HEALTH CHECK
# ==========================================

def get_project_status():
    """Return basic dataset and backend information."""

    df = load_data()

    return {
        "status": "Backend ready",
        "records": len(df),
        "startups": df["Startup"].nunique(),
        "industries": df["Industry"].nunique(),
        "valid_funding_amounts": int(
            df["InvestmentAmount_USD"].notna().sum()
        ),
    }


# ==========================================
# FUNDING PREDICTION
# ==========================================

def predict_next_year_funding():
    """Forecast the next year's total recorded funding."""

    df = load_data()

    yearly = (
        df.dropna(
            subset=[
                "Year",
                "InvestmentAmount_USD",
            ]
        )
        .groupby(
            "Year",
            as_index=False,
        )["InvestmentAmount_USD"]
        .sum()
        .sort_values("Year")
    )

    yearly = yearly[
        np.isfinite(yearly["Year"])
        & np.isfinite(
            yearly["InvestmentAmount_USD"]
        )
    ]

    if yearly["Year"].nunique() < 4:
        raise ValueError(
            "At least four distinct years with funding data "
            "are required."
        )

    X = yearly[["Year"]]
    y = yearly["InvestmentAmount_USD"]

    # Reserve the latest observations for testing.
    test_size = max(
        1,
        int(np.ceil(len(yearly) * 0.2)),
    )

    split = len(yearly) - test_size

    if split < 2:
        raise ValueError(
            "Not enough observations to evaluate the model."
        )

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]

    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    evaluation_model = LinearRegression()

    evaluation_model.fit(
        X_train,
        y_train,
    )

    test_predictions = evaluation_model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        test_predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            test_predictions,
        )
    )

    # Refit using all available historical years.
    final_model = LinearRegression()

    final_model.fit(
        X,
        y,
    )

    next_year = int(X["Year"].max()) + 1

    prediction = float(
        final_model.predict(
            pd.DataFrame({
                "Year": [next_year]
            })
        )[0]
    )

    return {
        "next_year": next_year,
        "predicted_funding": prediction,
        "mae": float(mae),
        "rmse": float(rmse),
        "historical_data": yearly,
        "actual_test": y_test.tolist(),
        "predicted_test": test_predictions.tolist(),
    }


# ==========================================
# VALUATION CALCULATOR
# ==========================================

def calculate_valuation(
    revenue,
    low_multiple,
    base_multiple,
    high_multiple,
):
    """Calculate illustrative revenue-multiple scenarios."""

    if revenue < 0:
        raise ValueError(
            "Revenue cannot be negative."
        )

    if not (
        0 < low_multiple
        <= base_multiple
        <= high_multiple
    ):
        raise ValueError(
            "Multiples must satisfy "
            "0 < low <= base <= high."
        )

    return pd.DataFrame({
        "Scenario": [
            "Low",
            "Base",
            "High",
        ],
        "Revenue_Multiple": [
            low_multiple,
            base_multiple,
            high_multiple,
        ],
        "Estimated_Valuation_USD": [
            revenue * low_multiple,
            revenue * base_multiple,
            revenue * high_multiple,
        ],
    })


# ==========================================
# INVESTOR RECOMMENDATION
# ==========================================

def recommend_investors(
    industry,
    city=None,
    top_n=10,
):
    """Rank investors from historical funding records."""

    df = load_data()

    if not industry.strip():
        raise ValueError(
            "Please provide a startup industry."
        )

    matches = df[
        df["Industry"].str.casefold()
        == industry.strip().casefold()
    ].copy()

    matches = matches[
        matches["Investors"].str.casefold()
        != "unknown"
    ]

    if matches.empty:
        return pd.DataFrame()

    # Each comma-separated investor is treated as a separate name.
    matches["Investor"] = matches["Investors"].str.split(",")

    matches = matches.explode("Investor")

    matches["Investor"] = (
        matches["Investor"].fillna("").str.strip()
    )

    matches = matches[
        (matches["Investor"] != "")
        & (
            matches["Investor"].str.casefold()
            != "unknown"
        )
    ]

    matches["Investor_Key"] = (
        matches["Investor"].str.casefold()
    )

    recommendations = (
        matches.groupby("Investor_Key")
        .agg(
            Investor=("Investor", "first"),
            Industry_Matches=("Startup", "size"),
            Example_Startups=(
                "Startup",
                lambda values: ", ".join(
                    values.dropna().astype(str).unique()[:3]
                ),
            ),
        )
        .reset_index()
    )

    recommendations["City_Matches"] = 0

    if city and city.strip():
        city_matches = matches[
            matches["City"].str.casefold()
            == city.strip().casefold()
        ]

        city_counts = (
            city_matches.groupby("Investor_Key").size()
        )

        recommendations["City_Matches"] = (
            recommendations["Investor_Key"]
            .map(city_counts)
            .fillna(0)
            .astype(int)
        )

    recommendations["Score"] = (
        recommendations["Industry_Matches"]
        + 2 * recommendations["City_Matches"]
    )

    return (
        recommendations.sort_values(
            ["Score", "Industry_Matches"],
            ascending=False,
        )
        .head(max(1, int(top_n)))
        [[
            "Investor",
            "Industry_Matches",
            "City_Matches",
            "Score",
            "Example_Startups",
        ]]
        .reset_index(drop=True)
    )


# ==========================================
# RUN BACKEND HEALTH CHECK
# ==========================================

if __name__ == "__main__":

    print("\n===== BACKEND HEALTH CHECK =====")

    try:
        status = get_project_status()

        for key, value in status.items():
            print(f"{key}: {value}")

    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Backend error: {error}")
