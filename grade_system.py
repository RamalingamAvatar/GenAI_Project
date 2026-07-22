# Get the user Mark as input
marks = input("Enter Student Marks (or A for Absent): ")

# Validate if Ansent as A. user can input as A/a this will convert into uppercase
if marks.upper() == "A":
    grade = "Absent"

    # simply if we validate as isdigit it wont validate flot digit/text, it consider only whole number, so using replace to replace DOT to remove
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
        grade = "Invalid Marks, please check............test"
else:
    grade = "Invalid Input"
print("Result:", grade)