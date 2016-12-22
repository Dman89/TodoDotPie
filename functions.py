import os
from sys import platform

def clear():
    if "win" in platform.lower():
        os.system("cls")
    else:
        os.system("clear")

def p(msg):
    print(msg)

def is_max(max):
    p("""
    Assign a number between 0 and {}""".format(max))
    num = input(str("> "))
    if num == "":
        return False
    else:
        try:
            num = int(num)
        except (ValueError, TypeError):
            return is_max()
        else:
            if num >= 0:
                if num <= 100:
                    return num
                else:
                    return is_max()
            else:
                return is_max()

def compute_value(subrank, rank, impact, progression):
    return ((int(rank) * int(subrank)) * (int(impact) * int(progression)))

def search_for_subject(subj, subjects):
    for x in subjects:
        if subj == x["name"]:
            return x["rank"]
        else:
            continue
    return True

def load_subjects(u):
    try:
        with open("{}_subjects.json".format(u), "r")as DATA:
            subjects = json.load(DATA)
            subjects = subjects["subjects"]
            print("\nSubjects Loaded\n\n")
            print("In", len(subjects), "Subjects.\n\n")
    except FileNotFoundError:
        subjects = []
        print("\nSubjects Created\n\n")
    return subjects
