from functions import clear
from functions import p
import json

run_priorities_on = 1
goals_arr = []
username = ""
top_one = ""
top_one = ""
final_ans = {}
run_mode = 1


def start_goal_finding():
    clear()
    p("Enter your life goals, one by one:")
    enter_mode = 1
    x = 0
    global run_priorities_on
    global goals_arr
    while (enter_mode == 1):
        p("\n")
        goal_item = add_item()
        if "EXIT" in goal_item:
            enter_mode = 0
            run_priorities_on = 1
        elif len(goal_item) == 0:
            if len(goals_arr) > 2:
                if "" in goal_item:
                    enter_mode = 0
        else:
            goals_arr.append(goal_item)
            x+=1
    return goals_arr

def add_item():
    global goals_arr
    res = input(str("> "))
    if len(res) == 0:
        if len(goals_arr) > 2:
            return ""
        else:
            print("Must have Three Items")
            return add_item()
    else:
        return res

def selecting_priorities(req):
    clear()
    x=1
    for item in req:
        print("""
        #{} - {}
        """.format(x,item))
        x+=1
    return x

def top_3_select(req):
    p("""
    Select the Top 3 Goals:
    """)
    n1 = top_3_check("First")
    n2 = unique_check("Second", n1, top_3_check("Second"), None)
    n3 = unique_check("Third", n1, n2, top_3_check("Third"))
    clear()
    print("""
    {}
    {}
    {}
    """.format(req[n1-1], req[n2-1], req[n3-1]))
    return [req[n1-1], req[n2-1], req[n3-1]]

def unique_check(text, n1, n2, n3):
    if n3:
        if n3 != n1:
            if n3 != n2:
                return n3
            else:
                return unique_check(text, n1, n2, top_3_check("{} [NOT in use] ".format(text)))
        else:
            return unique_check(text, n1, n2, top_3_check("{} [NOT in use] ".format(text)))
    else:
        if n2 != n1:
            return n2
        else:
            return unique_check(text, n1, top_3_check("{} [NOT in use] ".format(text)), None)

def top_3_check(text):
    if "Must be a Number" in text:
        text = "{}".format(text)
    else:
        text = "{} (Must be a Number)".format(text)
    try:
        num = int(input(str("{}: ".format(text))))
    except (ValueError, TypeError):
        top_3_check(text)
    else:
        global goalsArr
        if num < 1:
            return top_3_check(text)
        elif num > len(goalsArr):
            return top_3_check(text)
        return int(num)

def check_remove():
    try:
        remove = int(input(str("> ")))
    except (TypeError, ValueError):
        return check_remove()
    else:
        if remove < 1:
            return check_remove()
        if remove > 3:
            return check_remove()
        return remove

def print_list(data):
    x=1
    for item in data:
        print("""#{} - {}""".format(x, item))
        x+=1

def pick_item():
    try:
        add = int(input(str("> ")))
    except (TypeError, ValueError):
        return pick_item()
    else:
        if add < 1:
            return pick_item()
        if add > 2:
            return pick_item()
        return add

def loaded_file_select_next_step():
    global run_mode
    global goalsArr
    print("""
    ADD, REPICK, EDIT, REMOVE, LIST, EXIT, or SE to Save and Exit
    """)
    option_selected = input(str("> "))
    clear()
    if "ADD" in option_selected:
        add_to_old_file(goalsArr)
        initiate_priorities(goalsArr)
    elif "EDIT" in option_selected:
        edit_priorities()
    elif "REMOVE" in option_selected:
        remove_priorities()
    elif "LIST" in option_selected:
        list_priorities()
    elif "REPICK" in option_selected:
        initiate_priorities(goalsArr)
    elif "EXIT" in option_selected:
        run_mode = 0
        return
    elif "SE" in option_selected:
        save_file_life_goals()
        run_mode = 0
        return

def add_to_old_file(arraY):
    run = 1
    print("Enter Life Goals or Leave Blank and Hit Enter to Save and Exit")
    while (run == 1):
        goal = input(str("> "))
        if len(goal) == 0:
            if "" in goal:
                run = 0
        else:
            arraY.append(goal)
    global goalsArr
    goalsArr = arraY

def save_file_life_goals():
    global username
    global goalsArr
    global top_3
    global top_one
    global final_ans
    final_ans = {"top": top_one[0], "top_three": top_3, "list": goalsArr}
    with open("{}_life_goals.json".format(username), mode="w") as file:
        json.dump(final_ans, file)

def top_3_select_number_one(arraY):
    top_one = arraY
    clear()
    print_list(top_one)
    p("Remove the least important of the three (1, 2, or 3)")
    remove_item = check_remove()
    del top_one[remove_item - 1]
    clear()
    print_list(top_one)
    p("""
    Pick the Most Important of the Two (1 or 2)
    """)
    final_item = pick_item()
    del top_one[final_item - 1]
    return top_one

def initiate_priorities(goalsArr):
    global top_3
    global top_one
    selecting_priorities(goalsArr)
    top_3 = top_3_select(goalsArr)
    top_one = top_3_select_number_one(top_3[:])

def remove_priorities():
    global goalsArr
    selected = display_list_for_edit()
    x=0
    for item in goalsArr:
        if selected in item:
            del goalsArr[x]
        x+=1

def edit_priorities():
    global goalsArr
    selected = display_list_for_edit()
    goalsArr = selected_item_to_edit(selected)

def list_priorities():
    global goalsArr
    print("""
    Printing Life Goals
    """)
    for item in goalsArr:
        print(item)

def selected_item_to_edit(selecteD):
    global goalsArr
    x=0
    for item in goalsArr:
        if selecteD in item:
            res = input(str("{}  > ".format(selecteD)))
            if res == "":
                return goalsArr
            else:
                goalsArr[x] = res
                return goalsArr
        x+=1

def select_item(arraY):
    try:
        num = int(input(str("> ")))
    except (TypeError, ValueError):
        return select_item(arraY)
    else:
        num -= 1
        if num >= 0:
            if num < len(arraY):
                return arraY[num]
            else:
                return select_item(arraY)
        else:
            return select_item(arraY)

def display_list_for_edit():
    global goalsArr
    x=0
    item_arr = []
    for item in goalsArr:
        x+=1
        item_arr.append(item)
        print("#{} - {}".format(x, item))
    return select_item(item_arr)

def top_3_start(usrnam):
    username = usrnam
    global goalsArr
    global final_ans
    global run_mode
    try:
        with open("{}_life_goals.json".format(username), "r") as filez:
            oldGoalsArr = json.load(filez)
            goalsArr = oldGoalsArr["list"]
    except FileNotFoundError:
        goalsArr = start_goal_finding()
        if run_priorities_on == 1:
            initiate_priorities(goalsArr)
    else:
        while (run_mode == 1):
            loaded_file_select_next_step()
    return final_ans
