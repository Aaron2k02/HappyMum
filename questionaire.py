# from pathlib import Path
import streamlit as st

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
breech_position = st.radio("Is your baby currently in a breech position?", options=[0, 1])

# Question 4: Yes/No
cephalic_position = st.radio("Is your baby currently in a cephalic position?", options=[0, 1])

# Question 5: Yes/No
baby_position = st.radio("Is your baby currently in a position other than breech or cephalic?", options=[0, 1])

# Question 6: Yes/No
amniotic_fluid_level  = st.radio("Is your amniotic fluid level normal?", options=[0, 1])

# Question 7: Yes/No
hypertension  = st.radio("Do you have hypertension?", options=[0, 1])

# Question 8: Yes/No
pregnancy_induced_hypertension  = st.radio("Do you have pregnancy-induced hypertension?", options=[0, 1])

# Question 9: Yes/No
gestational_diabetes_mellitus  = st.radio("Do you have gestational diabetes mellitus?", options=[0, 1])

# Question 10: Yes/No
diabetes = st.radio("Do you have diabetes?", options=[0, 1])

# Import model 
import pickle

# Import library
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Load model from file
with open('delivery_mode_model.sav', 'rb') as f:
    model = pickle.load(f)

# Check if all questions have been answered
#if None not in user_inputs.values():
    # Submit button
    if st.button('Submit'):
        # Generate output
        inputs = {'mum_age': [age], 'mum_height': [height], 'presentation_breech': [breech_position],
                'presentation_cephalic': [cephalic_position], 'presentation_other': [baby_position],
                'amniotic_normal': [amniotic_fluid_level], 'hypertension_nil': [1-hypertension],
                'hypertension_pih': [pregnancy_induced_hypertension],
                'diabetes_gdm': [gestational_diabetes_mellitus], 'diabetes_nil': [1-diabetes]}
        st.write("Here are your inputs:")
        st.write(inputs)

        #Dictionary 
        Birth_delivery = ["Vaginal Delivery","Lower segment Caesarean section","Others"]
        
        inputs_df = pd.DataFrame(data = inputs)

        test_Predict = model.predict(inputs_df)

        test_Predict_prob = model.predict_proba(inputs_df)

        # Probability of each birth delivery method class 
        st.write('Percentage of probability')
        j = 0
        x_list = []
        y_list = []
        for i in test_Predict_prob[0]:
            st.write("{} : {c}". format(Birth_delivery[j], c = i*100))
            y_list.append(Birth_delivery[j])
            x_list.append(i*100)
            j += 1

        # Plot bar graph for percentage of probability
        fig, ax = plt.subplots()
        ax.barh(y_list, x_list)
        ax.set_xlabel("Percentage of probability (%)")
        ax.set_ylabel("Delivery Method")
        ax.set_title("Percentage of each method")
        st.pyplot(fig)

#else :
#    st.warning('Please answer all questions before submitting.')

