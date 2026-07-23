import streamlit as st

st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.calc{
    width:380px;
    margin:auto;
    background:#1f2937;
    padding:20px;
    border-radius:20px;
    box-shadow:0 15px 35px rgba(0,0,0,.5);
}

.display{
    background:#111827;
    color:#00ff99;
    padding:18px;
    font-size:32px;
    text-align:right;
    border-radius:10px;
    margin-bottom:15px;
    font-family:Consolas;
    min-height:45px;
}

button[kind="secondary"]{
    height:60px;
    font-size:40px !important;   /* Button text size */
    border-radius:10px !important;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

if "expression" not in st.session_state:
    st.session_state.expression = ""

st.markdown("<h1 style='text-align:center;color:white;'>🧮 Calculator</h1>", unsafe_allow_html=True)

st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown(
    f"<div class='display'>{st.session_state.expression or '0'}</div>",
    unsafe_allow_html=True,
)

buttons = [
    ["7","8","9","/"],
    ["4","5","6","*"],
    ["1","2","3","-"],
    ["0",".","=","+"],
    ["C","⌫","(",")"]
]

for row in buttons:
    cols = st.columns(4)
    for i, b in enumerate(row):
        with cols[i]:
            if st.button(b, use_container_width=True):

                if b == "=":
                    try:
                        st.session_state.expression = str(
                            eval(st.session_state.expression)
                        )
                    except:
                        st.session_state.expression = "Error"

                elif b == "C":
                    st.session_state.expression = ""

                elif b == "⌫":
                    st.session_state.expression = st.session_state.expression[:-1]

                else:
                    if st.session_state.expression == "Error":
                        st.session_state.expression = ""
                    st.session_state.expression += b

st.markdown("</div>", unsafe_allow_html=True)