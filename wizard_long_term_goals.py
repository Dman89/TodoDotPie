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
master=""
long_term_goals={}
life_goals={}
file_life_goals = {}
run_list = 1

def add_to_life_goals(g, i):
    global long_term_goals
    x=0
    for item in long_term_goals:
        if item["id"] == i:
            long_term_goals["long"][x]["life_goals"].append(g)
        x+=1
def create_new_set_of_life_goals(linked):
    return {"id": time.time(), "life_goals": [], "linked": linked}
def create_long_term_goals(duration, p, m):
    ltg = {"time": duration, "goals": [], "parent": p, "master": m}
    return ltg
def create_long_term_goal(name, sub, rank, impact, progression, value):
    return {"goal": {"name": name, "subject": sub, "rank": rank, "impact": impact, "progression": progression, "value": value}}
def create_goal(d, s):
    global subjects
    global username
    print("""\nCreate {} Goals for {}:
    Type EXIT to stop adding goals for the {} timeframe\n\n    Name:""".format(d, s, d))
    name = functions.get_input()
    if "EXIT" not in name:
        print("Subject:")
        subject = functions.get_input()
        if "EXIT" not in subject:
            new_subject = search_for_subject(subject, subjects)
            if new_subject == True:
                print("Subject Value (1 - 100):")
                subrank = is_max(100)
            else:
                subrank = new_subject
            sub = {"rank": subrank, "name": subject}
            if new_subject == True:
                subjects.append(sub)
            print("Rank (1 - 10):")
            rank = is_max(10)
            if rank >= 0:
                print("Impact (1 - 10):")
                impact = is_max(10)
                if impact >= 0:
                    print("Progression (1 - 100):")
                    progression = is_max(100)
                    if progression >= 0:
                        value = compute_value(subrank, rank, impact, progression)
                        goal = create_long_term_goal(name, sub, rank, impact, progression, value)
                        return goal
    return False
def create_goals(l):
    global master
    global long_term_goals
    linked = l
    life_goals = create_new_set_of_life_goals(l)
    print_alert_of_new_loop("Ten Year")
    tenyr = create_long_term_goals("tenyr", "", "")
    tenyr["goals"] = create_goals_loop("Ten Year", l)
    master = create_master_goal_loop(tenyr["goals"])
    fiveyr = create_child_goal_loop("Five Year", "fiveyr", l)
    threeyr = create_parent_goal_loop("Three Year", "threeyr", l, fiveyr)
    twoyr = create_parent_goal_loop("Two Year", "twoyr", l, threeyr)
    oneyr = create_parent_goal_loop("One Year", "oneyr", l, twoyr)
    sixmnth = create_parent_goal_loop("Six Months", "sixmnth", l, oneyr)
    threemnth = create_parent_goal_loop("Three Months", "threemnth", l, sixmnth)
    onemnth = create_parent_goal_loop("One Months", "onemnth", l, threemnth)
    life_goals["life_goals"].append(tenyr)
    life_goals["life_goals"].append(fiveyr)
    life_goals["life_goals"].append(threeyr)
    life_goals["life_goals"].append(twoyr)
    life_goals["life_goals"].append(oneyr)
    life_goals["life_goals"].append(sixmnth)
    life_goals["life_goals"].append(threemnth)
    life_goals["life_goals"].append(onemnth)
    long_term_goals["long"].append(life_goals)
def create_goals_loop(d, s):
    run = 1
    arr = []
    x=0
    while (run == 1):
        x+=1
        goal = create_goal(d, s)
        if goal == False:
            run = 0
            if x == 1:
                return create_goal(d, s)
        else:
            arr.append(goal)
    clear()
    return arr
def create_child_goal_loop(n, d, l):
    global master
    p = ""
    long_term_goal = {"goals": []}
    for item in master:
        print_alert_of_new_loop(n)
        print_alert_of_new_loop_parent(item, item)
        long_term_goal = create_long_term_goals(d, item, item)
        long_term_goal["goals"] = create_goals_loop(n, l)
    return long_term_goal
def create_parent_goal_loop(n, d, l, arraY):
    long_term_goal = {"goals": []}
    m=arraY["master"]
    for item in arraY["goals"]:
        p=item["goal"]["name"]
        print_alert_of_new_loop(n)
        print_alert_of_new_loop_parent(m, p)
        long_term_goal = create_long_term_goals(d, p, m)
        long_term_goal["goals"].extend(create_goals_loop(n, l))
    return long_term_goal
def create_master_goal_loop(arraY):
    arr = []
    for item in arraY:
        arr.append(item["goal"]["name"])
    return (arr)
def start(u):
    global username
    global subjects
    global run_list
    username = u
    file_loaded = load_file(u)
    subjects = functions.load_subjects(u)
    load_file_life_goals(u)
    if file_loaded == True:
        while (run_list == 1):
            # Load Options
            list_options()
    else:
        select_linked()
        # Go Through Walk Through Wizard
def save_file(u):
    global long_term_goals
    with open("{}_long_term.json".format(u), mode="w") as file:
        json.dump(long_term_goals, file)
        print("""
    Saved File...
        """)
def save_file_subjects(u):
    global subjects
    data = subjects
    with open("{}_subjects.json".format(u), mode="w") as file:
        json.dump({"subjects": data}, file)
        print("""
    Saved File...
        """)
def select_linked():
    global long_term_goals
    global file_life_goals
    global username
    select = list_n_choose_file_life_goals()
    create_goals(select)
    save_file(username)
    save_file_subjects(username)
def list_life_goal():
    global long_term_goals
    print(long_term_goals, "\n\n\n")
    for item in long_term_goals["long"]:
        print(item, "\n\n\n")
        for ite in item["life_goals"]:
            print(ite)
def list_options():
    global username
    global run_list
    print("""
    Enter ADD, EDIT, REMOVE, LIST, SAVE, EXIT, or SE (Save and Exit)
    """)
    option = input(str(">  "))
    if "ADD" in option:
        add_life_goal()
    elif "EDIT" in option:
        edit_life_goal()
    elif "REMOVE" in option:
        remove_life_goal()
    elif "LIST" in option:
        list_life_goal()
    elif "SAVE" in option:
        save_file(username)
        save_file_subjects(username)
    elif "EXIT" in option:
        run_list = 1
    elif "SE" in option:
        save_file(username)
        save_file_subjects(username)
        run_list = 1
def list_n_choose_file_life_goals():
    global file_life_goals
    x=0
    z=0
    for item in file_life_goals["list"]:
        x+=1
        if item == file_life_goals["top"]:
            z = x
        print("""#{} - {}""".format(x, item))
    print("We recommend setting up long term goals for {} - #{}".format(file_life_goals["top"], z))
    selection = is_max(len(file_life_goals["list"]))
    return file_life_goals["list"][selection]
def load_file_life_goals(u):
    global file_life_goals
    with open("{}_life_goals.json".format(u), "r") as fi:
        file_life_goals = json.load(fi)
        print("""
    Life Goals File Loaded
        """)
def load_file(u):
    global long_term_goals
    try:
        with open("{}_long_term.json".format(u), "r") as fi:
            long_term_goals = json.load(fi)
            print("""
    Long Term Goals File Loaded
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
def print_alert_of_new_loop(n):
    print("""

            *> {} <*

    """.format(n))
def print_alert_of_new_loop_parent(m, p):
    print("""

            *> In {} for {} <*

    """.format(m, p))
def print_goals(ltgs):
    x=0
    arr = []
    for ltg in ltgs["goals"]:
        x+=1
        arr.append(ltg["goal"]["name"])
        print("     *-> {} <-*     ".format(x))
        print_goal(ltg, ltgs["master"], ltgs["parent"])
        print("     *-> {} <-*     ".format(x))
    return arr
def print_goal(ltg, m, p):
    value = (ltg["goal"]["value"] / 10000)
    print("""Name: {}
    Value: {}
        Subject: {}
            Master: {}
                Parent: {}
        """.format(ltg["goal"]["name"], value, ltg["goal"]["subject"]["name"], m, p))
