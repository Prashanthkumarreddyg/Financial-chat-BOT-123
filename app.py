import streamlit as st
from flask import Flask, request, jsonify
from streamlit.components.v1 import html as st_html

# --- Mock IBM Watson Assistant response function ---
def get_chatbot_response(user_input, user_type):
    """
    Simulate chatbot response with demographic-aware communication.
    """
    base_response = "Here's some financial advice regarding your query: "
    if user_type == "student":
        tone = "I'll keep it simple and easy to understand."
    else:
        tone = "I'll provide a detailed and professional explanation."

    # Simple keyword-based responses
    if "tax" in user_input.lower():
        advice = "You should plan for taxes by setting aside ~20% of your income."
    elif "save" in user_input.lower():
        advice = "Aim to save at least 15-20% of your monthly income."
    elif "invest" in user_input.lower():
        advice = "Consider diversifying investments across mutual funds, stocks, and bonds."
    else:
        advice = "Track expenses carefully and adjust your budget every month."

    return f"{base_response}{advice} {tone}"

# Flask app inside Streamlit
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    user_type = data.get("userType", "professional")
    reply = get_chatbot_response(user_input, user_type)
    return jsonify({"reply": reply})


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Personal Finance Chatbot", layout="wide")

st.title("💰 Personal Finance Chatbot (All-in-One)")
st.write("This app merges the chatbot UI and Python backend. Ask about **savings, taxes, or investments**!")

# --- Full HTML UI with backend integration ---
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Personal Finance Chatbot — All-in-One</title>
  <style>
    :root{ --bg:#0f1724; --card:#0b1220; --muted:#99a7c7; --text:#e6eef9; --accent:#06b6d4; --glass: rgba(255,255,255,0.03); --radius:12px; }
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter,system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:linear-gradient(180deg,#071124 0%, #0b1220 100%);color:var(--text);min-height:100vh;}
    .app{max-width:1000px;margin:28px auto;padding:20px;display:grid;grid-template-columns:380px 1fr;gap:18px}
    header{grid-column:1/3;display:flex;align-items:center;justify-content:space-between}
    header h1{margin:0;font-size:20px}
    .card{background:var(--card);padding:14px;border-radius:var(--radius);box-shadow:0 8px 30px rgba(2,6,23,.6)}
    .left{display:flex;flex-direction:column;gap:12px}
    .profile{display:flex;gap:12px;align-items:center}
    .avatar{width:58px;height:58px;border-radius:12px;background:linear-gradient(135deg,var(--accent),#8b5cf6);display:flex;align-items:center;justify-content:center;font-weight:700}
    label.select{display:flex;gap:8px;align-items:center}
    .btn{background:linear-gradient(90deg,var(--accent),#8b5cf6);border:none;color:white;padding:8px 12px;border-radius:10px;cursor:pointer}
    .btn.secondary{background:transparent;border:1px solid rgba(255,255,255,0.06)}
    .chat{display:flex;flex-direction:column;height:60vh}
    .messages{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:10px}
    .msg{max-width:78%;padding:10px;border-radius:10px}
    .msg.user{align-self:flex-end;background:linear-gradient(180deg,#122436,#0e2540)}
    .msg.bot{align-self:flex-start;background:rgba(255,255,255,0.03)}
    .composer{display:flex;gap:8px;padding:10px}
    input[type=text]{width:100%;padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.04);background:transparent;color:var(--text)}
  </style>
</head>
<body>
  <div class="app">
    <header>
      <h1>Personal Finance Chatbot</h1>
      <div class="small">Status: <strong>Connected</strong></div>
    </header>

    <div class="left">
      <div class="card profile">
        <div class="avatar" id="avatar">PF</div>
        <div style="flex:1">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
              <div id="username" style="font-weight:700">Guest User</div>
              <div class="small" id="useremail">No profile loaded</div>
            </div>
            <div style="text-align:right">
              <div class="small">User type</div>
              <select id="userType">
                <option value="student">Student</option>
                <option value="professional" selected>Professional</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2 style="margin:0">Chat</h2>
      <div class="chat">
        <div class="messages" id="messages"></div>
        <div class="composer">
          <input id="userInput" type="text" placeholder="Ask me about savings, tax, or investments..." />
          <button class="btn" id="send">Send</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    const state = { messages: [] }
    const $ = id => document.getElementById(id)

    function appendMessage(text, who='bot'){
      state.messages.push({who,text})
      renderMessages()
    }
    function renderMessages(){
      const box = $('messages'); box.innerHTML=''
      state.messages.forEach(m=>{
        const d=document.createElement('div')
        d.className='msg '+(m.who==='user'?'user':'bot')
        d.innerHTML='<div>'+m.text+'</div>'
        box.appendChild(d)
      })
      box.scrollTop=box.scrollHeight
    }

    $('send').onclick=()=>{
      const t=$('userInput').value.trim()
      if(!t)return
      appendMessage(t,'user')
      $('userInput').value=''
      processUserQuery(t)
    }
    $('userInput').addEventListener('keydown',e=>{
      if(e.key==='Enter'){e.preventDefault();$('send').click()}
    })

    function processUserQuery(text){
      const type = $('userType').value
      fetch("/chat", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:text,userType:type})
      })
      .then(r=>r.json())
      .then(res=>appendMessage(res.reply,'bot'))
      .catch(()=>appendMessage("⚠️ Error connecting to backend.","bot"))
    }
  </script>
</body>
</html>
"""

# Render HTML inside Streamlit
st_html(html_code, height=800, scrolling=True)
