import base64
import streamlit as st
from pathlib import Path


ASSETS_PATH = Path(__file__).parent.parent / "assets"


def load_css():
    """
    Load and inject the main CSS stylesheet into the Streamlit app.

    The CSS file is read from the assets directory and applied globally
    using Streamlit's markdown HTML rendering.

    Returns
    -------
    None
    """
    css_path = ASSETS_PATH / "styles" / "styles.css"

    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def load_image(path: Path):
    """
    Encode an image file as base64.

    Parameters
    ----------
    path : Path
        Path to the image file.

    Returns
    -------
    str
        Base64-encoded string representation of the image.
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def load_icons():
    """
    Load all UI icons from the assets directory.

    Returns
    -------
    dict
        Dictionary mapping icon names to base64-encoded images.
    """
    icons_path = ASSETS_PATH / "images"

    return {
        "github": load_image(icons_path / "github.png"),
        "linkedin": load_image(icons_path / "LK.png"),
        "x": load_image(icons_path / "X.png"),
        "email": load_image(icons_path / "correo.png"),
        "telefono": load_image(icons_path / "Tel.png"),
        "portfolio": load_image(icons_path / "portfolio.png"),
        "chat": load_image(icons_path / "chatbot.png"),
    }