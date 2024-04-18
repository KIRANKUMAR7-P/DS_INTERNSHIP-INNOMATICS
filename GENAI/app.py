import streamlit as st
from openai import OpenAI
import requests.exceptions

# Set page title and background color
st.title("Code Quality Enhancement with OpenAI")
bg_color = "#F4F4F4"
title_color = "#FF4505"  # Custom color for the title
st.markdown(f"""
    <style>
        .reportview-container {{
            background-color: {bg_color};
        }}
        .sidebar .sidebar-content {{
            background-color: #FFFFFF;
            box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.1);
        }}
        h1, h2, h3 {{
            color: {title_color};  /* Custom title color */
            font-weight: bold;
        }}
        h2 {{
            color: #FFA500; /* Custom title color */
            border-bottom: 2px solid #FFA500; /* Custom title color border bottom */
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

# Read API key from file
try:
    with open(r"C:\Users\pamar\Desktop\Ds internship\backend\GENAI\keys\apikey.txt", "r") as f:
        OPENAI_API_KEY = f.read().strip()
except FileNotFoundError:
    st.error("OpenAI API key file not found. Please make sure to add your API key in the correct location.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# User input section
st.header("Input Your Code")
prompt = st.text_area("Paste your code here:", height=200,placeholder="Enter the code hear")

# Button to trigger code reviews
if st.button("Enhance Code Quality"):
    st.header("Code Quality Enhancement Result 🚀")

    try:
        # Generate code review using OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "You are a helpful AI assistant that reviews Python code, analyze the submitted code, identify potential bugs, errors, or areas of improvement. After identifying, give the bug report and fixed code snippet in a text box."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=1,
            top_p=1,
            n=1,
            presence_penalty=0,
            frequency_penalty=0,
        )

        # Display the generated review
        generated_text = response.choices[0].message.content
        st.subheader("Corrected Code")
        st.code(generated_text)
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error occurred: {e}")
    except Exception as e:
        st.error(f"An error occurred while processing the request: {e}")
