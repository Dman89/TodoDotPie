import json
import os
import time
import functions
from functions import clear
from functions import compute_value
from functions import is_max
from functions import search_for_subject

username=""
subjects=""
long_term_goals={}
life_goals={}
file_life_goals = {}

def add_to_life_goals(g, i):
    global long_term_goals
    x=0
    for item in long_term_goals:
        if item["id"] == i:
            long_term_goals["long"][x]["life_goals"].append(g)
        x+=1
def create_new_set_of_life_goals(linked):
    return {"id": time.time(), "life_goals": [], "linked": linked}

def create_long_term_goals(duration):
    ltg = {"{}".format(duration): []}
    return ltg

def create_long_term_goal(name, sub, rank, impact, progression, value):
    return {"goal": {"name": name, "subject": subject, "rank": rank, "impact": impact, "progression": progression, "value": value}}

def create_goal():
    global subjects
    global username
    name = input(str("> "))
    subject = input(str("""Enter Subject
>"""))
    new_subject = search_for_subject(subject, subjects)
    if new_subject == True:
        subrank = is_max(100)
    else:
        subrank = new_subject
    rank = is_max(10)
    impact = is_max(10)
    progression = is_max(100)
    value = compute_value(subrank, rank, impact, progression)
    goal = create_long_term_goal(name, sub, rank, impact, progression, value)
    return goal

def create_goals(l):
    global long_term_goals
    linked = l
    life_goals = create_new_set_of_life_goals(l)
    tenyr = create_long_term_goals("tenyr")
    tenyr["tenyr"] = create_goals_loop()
    fiveyr = create_long_term_goals("fiveyr")
    fiveyr["fiveyr"] = create_goals_loop()
    threeyr = create_long_term_goals("threeyr")
    threeyr["threeyr"] = create_goals_loop()
    oneyr = create_long_term_goals("oneyr")
    oneyr["oneyr"] = create_goals_loop()
    sixmnth = create_long_term_goals("sixmnth")
    sixmnth["sixmnth"] = create_goals_loop()
    life_goals["life_goals"].append(tenyr)
    life_goals["life_goals"].append(fiveyr)
    life_goals["life_goals"].append(threeyr)
    life_goals["life_goals"].append(oneyr)
    life_goals["life_goals"].append(sixmnth)
    long_term_goals["long"].append(life_goals)

def create_goals_loop():
    run = 1
    arr = []
    while (run == 1):
        goal = create_goal()
        if goal == "":
            run = 0
        else:
            arr.append(goal)
    return arr


def list_options():
    print("""
    Enter ADD, EDIT, REMOVE, LIST, SAVE, EXIT, or SE (Save and Exit)
    """)
    option = input(str(">  "))

def start(u):
    global username
    global subjects
    username = u
    file_loaded = load_file(u)
    subjects = functions.load_subjects(u)
    load_file_life_goals(u)
    if file_loaded == True:
        # Load Options
        list_options()
    else:
        select_linked
        # Go Through Walk Through Wizard

def select_linked():
    global long_term_goals
    global file_life_goals
    select = list_n_choose_file_life_goals(file_life_goals)
    create_goal(select)
    print(long_term_goals)


def list_n_choose_file_life_goals():
    global file_life_goals
    x=0
    z=0
    for item in file_life_goals["list"]:
        x+=1
        if item == file_life_goals["top"]:
            z = x[:]
        print("""#{} - {}""".format(x, item))
    print("We recommend setting up long term goals for {} - #{}".format(file_life_goals["top"], z))
    selection = is_max(len(file_life_goals))
    return file_life_goals["list"][selection]



def load_file_life_goals(u):
    global file_life_goals
    with open("{}_life_goals.json".format(u), "r") as fi:
        file_life_goals = json.load(fi)
        print("""
File Loaded
        """)


def load_file(u):
    global long_term_goals
    try:
        with open("{}_long_term.json".format(u), "r") as fi:
            long_term_goals = json.load(fi)
            print("""
    File Loaded
            """)
            return True
    except FileNotFoundError:
        long_term_goals = {"long": []}
        print("""
    File Created
        """)
        return False


def load_file_of_life_goals(u):
    global life_goals
    try:
        with open("{}_life_goals.json".format(u), "r") as fi:
            life_goals = json.load(fi)
            print("""
    File Loaded
            """)
            return True
    except FileNotFoundError:
        return False


def save_file(u):
    global long_term_goals
    data = long_term_goals
    with open("{}_long_term.json".format(u), mode="w") as file:
        json.dump({"long": data}, file)
        print("""
    Saved File...
        """)
