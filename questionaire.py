# from pathlib import Path
import streamlit as st

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
baby_position = st.radio("Is your baby currently in a position other than breech or cephalic?", options=['No', 'Yes'])
baby_position = 1 if baby_position == 'Yes' else 0

# Question 6: Yes/No
amniotic_fluid_level  = st.radio("Is your amniotic fluid level normal?", options=['No', 'Yes'])
amniotic_fluid_level = 1 if amniotic_fluid_level == 'Yes' else 0

# Question 7: Yes/No
hypertension  = st.radio("Do you have hypertension?", options=['No', 'Yes'])
hypertension = 1 if hypertension == 'Yes' else 0

# Question 8: Yes/No
pregnancy_induced_hypertension  = st.radio("Do you have pregnancy-induced hypertension?", options=['No', 'Yes'])
pregnancy_induced_hypertension = 1 if pregnancy_induced_hypertension == 'Yes' else 0

# Question 9: Yes/No
gestational_diabetes_mellitus  = st.radio("Do you have gestational diabetes mellitus?", options=['No', 'Yes'])
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
with open('delivery_mode_model.sav', 'rb') as f:
    model = pickle.load(f)


# Submit button
if st.button('Submit'):
    # Generate output
    inputs = {'mum_age': [age], 'mum_height': [height], 'presentation_breech': [breech_position],
            'presentation_cephalic': [cephalic_position], 'presentation_other': [baby_position],
            'amniotic_normal': [amniotic_fluid_level], 'hypertension_nil': [1-hypertension],
            'hypertension_pih': [pregnancy_induced_hypertension],
            'diabetes_gdm': [gestational_diabetes_mellitus], 'diabetes_nil': [1-diabetes]}

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


