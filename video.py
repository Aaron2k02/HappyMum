# from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="happymom.ai", page_icon=":baby:", layout="wide")


# LOGIN #

def login():
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.checkbox("Login"):
        if username == "mummyamalina" and password == "12345":
            st.sidebar.success("Logged in!")
            return True
        else:
            st.sidebar.error("Incorrect username or password")
    return False


if login():
    st.markdown("<h1 style='text-align: center; color: pink;'>❤ happymom.ai ❤</h1>", unsafe_allow_html=True)

    # HOME #
    st.subheader("hi mommy!")
    selected = option_menu(
        menu_title=None,
        options=["Let's eat mom!", "Let's deliver mom!", "Let's get you covered mom!"],
        icons=["", "", ""],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-colour": "green"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "middle",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "green"},
        },
    )

    if selected == "Let's eat mom!":
        st.title(f"Let's eat mom! 🍗")
    if selected == "Let's deliver mom!":
        st.title(f"Let's deliver mom! 👶")
    if selected == "Let's get you covered mom!":
        st.title(f"Let's get you covered mom!❤️‍🩹")

else:
    st.title("Login Page")
    # Add your login page content here