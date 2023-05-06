import streamlit as st
from PIL import Image
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from tensorflow.keras.models import load_model
import requests
from bs4 import BeautifulSoup
import datetime as dt

model = load_model(r'C:\Users\Avienash\Downloads\ImageCaloriesCalc\myfood11_mobilenetv2.h5')
labels = {0: 'Fried Chicken', 1: 'Boiled Eggs', 2: 'Burger', 3: 'French Fries', 4: 'Curry Puff', 5: 'Laksa', 6: 'Fried Noodles',
          7: 'Fried Rice', 8: 'Pizza', 9: 'Rice', 10: 'Steak'}

def fetch_calories(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        st.error("Unable to fetch the calories")
        print(e)

def processed_img(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()

def run():
    st.title("Food Calories Calculator")
    st.subheader("Recommended Calorie Intake Per Day = 2000")
    img_file = st.file_uploader("Upload an image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, use_column_width=False)
        save_image_path = r'C:\Users\Avienash\Downloads\ImageCaloriesCalc\uploaded_images/' + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result = processed_img(save_image_path)
            st.success("**Predicted : " + result + '**')
            cal = fetch_calories(result)
            if cal:
                st.warning('**' + cal + ' (for 100 grams)**')
                # Initialize the total_calories key if it does not exist
                if 'total_calories' not in st.session_state:
                    st.session_state['total_calories'] = 0
                # Add the calories to the total_calories counter
                st.session_state['total_calories'] += int(cal.split()[0])

    # Get the current time
    now = dt.datetime.now()
    # Check if the date has changed since the last time this code was run
    if now.date() != st.session_state.get('last_date', now.date()):
        # If the date has changed, update the reward points and reset the total_calories counter
        total_calories = st.session_state.get('total_calories', 0)
        # Check if the total calories is between 1800 and 2200
        if 1800 <= total_calories <= 2200:
            # Add 5 reward points
            st.session_state['reward_points'] = st.session_state.get('reward_points', 0) + 5
        else:
            # Subtract 3 reward points
            st.session_state['reward_points'] = st.session_state.get('reward_points', 0) - 3
        # Reset the total_calories counter
        st.session_state['total_calories'] = 0
        # Store the current date in the session state
        st.session_state['last_date'] = now.date()

    # Display the total calories counter in the bottom right corner of the page
    st.markdown(f"**_Total Calories: {st.session_state.get('total_calories', 0)}_**")
    # Display the reward points counter in the top right corner of the page
    st.text('')
    st.info(f"**Reward Points: {st.session_state.get('reward_points', 0)}**")

run()