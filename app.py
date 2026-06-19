import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq

client = Groq(api_key="your_api_key_here")

st.set_page_config(page_title="AI Expense Analyzer", layout="wide")
st.title("AI Expense Analyzer")
st.markdown("Track your expenses, view insights, and get AI-powered recommendations!")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

with st.form("expense_form"):
    date = st.date_input("Date")
    amount = st.number_input("Amount (Rs.)", min_value=0.0, step=0.01)
    description = st.text_input("Description (e.g., Bought pizza, paid rent)")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    if amount > 0 and description.strip():
        st.session_state.expenses.append({
            "Date": date,
            "Amount": amount,
            "Description": description
        })
        st.success("Expense added successfully!")
    else:
        st.error("Please enter valid details.")

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)

    st.subheader("Expense Summary")
    st.dataframe(df)

    trend = df.groupby("Date")["Amount"].sum().reset_index()
    st.subheader("Expense Trend")
    fig, ax = plt.subplots()
    ax.plot(trend["Date"], trend["Amount"], marker="o", linestyle="-")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount Spent (Rs.)")
    ax.set_title("Spending Over Time")
    st.pyplot(fig)

    st.subheader("Expense Distribution")
    desc_summary = df.groupby("Description")["Amount"].sum()
    fig2, ax2 = plt.subplots()
    ax2.pie(desc_summary, labels=desc_summary.index, autopct="%1.1f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)

    st.subheader("AI Expense Insights")
    analyze_btn = st.button("Generate AI Recommendations")
    if analyze_btn:
        text_prompt = (
            "Analyze the following expenses and give insights on spending habits, "
            "patterns, and practical strategies to save money:\n\n"
            + df.to_string(index=False)
        )
        with st.spinner("Analyzing your expenses..."):
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": text_prompt}],
                model="llama-3.3-70b-versatile",
            )
            st.markdown("### Recommendations:")
            st.write(response.choices[0].message.content)
else:
    st.info("Add some expenses to start tracking!")

st.markdown("---")
st.caption("Built with Streamlit + Groq AI")
