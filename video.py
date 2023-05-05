# from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

#st.set_page_config(page_title="happymom.ai", page_icon=":baby:", layout="wide")
st.markdown("<h1 style='text-align: center; color: pink;'>❤ happymom.ai ❤</h1>", unsafe_allow_html=True)


# LOGIN #

def login():
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.checkbox("Login"):
        if username == "mum" and password == "1":
            st.sidebar.success("Logged in!")
            return True
        else:
            st.sidebar.error("Incorrect username or password")
    return False


if login():
   # st.markdown("<h1 style='text-align: center; color: pink;'>❤ happymom.ai ❤</h1>", unsafe_allow_html=True)
   # image = Image.open('/Users/magdalenamayaanakdavid/PycharmProjects/my_website.py/preg.jpeg')
   # st.image(image, caption='Healthy Baby, Happy Mum', use_column_width=True)
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
            "container": {"padding": "0!important", "background-colour": "cream"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "middle",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "cream"},
        },
    )

    if selected == "Let's eat mom!":
        st.title(f"Let's eat mom! 🍗")
        # ash
    if selected == "Let's deliver mom!":
        st.title(f"Let's deliver mom! 👶")

        # Define a dictionary to store the user's inputs
        user_inputs = {'age': None,
                       'height': None,
                       'breech_position': None,
                       'cephalic_position': None,
                       'baby_position': None,
                       'amniotic_fluid_level': None,
                       'hypertension': None,
                       'pregnancy_induced_hypertension': None,
                       'gestational_diabetes_mellitus': None,
                       'diabetes': None}

        # Question 1: Age
        age = st.number_input("What is your age?", min_value=0, max_value=120, step=1)

        # Question 2: Height
        height = st.number_input("What is your height in centimeters?", min_value=0.0, max_value=300.0, step=0.01)

        # Question 3: Yes/No
        breech_position = st.radio("Is your baby currently in a breech position?", options=['No', 'Yes'])
        breech_position = 1 if breech_position == 'Yes' else 0

        # Question 4: Yes/No
        cephalic_position = st.radio("Is your baby currently in a cephalic position?", options=['No', 'Yes'])
        cephalic_position = 1 if cephalic_position == 'Yes' else 0

        # Question 5: Yes/No
        baby_position = st.radio("Is your baby currently in a position other than breech or cephalic?",
                                 options=['No', 'Yes'])
        baby_position = 1 if baby_position == 'Yes' else 0

        # Question 6: Yes/No
        amniotic_fluid_level = st.radio("Is your amniotic fluid level normal?", options=['No', 'Yes'])
        amniotic_fluid_level = 1 if amniotic_fluid_level == 'Yes' else 0

        # Question 7: Yes/No
        hypertension = st.radio("Do you have hypertension?", options=['No', 'Yes'])
        hypertension = 1 if hypertension == 'Yes' else 0

        # Question 8: Yes/No
        pregnancy_induced_hypertension = st.radio("Do you have pregnancy-induced hypertension?", options=['No', 'Yes'])
        pregnancy_induced_hypertension = 1 if pregnancy_induced_hypertension == 'Yes' else 0

        # Question 9: Yes/No
        gestational_diabetes_mellitus = st.radio("Do you have gestational diabetes mellitus?", options=['No', 'Yes'])
        gestational_diabetes_mellitus = 1 if gestational_diabetes_mellitus == 'Yes' else 0

        # Question 10: Yes/No
        diabetes = st.radio("Do you have diabetes?", options=['No', 'Yes'])
        diabetes = 1 if diabetes == 'Yes' else 0

        # Import model
        import pickle

        # Import library
        import pandas as pd
        import numpy as np
        import joblib
        import matplotlib.pyplot as plt

        # Load model from file
        with open('/Users/magdalenamayaanakdavid/PycharmProjects/my_website.py/delivery_mode_model.sav', 'rb') as f:
            model = pickle.load(f)

            # Check if all questions have been answered
            # if None not in user_inputs.values():
            # Submit button
            if st.button('Submit'):
                # Generate output
                inputs = {'mum_age': [age], 'mum_height': [height], 'presentation_breech': [breech_position],
                          'presentation_cephalic': [cephalic_position], 'presentation_other': [baby_position],
                          'amniotic_normal': [amniotic_fluid_level], 'hypertension_nil': [1 - hypertension],
                          'hypertension_pih': [pregnancy_induced_hypertension],
                          'diabetes_gdm': [gestational_diabetes_mellitus], 'diabetes_nil': [1 - diabetes]}

                # Dictionary
                Birth_delivery = ["Vaginal Delivery", "Lower segment Caesarean section", "Others"]

                inputs_df = pd.DataFrame(data=inputs)

                test_Predict = model.predict(inputs_df)

                test_Predict_prob = model.predict_proba(inputs_df)

                # Probability of each birth delivery method class
                st.write('Percentage of probability')
                j = 0
                x_list = []
                y_list = []
                for i in test_Predict_prob[0]:
                    st.write("{} : {c}".format(Birth_delivery[j], c=i * 100))
                    y_list.append(Birth_delivery[j])
                    x_list.append(i * 100)
                    j += 1

                # Plot bar graph for percentage of probability
                fig, ax = plt.subplots()
                ax.barh(y_list, x_list)
                ax.set_xlabel("Percentage of probability (%)")
                ax.set_ylabel("Delivery Method")
                ax.set_title("Percentage of each method")
                st.pyplot(fig)

                # Print recommended delivery method result and note
                if test_Predict[0] == 0:
                    result = 'Vaginal Delivery'
                    note = 'Stay active and upright during labour'
                elif test_Predict[0] == 1:
                    result = 'Lower segment Caesarean section'
                    note = 'You may need to adjust your exercise routine depending on your individual situation'
                else:
                    result = 'Others'
                    note = 'You might need to consult with a doctor for a suitable birth delivery method'

                st.write("\nYour Recommended Delivery Method Result:", result)
                st.write(note)

    if selected == "Let's get you covered mom!":
        st.title(f"Let's get you covered mom!❤️‍🩹")

else:
    image = Image.open('/Users/magdalenamayaanakdavid/PycharmProjects/my_website.py/preg.jpeg')
    st.image(image, use_column_width=True)
    st.markdown("<h1 style='text-align: center; color: brown;'>Healthy Baby, Happy Mum</h1>", unsafe_allow_html=True)
