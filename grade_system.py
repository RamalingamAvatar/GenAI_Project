marks = input("Enter Student Marks (or A for Absent): ")

if marks.upper() == "A":
    grade = "Absent"
    # marks.isdigit():
elif marks.replace(".", "", 1).isdigit():
    marks = float(marks)

    if 90 <= marks <= 100:
        grade = "A"
    elif 80 <= marks < 90:
        grade = "B"
    elif 70 <= marks < 80:
        grade = "C"
    elif 60 <= marks < 70:
        grade = "D"
    elif 0 <= marks < 60:
        grade = "E"
    else:
        grade = "Invalid Marks"
else:
    grade = "Invalid Input"

print("Result:", grade)