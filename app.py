import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SaaS Metrics Dashboard", layout="wide")

st.title("SaaS Metrics Dashboard")
st.markdown("Upload your customer data to analyse key SaaS metrics.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Metrics
    total_mrr = df[df["status"] == "Active"]["mrr"].sum()
    total_customers = len(df)
    active_customers = len(df[df["status"] == "Active"])
    churned_customers = len(df[df["status"] == "Churned"])
    churn_rate = round((churned_customers / total_customers) * 100, 1)

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total MRR", f"${total_mrr:,}")
    col2.metric("Total Customers", total_customers)
    col3.metric("Active Customers", active_customers)
    col4.metric("Churn Rate", f"{churn_rate}%")

    st.divider()

    # Charts
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Revenue by Plan")
        plan_revenue = df[df["status"] == "Active"].groupby("plan")["mrr"].sum().reset_index()
        fig1 = px.bar(plan_revenue, x="plan", y="mrr", color="plan")
        st.plotly_chart(fig1, use_container_width=True)

    with col6:
        st.subheader("Customer Growth by Month")
        growth = df.groupby("signup_month")["customer_id"].count().reset_index()
        fig2 = px.line(growth, x="signup_month", y="customer_id", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Raw Data")
    st.dataframe(df)