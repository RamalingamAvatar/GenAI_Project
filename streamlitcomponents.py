import streamlit as st

st.title("My First Streamlit App")
st.write("Welcome to my first Streamlit application! This is a simple app to demonstrate the capabilities of Streamlit for building interactive web applications with Python.")

# text as input
UserName = st.text_input("Enter your name:")
UserCity = st.text_input("Enter your city name:")
st.write(f"Hello, {UserName} from {UserCity}!")

# Number as input
UserAge = st.number_input("Enter your age:", min_value=1.0, max_value=150.0, step=1.0)
st.write(f"You are {UserAge} years old.")

# Button
if st.button("Submit"):
    st.write(f"From the above inputs, we can say that you are a {UserAge} years old person named {UserName} from {UserCity}.")

# Slider
number=st.slider("Select a number:", 0, 100, 25)
st.write(f"You selected the number: {number}")

# Selectbox
city = st.selectbox("CHoose your city:", ["Chennai", "Madurai", "Coimbatore", "Salem"])
st.write(f"You selected: {city}")

# CheckBox
agree = st.checkbox("I agree to the terms and conditions.")
if agree:
    st.write("Thank you for agreeing!")
else:
    st.write("You did not agree.")

# Showing Messages
st.success("This is a success message!")
st.info("This is an info message.")
st.warning("This is a warning message!")
st.error("This is an error message!")
st.exception("This is an exception message!")
st.help("This is a help message!")
st.write("This is a normal message.")
st.write("This is a message with a link to [Streamlit](https://streamlit.io/).")

#################################################################################################
st.title("This is Title font size.")
st.header("This header font size.")
st.subheader("This subheader font size.")
st.write("This is normal font size.")
st.markdown("This is **bold** and *italic* font size.")

st.header("Features")
st.subheader("Key Features of Streamlit")
st.write("""
- **Interactive Widgets**: Streamlit provides a variety of widgets like sliders, buttons, and text inputs that allow users to interact with your app in real-time.
- **Data Visualization**: Easily create charts and graphs using popular libraries like Matplotlib, Plotly, and Altair.
- **Markdown Support**: You can use Markdown to format your text, making it easy to create headings, lists, and links.
- **Real-time Updates**: Streamlit apps automatically update when the underlying data changes, providing    a seamless experience for users.
""")
st.markdown("For more information, visit the [Streamlit documentation](https://docs.streamlit.io/).")

st.subheader("Key components in Streamlit")
st.write("""
- **st.title()**: Displays a title for your app- Big heading.
- **st.header()**: Displays a header for your app - Medium heading.
- **st.subheader()**: Displays a subheader for your app - Small heading.
- **st.write()**: Displays text or other elements in your app- normal heading.
- **st.markdown()**: Displays Markdown formatted text in your app, eg **bold** or *italic*.
""")

