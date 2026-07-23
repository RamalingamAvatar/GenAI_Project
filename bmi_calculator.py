import streamlit as st

# pip install streamlit
# run streamlit run bmi_calculator.py

# Show a title
st.title("BMI Calculator")

# Ask for weight (in kg)
weight = st.number_input("Enter your weight (in kg):", min_value=1.0, step=0.1)

# Ask for height (in cm)
height = st.number_input("Enter your height (in cm):", min_value=1.0, step=0.1)

# # Button Calculate BMI
if st.button("Calculate BMI"):
    if weight > 0 and height > 0:
        bmi = weight / ((height / 100) ** 2)
        st.write(f"Your BMI is: {bmi:.2f}")

        # Determine BMI category
        if bmi < 18.5:  
            st.warning("You are underweight.")
        elif 18.5 <= bmi < 24.9:
            st.success("You have a normal weight.")
        elif 25 <= bmi < 29.9:
            st.warning("You are overweight.")
        else:
            st.warning("You are obese.")
    else:
        st.error("Please enter valid weight and height values.")