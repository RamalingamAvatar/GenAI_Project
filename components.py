import streamlit as st

st.title("My First Streamlit App")
st.write("Welcome to my first Streamlit application! This is a simple app to demonstrate the capabilities of Streamlit for building interactive web applications with Python.")

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



