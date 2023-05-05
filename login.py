import streamlit as st

# Define the username and password
username = "mummyamalina"
password = "happymom"

# Define the Streamlit app

def app():
    # Set page config
    st.set_page_config(page_title="happymom.ai", page_icon=":baby:", layout="wide")

    # Set up the web app
    st.markdown("<h1 style='text-align: center; color: pink;'>❤ happymom.ai ❤</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: pink;'>Login Page</h2>", unsafe_allow_html=True)

    # Define the input fields for the user
    input_username = st.text_input("Username:")
    input_password = st.text_input("Password:", type="password")

    # Check if the username and password match
    if input_username == username and input_password == password:
        st.write("Logged in successfully!")
        if st.button("Go to Homepage"):
            st.set_page_config(
               page_title="Multipage App",
               page_icon="👋",
            )
    elif input_username != "" and input_password != "":
        st.write("Invalid username or password.")

# Run the Streamlit app
if __name__ == '__main__':
    app()