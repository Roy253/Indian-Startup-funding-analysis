
import streamlit as st
import pandas as pd
import plotly.express as px

from backend import (
    load_data,
    predict_next_year_funding,
    recommend_investors,
    calculate_valuation, 
)

st.set_page_config(
    page_title="Venture AI Lab",
    page_icon="🚀",
    layout="wide",
)

# Load data through the backend.
try:
    df = load_data()
except (FileNotFoundError, ValueError, OSError) as error:
    st.error(f"Backend data error: {error}")
    st.stop()


def format_money(value):
    if pd.isna(value):
        return "Not available"

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"

    return f"${value:,.2f}"


# Sidebar
st.sidebar.title("🚀 Venture AI Lab")
st.sidebar.caption("Startup Funding Analysis")

page = st.sidebar.radio(
    "Select a tool",
    [
        "Overview",
        "Funding Prediction",
        "Investor Finder",
        "Valuation Advisor",
        "Startup Explorer",
    ],
)


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":
    st.title("Venture AI Lab")
    st.write(
        "Run backend-powered funding forecasts, investor discovery "
        "and valuation scenarios."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Funding Records", f"{len(df):,}")
    c2.metric("Startups", f"{df['Startup'].nunique():,}")
    c3.metric("Industries", f"{df['Industry'].nunique():,}")
    c4.metric(
        "Recorded Funding",
        format_money(df["InvestmentAmount_USD"].sum(min_count=1)),
    )

    st.info(
        "Choose a model from the sidebar to run it with interactive inputs."
    )


# --------------------------------------------------
# FUNDING PREDICTION
# --------------------------------------------------

elif page == "Funding Prediction":
    st.title("📈 Funding Prediction")

    st.write(
        "Run the funding forecasting function from backend.py."
    )

    if st.button("Run Funding Prediction", type="primary"):
        try:
            result = predict_next_year_funding()

            c1, c2, c3 = st.columns(3)

            c1.metric(
                f"Forecast for {result['next_year']}",
                format_money(result["predicted_funding"]),
            )
            c2.metric("Test MAE", format_money(result["mae"]))
            c3.metric("Test RMSE", format_money(result["rmse"]))

            historical = result["historical_data"]

            fig = px.line(
                historical,
                x="Year",
                y="InvestmentAmount_USD",
                markers=True,
                title="Historical Annual Funding",
                template="plotly_white",
            )

            st.plotly_chart(fig, use_container_width=True)

            test_results = pd.DataFrame({
                "Year": result["historical_data"]["Year"]
                .tail(len(result["actual_test"]))
                .tolist(),
                "Actual Funding": result["actual_test"],
                "Predicted Funding": result["predicted_test"],
            })

            st.subheader("Test-set predictions")
            st.dataframe(
                test_results,
                use_container_width=True,
                hide_index=True,
            )

        except (ValueError, FileNotFoundError, OSError) as error:
            st.error(f"Prediction failed: {error}")


# --------------------------------------------------
# INVESTOR FINDER
# --------------------------------------------------

elif page == "Investor Finder":
    st.title("🎯 Investor Finder")

    industries = sorted(
        df.loc[df["Industry"] != "Unknown", "Industry"]
        .dropna()
        .unique()
        .tolist()
    )

    cities = sorted(
        df.loc[df["City"] != "Unknown", "City"]
        .dropna()
        .unique()
        .tolist()
    )

    if not industries:
        st.warning("No industries are available in the dataset.")
    else:
        with st.form("investor_search_form"):
            industry = st.selectbox(
                "Startup industry",
                industries,
            )

            city_options = ["Any city"] + cities

            city_choice = st.selectbox(
                "City",
                city_options,
            )

            top_n = st.slider(
                "Number of recommendations",
                min_value=1,
                max_value=25,
                value=10,
            )

            submitted = st.form_submit_button(
                "Find Investors",
                type="primary",
            )

        if submitted:
            try:
                city = (
                    None
                    if city_choice == "Any city"
                    else city_choice
                )

                recommendations = recommend_investors(
                    industry=industry,
                    city=city,
                    top_n=top_n,
                )

                if recommendations.empty:
                    st.warning(
                        "No historical investor matches were found."
                    )
                else:
                    st.subheader("Recommended historical matches")

                    st.dataframe(
                        recommendations,
                        use_container_width=True,
                        hide_index=True,
                    )

                    st.download_button(
                        "Download recommendations",
                        data=recommendations.to_csv(
                            index=False
                        ).encode("utf-8"),
                        file_name="investor_recommendations.csv",
                        mime="text/csv",
                    )

                st.caption(
                    "These recommendations are based on historical "
                    "records, not verified current investor preferences."
                )

            except (ValueError, KeyError, OSError) as error:
                st.error(f"Investor search failed: {error}")


# --------------------------------------------------
# VALUATION ADVISOR
# --------------------------------------------------

elif page == "Valuation Advisor":
    st.title("🧮 Valuation Advisor")

    st.write(
        "Calculate low, base and high valuation scenarios using "
        "your selected revenue multiples."
    )

    with st.form("valuation_form"):
        revenue = st.number_input(
            "Annual revenue (USD)",
            min_value=0.0,
            value=1_000_000.0,
            step=100_000.0,
        )

        low_multiple = st.number_input(
            "Low revenue multiple",
            min_value=0.1,
            value=2.0,
            step=0.5,
        )

        base_multiple = st.number_input(
            "Base revenue multiple",
            min_value=0.1,
            value=5.0,
            step=0.5,
        )

        high_multiple = st.number_input(
            "High revenue multiple",
            min_value=0.1,
            value=8.0,
            step=0.5,
        )

        calculate = st.form_submit_button(
            "Calculate Valuation",
            type="primary",
        )

    if calculate:
        try:
            results = calculate_valuation(
                revenue,
                low_multiple,
                base_multiple,
                high_multiple,
            )

            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True,
            )

            fig = px.bar(
                results,
                x="Scenario",
                y="Estimated_Valuation_USD",
                title="Valuation Scenarios",
                template="plotly_white",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            st.download_button(
                "Download valuation results",
                data=results.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="valuation_scenarios.csv",
                mime="text/csv",
            )

        except ValueError as error:
            st.error(f"Valuation failed: {error}")


# --------------------------------------------------
# STARTUP EXPLORER
# --------------------------------------------------

elif page == "Startup Explorer":
    st.title("🔎 Startup Explorer")

    startup_query = st.text_input(
        "Enter startup name",
        placeholder="Search for a startup",
    )

    if startup_query.strip():
        mask = df["Startup"].str.contains(
            startup_query.strip(),
            case=False,
            regex=False,
            na=False,
        )

        matches = df[mask]

        if matches.empty:
            st.warning("No startup found.")
        else:
            startup_names = sorted(
                matches["Startup"].unique().tolist()
            )

            selected_startup = st.selectbox(
                "Select startup",
                startup_names,
            )

            profile = df[
                df["Startup"] == selected_startup
            ]

            st.subheader(selected_startup)

            c1, c2 = st.columns(2)

            c1.metric(
                "Funding Records",
                f"{len(profile):,}",
            )

            c2.metric(
                "Recorded Funding",
                format_money(
                    profile["InvestmentAmount_USD"].sum(
                        min_count=1
                    )
                ),
            )

            st.dataframe(
                profile,
                use_container_width=True,
                hide_index=True,
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Venture AI Lab | Historical data and decision support"
)

