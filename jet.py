import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="💰 Personal Finance Assistant", layout="wide")

# ---------- STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "categories" not in st.session_state:
    st.session_state.categories = []
if "income" not in st.session_state:
    st.session_state.income = 0

# ---------- FUNCTIONS ----------
def format_money(n):
    return f"${n:,.2f}"

def get_response(user_input, user_type):
    base_response = "Here's some financial advice: "
    if user_type == "Student":
        tone = "I'll keep it simple."
    else:
        tone = "I'll give you a detailed explanation."

    q = user_input.lower()
    if "tax" in q:
        return f"{base_response} Set aside around 20% of your income for taxes. {tone}"
    elif "save" in q:
        return f"{base_response} Save at least 15-20% of monthly income. {tone}"
    elif "invest" in q:
        return f"{base_response} Diversify between mutual funds, stocks, and bonds. {tone}"
    elif "budget" in q:
        income = st.session_state.income
        expenses = sum(c['amount'] for c in st.session_state.categories)
        savings = income - expenses
        return f"Budget Summary:\nIncome: {format_money(income)}\nExpenses: {format_money(expenses)}\nSavings: {format_money(savings)}"
    else:
        return f"{base_response} Track your expenses and review monthly. {tone}"

def simple_tax_calc(annual):
    """ Simple progressive tax calculator (demo) """
    tax = 0
    if annual > 250000:
        tax += min(annual-250000,250000)*0.05
    if annual > 500000:
        tax += min(annual-500000,500000)*0.1
    if annual > 1000000:
        tax += (annual-1000000)*0.15
    return round(tax,2)

def debt_payoff_months(principal, rate, payment):
    """ Return months to pay off debt """
    monthly_rate = rate/12/100
    months = 0
    balance = principal
    while balance > 0 and months < 1000:
        balance = balance*(1+monthly_rate) - payment
        months += 1
        if payment <= balance*monthly_rate:  # payment too small
            return None
    return months

def future_value(monthly_invest, years, rate):
    """ FV of monthly investment with compounding """
    r = rate/12/100
    n = years*12
    fv = monthly_invest * (((1+r)**n - 1)/r)
    return round(fv,2)

# ---------- SIDEBAR ----------
st.sidebar.header("👤 Profile")
name = st.sidebar.text_input("Name", "Guest User")
user_type = st.sidebar.selectbox("User Type", ["Professional", "Student"])
income = st.sidebar.number_input("Monthly Income", min_value=0, step=100)
st.session_state.income = income

st.sidebar.subheader("💸 Add Expenses")
cat_name = st.sidebar.text_input("Category")
cat_amt = st.sidebar.number_input("Amount", min_value=0, step=10)
if st.sidebar.button("Add Expense"):
    if cat_name and cat_amt > 0:
        st.session_state.categories.append({"name": cat_name, "amount": cat_amt})
        st.sidebar.success("Added!")
    else:
        st.sidebar.error("Enter category and amount")

if st.sidebar.button("Clear Expenses"):
    st.session_state.categories = []

if st.session_state.categories:
    df = pd.DataFrame(st.session_state.categories)
    st.sidebar.table(df)

# ---------- MAIN ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["💬 Chatbot", "📊 Budget & Insights", "🧾 Tax Estimator", "📉 Debt Payoff", "📅 Future Value"]
)

# ---- Chatbot ----
with tab1:
    st.title("💬 Personal Finance Chatbot")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about savings, tax, investments, or budgeting..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_response(prompt, user_type)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# ---- Budget & Insights ----
with tab2:
    st.header("📊 Budget Summary")
    income = st.session_state.income
    expenses = sum(c['amount'] for c in st.session_state.categories)
    savings = income - expenses
    st.write(f"**Income:** {format_money(income)}")
    st.write(f"**Expenses:** {format_money(expenses)}")
    st.write(f"**Savings:** {format_money(savings)}")

    if st.session_state.categories:
        df = pd.DataFrame(st.session_state.categories)
        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(df["amount"], labels=df["name"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        # Bar chart
        st.bar_chart(df.set_index("name"))

# ---- Tax Estimator ----
with tab3:
    st.header("🧾 Tax Estimator")
    annual_income = st.number_input("Enter Annual Income", min_value=0, step=1000)
    if annual_income:
        tax = simple_tax_calc(annual_income)
        st.write(f"Estimated Tax: {format_money(tax)}")
        st.write(f"Net Income after Tax: {format_money(annual_income-tax)}")

# ---- Debt Payoff ----
with tab4:
    st.header("📉 Debt Payoff Helper")
    principal = st.number_input("Debt Amount", min_value=0, step=1000)
    rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.1)
    payment = st.number_input("Monthly Payment", min_value=0, step=100)
    if st.button("Calculate Payoff Time"):
        months = debt_payoff_months(principal, rate, payment)
        if months:
            st.success(f"🎉 You can pay off your debt in {months} months (~{months//12} years).")
        else:
            st.error("Monthly payment too low to cover interest!")

# ---- Future Value ----
with tab5:
    st.header("📅 Future Value of Investments")
    monthly_invest = st.number_input("Monthly Investment", min_value=0, step=100)
    years = st.number_input("Number of Years", min_value=1, step=1)
    rate = st.number_input("Annual Return Rate (%)", min_value=0.0, step=0.5)
    if st.button("Calculate Future Value"):
        fv = future_value(monthly_invest, years, rate)
        st.success(f"📈 Future Value after {years} years: {format_money(fv)}")
