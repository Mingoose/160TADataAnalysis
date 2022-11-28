import pandas as pd
names = pd.read_csv("questions-13.csv")

#find most common TA
names["TA_name"] = names["responded_to_by.first_name"] + " " + names["responded_to_by.last_name"]
print(names["TA_name"].value_counts())
#Find most common Student
names["student_name"] = names["asked_by.first_name"] + " " + names["asked_by.last_name"]
print(names["student_name"].value_counts())
#Find most common combo of Student + TA
names["TA_Student_Pair"] = names["TA_name"] + " " + names["student_name"]
print(names["TA_Student_Pair"].value_counts())

# possible ways to calculate most commonly asked questions
for i in range(1,10):
    print("Q" + str(i) + ": " + str(sum(names.text.str.count("Question" + str(i)) + names.text.str.count("question" + str(i)) + names.text.str.count("question " + str(i)) + names.text.str.count("Question " + str(i)) + names.text.str.count("Q" + str(i)) + names.text.str.count("q" + str(i)) + names.text.str.count("Q " + str(i)) + names.text.str.count("q " + str(i)))))
print("attempt 2")
for i in range(1,10):
    print("Q" + str(i) + ": " + str(sum(names.text.str.count(str(i)))))

# get weekdays by date
names["weekday"] = names["time_asked"].apply(lambda x: pd.Timestamp(x).weekday())
print(names["weekday"].value_counts())

maleFile = open("male.txt", "r")
femaleFile = open("female.txt", "r")
maleSet = set()
femaleSet = set()
for line in maleFile.readlines():
    maleSet.add(line.strip().lower())
for line in femaleFile.readlines():
    femaleSet.add(line.strip().lower())
namesSeen = set()
def getGender(name):
    name = name.lower()
    if name in maleSet and name in femaleSet:
        return "cant tell"
    if name in maleSet:
        return "male"
    elif name in femaleSet:
        return "female"
    else:
        if name not in namesSeen:
            print(name)
            namesSeen.add(name)
        return "cant tell"

names["gender"] = names["asked_by.first_name"].apply(lambda x: getGender(x))

# get most common school
def getSchoolFromEmail(email):
    if "seas" in email:
        return "seas"
    elif "wharton" in email:
        return "wharton"
    elif "sas" in email:
        return "sas"
    else:
        return "unreadable email"

names["school"] = names["asked_by.email"].apply(lambda x: getSchoolFromEmail(x))
print(names["school"].value_counts())
indNames = names.drop_duplicates(subset = ["student_name"])
print(indNames["school"].value_counts())
print(names["gender"].value_counts())
print(indNames["gender"].value_counts())