# from pathlib import Path
import streamlit as st

st.title("Mental Health Pregnancy Questionnaire")

# Part 1: Current Pregnancy Status
part1_current_preg_first = st.selectbox("Are you pregnant for the first time?", 
                                        options=["Yes", "I was pregnant and gave birth during a pandemic"])
# Map selected answer to numerical value
c = 1 if part1_current_preg_first == "Yes" else 2

# Part 2: Demographic Information
women_age = st.selectbox("What is your age?", options=["<35", ">=35"])
women_age = 1 if women_age == "<35" else 2

marriage_age = st.selectbox("At what age did you get married?", options=["<20", "20-29", "30+"])
marriage_age = 1 if marriage_age == "<20" else (2 if marriage_age == "20-29" else 3)

# Part 3: Pregnancy and Health Information
num_pregnancy = st.selectbox("How many times have you been pregnant? options=["One", "Two", "Three", "Four +"])
num_pregnancy = 1 if num_pregnancy == "One" else (2 if num_pregnancy == "Two" else (3 if num_pregnancy == "Three" else 4))

num_abortions = st.selectbox("How many times have you had an abortion?", 
                             options=["Zero", "One time", "Two times +"])
num_abortions = 0 if num_abortions == "Zero" else (1 if num_abortions == "One time" else 2)

education_level = st.selectbox("What is your highest education level?", 
                               options=["<= Secondary School", "> Secondary School"])
education_level = 1 if education_level == "<= Secondary School" else 2

work_status = st.selectbox("Are you currently working?", options=["Yes", "No"])
work_status = 1 if work_status == "Yes" else 2

financial_problem = st.selectbox("Have you faced any financial problems during pregnancy?", 
                                 options=["No", "Yes"])
financial_problem = 0 if financial_problem == "No" else 1

psychological_problem = st.selectbox("Have you faced any psychological problems during pregnancy?", 
                                     options=["No", "Yes"])
psychological_problem = 0 if psychological_problem == "No" else 1

family_income = st.selectbox("Has your family income changed during pregnancy?", 
                             options=["Decreased", "Increased/Same"])
family_income = 1 if family_income == "Decreased" else 2

sleep_duration = st.selectbox("How many hours do you sleep per day?", 
                              options=["<6", "6-8", ">8"])
sleep_duration = 1 if sleep_duration == "<6" else (2 if sleep_duration == "6-8" else 3)

bmi_pregnancy = st.selectbox("What is your BMI during pregnancy?", 
                             options=["Normal", "Thin", "Overweight", "Obese I", "Obese II", "Obese III"])
bmi_pregnancy = 0 if bmi_pregnancy == "Normal" else (1 if bmi_pregnancy == "Thin" else (2 if bmi_pregnancy == "Overweight" else (3 if bmi_pregnancy == "Obese I" else (4 if bmi_pregnancy == "Obese II" else 5)))))

food_adherence_options = {'No/Low Adherence (0-2)': 0, 'Moderate/High Adherence (3-5)': 1}
food_adherence = st.selectbox("How well did you adhere to a healthy food group?", options=list(food_adherence_options.keys()))

# Get the value corresponding to the selected option
food_adherence_value = food_adherence_options[food_adherence]

# Physical Activity During Pregnancy
physical_activity = st.selectbox("How would you describe your physical activity during pregnancy?", options=["Inactive (<1/2 hour)", "Active (>=1/2 hour)"])
physical_activity_value = 0 if physical_activity == "Inactive (<1/2 hour)" else 1

# Smoking During Pregnancy
smoking_during_pregnancy = st.selectbox("Did you smoke during pregnancy?", options=["No", "Yes"])
smoking_during_pregnancy_value = 0 if smoking_during_pregnancy == "No" else 1

# Import model 
import pickle

# Import library
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Load model from file
with open('depression_indicator_model.sav', 'rb') as f:
    model = pickle.load(f)
    
# Submit button
if st.button('Submit'):
    
    inputs = { 'part1_current_preg_first': [part1_current_preg_first], 'WomenAge': [women_age], 'MariageAge': [marriage_age], 'NumberofPregnancy': [num_pregnancy],
                'NumberofAbortions': [num_abortions], 'EducationLevel': [education_level], 'Work': [work_status],
                'FinancialProblem': [financial_problem], 'PsychologicalProb': [psychological_problem],
                'FamilyIncome1': [family_income], 'SleepingAfter': [sleep_duration],
                'BMI_Pregnancy': [bmi_pregnancy], 'Food_Group_Adher_During_CAT': [food_adherence_value],
                'Physical_activity_During_Cat': [physical_activity_value], 'Smoker_During_preg_Cat': [smoking_during_pregnancy_value]}
 
    #Dictionary 
    Depression_severity = ["Mild depression","Moderate  depression","Severe  depression"]

    inputs_df = pd.DataFrame(data = inputs)

    test_Predict = model.predict(inputs_df)

    test_Predict_prob = model.predict_proba(inputs_df)

    # Probability of each birth delivery method class 
    st.write('Percentage of probability')
    j = 0
    x_list = []
    y_list = []
    for i in test_Predict_prob[0]:
        st.write("{} : {c}". format(Depression_severity[j], c = i*100))
        y_list.append(Depression_severity[j])
        x_list.append(i*100)
        j += 1
    
    # Plot bar graph for percentage of probability
    fig, ax = plt.subplots()
    ax.barh(y_list, x_list)
    ax.set_xlabel("Percentage of probability (%)")
    ax.set_ylabel("Depression Severity")
    ax.set_title("Percentage of each Severity")
    st.pyplot(fig)
    
    # Print recommended delivery method result and note
    if test_Predict[0] == 0:
        result = Depression_severity[0]
        note = 'Practice self-care activities such as yoga, meditation, or a hobby that brings joy'
    elif test_Predict[0] == 1:
        result = Depression_severity[1]
        note = 'Seek professional help such as a therapist or a mental health counselor'
    else:
        result = Depression_severity[2]
        note = 'You might need to consult with a doctor and work closely with a mental health team to develop a treatment plan'

    st.write("\nYour Recommended Delivery Method Result:", result)
    st.write(note)