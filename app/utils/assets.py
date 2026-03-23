import base64
import pathlib
import streamlit as st


def load_css():
    css_path = pathlib.Path("frontend/styles/styles.css")

    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def load_icons():
    return {
        "github": load_image("frontend/images/github.png"),
        "linkedin": load_image("frontend/images/LK.png"),
        "x": load_image("frontend/images/X.png"),
        "email": load_image("frontend/images/correo.png"),
        "telefono": load_image("frontend/images/Tel.png"),
        "portfolio": load_image("frontend/images/portfolio.png"),
        "chat": load_image("frontend/images/chatbot.png"),
    }
    
    
    