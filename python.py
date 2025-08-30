import streamlit as st
from typing import List, Dict
import random

# Simulated IBM Watson / HuggingFace AI response functions
def generate_financial_guidance(user_type: str, user_message: str) -> str:
    # Placeholder: Replace with IBM Watson or HuggingFace API call
    student_responses = [
        "As a student, consider starting with a high-yield savings account for your emergency fund.",
        "Many students qualify for education tax credits. Let me help you explore options.",
        "Starting investments early gives you the power of compound interest. Even small amounts matter!",
        "Budgeting apps can help track your spending between classes and social activities."
    ]
    professional_responses = [
        "For professionals, maximizing 401(k) contributions should be a priority for retirement planning.",
        "Consider tax-loss harvesting strategies to optimize your investment portfolio this year.",
        "Real estate investments can provide both rental income and long-term appreciation benefits.",
        "Diversifying your investment portfolio across different asset classes reduces overall risk."
    ]
    if user_type == "Student":
        return random.choice(student_responses)
    else:
        return random.choice(professional_responses)

def generate_budget_summary(user_type: str) -> List[Dict]:
    # Placeholder budget summary data
    return [
        {"category": "Housing", "spent": 1200, "budget": 1500},
        {"category": "Food & Dining", "spent": 600, "budget": 800},
        {"category": "Entertainment", "spent": 300, "budget": 400},
    ]

def generate_spending_insights(user_type: str) -> List[Dict]:
    # Placeholder spending insights
    return [
        {"category": "Dining out", "change_percent": 25, "trend": "up"},
        {"category": "Shopping", "change_percent": 15, "trend": "down"},
    ]

def generate_investment_suggestions(user_type: str) -> List[Dict]:
    # Placeholder investment suggestions
    return [
        {"name": "Index Funds", "risk_level": "Low", "description": "Low risk, long-term growth", "expected_return": 8.2},
        {"name": "Tech Stocks", "risk_level": "Medium", "description": "Medium risk, high potential", "expected_return": 12.5},
        {"name": "Real Estate", "risk_level": "Stable", "description": "Stable returns, tax benefits", "expected_return": 6.8},
    ]

# Streamlit app starts here
st.set_page_config(page_title="Personal Finance Chatbot", layout="wide")

st.title("Personal Finance Chatbot: Intelligent Guidance for Savings, Taxes, and Investments")

# Sidebar for user profile selection
user_type = st.sidebar.selectbox("Select your profile type:", ["Student", "Professional"])

st.sidebar.markdown("""
---
**About:**  
This chatbot provides personalized financial guidance, budget summaries, spending insights, and investment suggestions tailored to your profile.
""")

# Chat interface
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_message(role: str, message: str):
    st.session_state.chat_history.append({"role": role, "message": message})

def display_chat():
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"<div style='text-align: right; background-color:#667eea; color:white; padding:8px; border-radius:10px; margin:5px 0;'>{chat['message']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background-color:#f1f5f9; color:#334155; padding:8px; border-radius:10px; margin:5px 0;'>{chat['message']}</div>", unsafe_allow_html=True)

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me about savings, taxes, investments, or your budget:")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    add_message("user", user_input)
    # Generate AI response
    response = generate_financial_guidance(user_type, user_input)
    add_message("bot", response)

# Display chat history
display_chat()

st.markdown("---")

# Budget Summary Section
st.subheader("AI-Generated Budget Summary")
budget_summary = generate_budget_summary(user_type)
for item in budget_summary:
    spent = item["spent"]
    budget = item["budget"]
    percent = int((spent / budget) * 100)
    st.write(f"**{item['category']}**: ${spent} spent of ${budget} budget")
    st.progress(min(percent, 100))

st.markdown("---")

# Spending Insights Section
st.subheader("Spending Insights and Suggestions")
spending_insights = generate_spending_insights(user_type)
for insight in spending_insights:
    trend_arrow = "⬆️" if insight["trend"] == "up" else "⬇️"
    st.write(f"{insight['category']}: {insight['change_percent']}% {trend_arrow}")

st.markdown("---")

# Investment Suggestions Section
st.subheader("Investment Opportunities")
investment_suggestions = generate_investment_suggestions(user_type)
for inv in investment_suggestions:
    st.markdown(f"**{inv['name']}** ({inv['risk_level']} risk): {inv['description']} — Expected Return: {inv['expected_return']}%")

st.markdown("---")

st.caption("Powered by IBM Watson AI • Granite • HuggingFace • Streamlit")
