import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# 🔹 Set Page Config at the Top
st.set_page_config(layout="wide", page_title="🚀 AI-Powered Cold Email Generator", page_icon="📧")

# 🔹 Custom Background & Styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #141e30, #243b55);
            color: white;
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #1E90FF;
            padding: 10px;
        }
        .stButton > button {
            border-radius: 10px;
            background-color: #1E90FF;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #0073e6;
        }
    </style>
""", unsafe_allow_html=True)


def create_streamlit_app(llm, portfolio, clean_text):
    # 🔹 Stylish Title
    st.markdown(
        "<h1 style='text-align: center; font-size: 36px; color: #1E90FF;'>🚀 AI-Powered Cold Email Generator</h1>",
        unsafe_allow_html=True
    )

    st.write("👋 Enter a job URL below to generate an AI-powered cold email.")

    # 🔹 Styled Input Box
    url_input = st.text_input("🔗 Enter a Job URL:", value="https://www.naukri.com/jobs-by-location")

    submit_button = st.button("🚀 Generate Email")

    if submit_button:
        with st.spinner("🔄 Processing your request... Please wait!"):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("⚠️ No jobs found. Try another URL!", icon="⚠️")
                    return

                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)

                    # 🔹 Show Email in a Nice Box
                    st.success("✅ Cold Email Generated Successfully!")
                    st.markdown(f"📧 **Generated Email:**")
                    st.code(email, language='markdown')

            except Exception as e:
                st.error(f"❌ An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
