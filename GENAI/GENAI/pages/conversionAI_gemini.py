import streamlit as st
import google.generativeai as genai

# Title styling
st.markdown(
    """
    <style>
        .title-text {
            color: darkgreen;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
        }
        .subtitle-text {
            color: skyblue;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
        }
    </style>
    """
    , unsafe_allow_html=True
)

# Title and subtitle
st.markdown('<p class="title-text">🌟Welcome to Chitti Robot - Your Data Science Assistant🌟</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">🤖Chitti Robot is Ready to Assist You!🤖</p>', unsafe_allow_html=True)

# Load API key from file
with open(r"C:\Users\pamar\Desktop\Ds internship\backend\GENAI\keys\geminiapikey.txt") as f:
    api_key = f.read()

# Configure GenerativeAI
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="""Hi! I'm ChittiRobot, your AI assistant for Data Science. I'm here to help you. Feel free to ask me anything related to Data Science or for assistance with any coding challenges you're facing. If the question is not related to data science, please note that I may not be able to provide the assistance you need."""
)

# Initialize chat history if not already present
if "memory" not in st.session_state:
    st.session_state["memory"] = []

# Start chat with the AI model
chat = model.start_chat(history=st.session_state["memory"])

for msg in chat.history:
    name=msg.role
    if name=="model":
        name="AI-chittirobot"
        st.chat_message(name).write(msg.parts[0].text)
    else:
        st.chat_message(msg.role).write(msg.parts[0].text)

user_input = st.chat_input()

if user_input:
    st.chat_message("user👤").write(user_input)
    response = chat.send_message(user_input)
    AC=st.chat_message("AI-chittirobot🤖").write(bot.text for bot in response)
    st.session_state["memory"] = chat.history


