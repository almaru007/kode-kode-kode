import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Marketing Attribution & Cohort Engine", layout="wide")

# Directory helper for Data folder
DATA_DIR = "Data" if os.path.exists("Data") else "data"
if not os.path.exists(DATA_DIR):
    DATA_DIR = "."

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "Data" / "Data synthesis"

@st.cache_data
def load_data():
    df_roas = pd.read_csv(DATA_DIR / "attribution_roas_comparison.csv")
    df_touches = pd.read_csv(DATA_DIR / "attributed_touchpoints.csv")
    df_cohort = pd.read_csv(DATA_DIR / "cohort_ltv_analysis.csv")
    return df_roas, df_touches, df_cohort

df_roas, df_touches, df_cohort = load_data()

st.title("🎯 Paid Media Multi-Touch Attribution & LTV Engine")
st.markdown(
    "First-party modeled cross-channel attribution engine comparing First-Touch, "
    "Last-Touch, and U-Shaped (40/20/40) credit."
)

tab1, tab2, tab3 = st.tabs(
    ["1. Executive Media Performance", "2. Touchpoint Drill-Down", "3. Cohort LTV"]
)

# --- TAB 1: EXECUTIVE OVERVIEW ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    total_spend = df_roas["spend_nok"].sum()
    total_rev = df_roas["ushaped_revenue"].sum()
    blended_roas = total_rev / total_spend if total_spend > 0 else 0

    col1.metric("Total Paid Media Spend", f"{total_spend:,.0f} NOK")
    col2.metric("Attributed Net Revenue", f"{total_rev:,.0f} NOK")
    col3.metric("Blended ROAS (U-Shaped)", f"{blended_roas:.2f}x")
    col4.metric("Monitored Channels", len(df_roas))

    st.subheader("Model Comparison: Attributed ROAS by Strategy")

    fig_roas = go.Figure(
        data=[
            go.Bar(
                name="First-Touch ROAS (Discovery)",
                x=df_roas["channel"],
                y=df_roas["roas_fta"],
            ),
            go.Bar(
                name="Last-Touch ROAS (Closer)",
                x=df_roas["channel"],
                y=df_roas["roas_lta"],
            ),
            go.Bar(
                name="U-Shaped ROAS (Balanced)",
                x=df_roas["channel"],
                y=df_roas["roas_ushaped"],
            ),
        ]
    )
    fig_roas.update_layout(
        barmode="group", yaxis_title="Attributed ROAS (x)", template="plotly_white"
    )
    st.plotly_chart(fig_roas, use_container_width=True)

    st.subheader("Performance Summary")
    st.dataframe(df_roas, use_container_width=True)

# --- TAB 2: TOUCHPOINT DRILL-DOWN ---
with tab2:
    st.subheader("Channel & Campaign Contribution")
    selected_channel = st.multiselect(
        "Filter by Channel",
        options=df_touches["channel"].unique(),
        default=df_touches["channel"].unique(),
    )
    filtered_touches = df_touches[df_touches["channel"].isin(selected_channel)]

    fig_pie = px.pie(
        filtered_touches,
        values="ushaped_revenue",
        names="channel",
        title="Attributed Revenue Share (U-Shaped)",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Sample Attributed Touchpoints")
    st.dataframe(filtered_touches.head(100), use_container_width=True)

# --- TAB 3: COHORT LTV ---
with tab3:
    st.subheader("Customer Maturation & Net LTV")
    fig_cohort = px.bar(
        df_cohort,
        x="maturation_window",
        y="revenue_nok",
        color="acquisition_channel",
        barmode="group",
        title="Revenue Realization by Maturation Window and First-Touch Source",
    )
    fig_cohort.update_layout(template="plotly_white", yaxis_title="Revenue (NOK)")
    st.plotly_chart(fig_cohort, use_container_width=True)

    st.subheader("Cohort Detail Data")
    st.dataframe(df_cohort, use_container_width=True)
