import os
import json
from sys import platform
def clear():
    if "win" in platform.lower():
        os.system("cls")
    else:
        os.system("clear")
def p(msg):
    print(msg)
def is_max(m):
    # m is for MAX value
    p("""
    Assign a number between 1 and {}""".format(m))
    num = input(str("> "))
    if num == "EXIT":
        return False
    else:
        try:
            num = int(num)
        except (ValueError, TypeError):
            return is_max(m)
        else:
            if num > 0:
                if num <= m:
                    return num
                else:
                    return is_max(m)
            else:
                return is_max(m)
def get_input():
    strin = input(str("> "))
    if strin == "":
        return get_input()
    return strin

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
            print("\n   Subjects Loaded\n\n")
            print("   In", len(subjects), "Subjects.\n\n")
    except FileNotFoundError:
        subjects = []
        print("\nSubjects Created\n\n")
    return subjects
