# pip install streamlit pandas
# run streamlit run studentgrademanager.py
# 
import streamlit as st
import pandas as pd
import os

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background-color: #81C784;
}

.main-title{
    text-align:center;
    color:white;
    font-size:42px;
    font-weight:bold;
}

.block{
    background:white;
    padding:40px;
    border-radius:15px;
    box-shadow:0px 5px 20px rgba(0,0,0,0.2);
}

div.stButton > button{
    width:100%;
    background:#1976D2;
    color:white;
    font-size:16px;
    border-radius:10px;
    height:45px;
}

div.stButton > button:hover{
    background:#0D47A1;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎓 Student Grade Manager</h1>", unsafe_allow_html=True)

FILE = "students.csv"

# -----------------------------
# Create CSV if not exists
# -----------------------------
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=[
        "Roll No","Name",
        "Math","Science","English","Social","Computer",
        "Total","Average","Grade","Status"
    ])
    df.to_csv(FILE,index=False)

df = pd.read_csv(FILE)

# -----------------------------
# Functions
# -----------------------------
def grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

def status(marks):
    return "PASS" if min(marks) >= 35 else "FAIL"

# -----------------------------
# Dashboard
# -----------------------------
c1,c2,c3,c4 = st.columns(4)

c1.metric("👨‍🎓 Students",len(df))

if len(df)>0:
    c2.metric("📈 Average",round(df["Average"].mean(),2))
    c3.metric("🏆 Highest",df["Average"].max())
    c4.metric("🥇 Top Grade",df.iloc[df["Average"].idxmax()]["Name"])
else:
    c2.metric("📈 Average",0)
    c3.metric("🏆 Highest",0)
    c4.metric("🥇 Top Grade","-")

st.divider()

tab1,tab2,tab3 = st.tabs(["➕ Add Student","📋 Student List","📊 Dashboard"])

# ============================================================
# ADD STUDENT
# ============================================================
with tab1:

    st.subheader("Add New Student")

    col1,col2=st.columns(2)

    with col1:
        roll=st.text_input("Roll Number")
        name=st.text_input("Student Name")

    with col2:
        math=st.number_input("Math",0,100)
        science=st.number_input("Science",0,100)
        english=st.number_input("English",0,100)
        social=st.number_input("Social",0,100)
        computer=st.number_input("Computer",0,100)

    if st.button("Save Student"):

        total=math+science+english+social+computer
        average=round(total/5,2)

        grd=grade(average)
        sts=status([math,science,english,social,computer])

        new_row=pd.DataFrame([{
            "Roll No":roll,
            "Name":name,
            "Math":math,
            "Science":science,
            "English":english,
            "Social":social,
            "Computer":computer,
            "Total":total,
            "Average":average,
            "Grade":grd,
            "Status":sts
        }])

        df=pd.concat([df,new_row],ignore_index=True)
        df.to_csv(FILE,index=False)

        st.success("Student Added Successfully")

        st.info(f"""
### Result

**Total :** {total}

**Average :** {average}

**Grade :** {grd}

**Status :** {sts}
""")

# ============================================================
# STUDENT LIST
# ============================================================
with tab2:

    st.subheader("Student Records")

    search=st.text_input("Search Roll Number")

    if search:
        data=df[df["Roll No"].astype(str).str.contains(search)]
    else:
        data=df

    st.dataframe(data,use_container_width=True)

    st.download_button(
        "⬇ Download CSV",
        data.to_csv(index=False),
        "students.csv",
        "text/csv"
    )

    st.subheader("Delete Student")

    delete_roll=st.text_input("Enter Roll Number")

    if st.button("Delete"):

        df=df[df["Roll No"]!=delete_roll]
        df.to_csv(FILE,index=False)

        st.success("Deleted Successfully")

# ============================================================
# DASHBOARD
# ============================================================
with tab3:

    if len(df)>0:

        st.subheader("Average Marks")

        chart=df.set_index("Name")["Average"]

        st.bar_chart(chart)

        st.subheader("Grade Distribution")

        st.dataframe(
            df["Grade"].value_counts().rename_axis("Grade").reset_index(name="Count")
        )

        st.subheader("Top 5 Students")

        top=df.sort_values("Average",ascending=False).head(5)

        st.dataframe(top,use_container_width=True)

    else:
        st.info("No Student Data Available")
