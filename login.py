import streamlit as st

def login():
    st.markdown("<h2 style='text-align: center; color: pink;'>Login Page</h2>", unsafe_allow_html=True)
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.checkbox("Login"):
        if username == "example" and password == "12345":
            st.sidebar.success("Logged in!")
            return True
        else:
            st.sidebar.error("Incorrect username or password")
    return False

if login():
    st.title("Main Page")
    # Add your main page content here

    # Define the pages
    def home():
        st.title("Home Page")
        st.write("Welcome to the home page!")
    
    def about():
        st.title("About Page")
        st.write("This is the about page.")
    
    def contact():
        st.title("Contact Page")
        st.write("Please contact us at contact@example.com")
    
    # Define the main function to run the app
    def main():
        st.set_page_config(page_title="Multi-page App")
    
        # Define the navigation menu
        pages = {
            "Home": home,
            "About": about,
            "Contact": contact
        }
    
        # Render the navigation menu
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", list(pages.keys()))
    
        # Run the selected page
        page = pages[selection]
        page()

else:
    # Set page config
    st.set_page_config(page_title="happymom.ai", page_icon=":baby:", layout="wide")

    # Set up the web app
    st.markdown("<h1 style='text-align: center; color: pink;'>❤ happymom.ai ❤</h1>", unsafe_allow_html=True)
