import streamlit as st
import pandas as pd

# Initialize storage
if "students" not in st.session_state:
    st.session_state.students = []

# Grade function
def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

st.title("🎓 Student Record Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "View Students", "Search Student", "Class Statistics"]
)

# Subjects list
subjects = ["Mathematics", "Science", "English", "Computer", "Social Studies"]

# ---------------- ADD STUDENT ----------------
if menu == "Add Student":

    st.header("Add Student")

    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")

    marks = []

    for subject in subjects:
        m = st.number_input(f"{subject} Marks", 0, 100)
        marks.append(m)

    if st.button("Add Student"):

        for s in st.session_state.students:
            if s["Roll"] == roll:
                st.error("Roll Number already exists")
                st.stop()

        total = sum(marks)
        avg = total / 5
        grade = calculate_grade(avg)

        student = {
            "Name": name,
            "Roll": roll,
            "Mathematics": marks[0],
            "Science": marks[1],
            "English": marks[2],
            "Computer": marks[3],
            "Social Studies": marks[4],
            "Total": total,
            "Average": avg,
            "Grade": grade
        }

        st.session_state.students.append(student)

        st.success("Student Added Successfully")

# ---------------- VIEW STUDENTS ----------------
elif menu == "View Students":

    st.header("All Students")

    if st.session_state.students:

        df = pd.DataFrame(st.session_state.students)

        st.dataframe(df)

    else:
        st.warning("No student records")

# ---------------- SEARCH STUDENT ----------------
elif menu == "Search Student":

    st.header("Search Student")

    search_roll = st.text_input("Enter Roll Number")

    if st.button("Search"):

        found = False

        for s in st.session_state.students:

            if s["Roll"] == search_roll:

                st.write(s)
                found = True

        if not found:
            st.error("Student not found")

# ---------------- CLASS STATISTICS ----------------
elif menu == "Class Statistics":

    st.header("Class Statistics")

    if st.session_state.students:

        df = pd.DataFrame(st.session_state.students)

        total_students = len(df)
        class_avg = df["Average"].mean()

        highest = df.loc[df["Total"].idxmax()]
        lowest = df.loc[df["Total"].idxmin()]

        st.write("Total Students:", total_students)
        st.write("Class Average:", round(class_avg, 2))
        st.write("Highest Scorer:", highest["Name"], "-", highest["Total"])
        st.write("Lowest Scorer:", lowest["Name"], "-", lowest["Total"])

        st.subheader("Grade Distribution")

        grade_counts = df["Grade"].value_counts()

        st.bar_chart(grade_counts)

    else:
        st.warning("No data available")