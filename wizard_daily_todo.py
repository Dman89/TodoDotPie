from functions import clear
import os
import json
content = ""
todos = ""
run_mode = 1
username = ""


def daily_todo_start(usrnam):
    global content
    global todos
    global run_mode
    global username
    username = usrnam
    try:
        with open("{}_subjects.json".format(username), "r") as fi:
            content = json.load(fi)
    except FileNotFoundError:
        print("No Subjects Available")
        return None
    try:
        with open("{}_daily.json".format(username), 'r') as f:
            todos = json.load(f)
    except FileNotFoundError:
        todos = start_todos(username)
        save_todos(username, todos)
    clear()
    while (run_mode == 1):
        function_selector()
    return todos

def list_todos():
    clear()
    print("""
    Listing Daily Todos:
    """)
    list_todos_function()

def list_todos_function():
    global todos
    x=0
    data = []
    for items in todos:
        x+=1
        print("""
        #{} - {}
        """.format(x, items))
        data.append(items)
        for item in todos[items]:
            print("""
            Name: {}
            Value: {}""".format(item['name'], item['rank']))
        print("\n")
    return data

def function_selector():
    global todos
    global username
    global run_mode
    print("""
ADD, EDIT, REMOVE, SAVE, or LIST Daily Todos
    To Exit: Type EXIT or SE to Save and Exit""")
    selector = input(str("""
> """))
    if "ADD" in selector:
        add_todos()
    elif "EDIT" in selector:
        edit_todos()
    elif "SAVE" in selector:
        save_todos(username, todos)
    elif "REMOVE" in selector:
        remove_todos()
    elif "LIST" in selector:
        list_todos()
    elif "EXIT" in selector:
        run_mode = 0
    elif "SE" in selector:
        save_todos(username, todos)
        run_mode = 0

def save_todos(username, todos):
    with open("{}_daily.json".format(username), mode="w") as file:
        json.dump(todos, file)
        print("""
        Saved File...
        """)

def edit_todos():
    global todos
    data = list_todos_function()
    print("""
    Select a Subject:""")
    subject = select_subject()
    name = data[subject]
    todo = todos[name]
    x=0
    for z in todo:
        x+=1
        print("""#{} - {} ({})""".format(x, z["name"], z["rank"]))
    select = select_req(todo)
    print("""
        Type DEL to Delete Item or Leave Blank to Use Old Data
        """)
    new_edit = input(str("""( {} )  > """.format(todo[select]["name"])))
    if "DEL" in new_edit:
        del todos[name][select]
    elif len(new_edit) == 0:
        if "" in new_edit:
            new_edit = todos[name][select]["name"]
            rank = check_edit_rank(todos[name][select])
            todos[name][select] = {"name": new_edit, "rank": rank}
    else:
        rank = check_edit_rank(todos[name][select])
        todos[name][select] = {"name": new_edit, "rank": rank}

def check_edit_rank(todo):
    print("Enter a value in the range of 1 - 100")
    rank = input(str("( {} )  > ".format(todo["rank"])))
    if len(rank) == 0:
        if "" in rank:
            rank = todo["rank"]
    else:
        rank = check_val(rank, todo)
        return rank

def remove_todos():
    data = list_todos_function()
    print("""
    Select a Subject:""")
    subject = select_subject()
    name = data[subject]
    todo = todos[name]
    x=0
    for z in todo:
        x+=1
        print("""#{} - {} ( {} )""".format(x, z['name'],z['rank']))
    select = select_req(todo)
    del todos[name][select]

def check_rank():
    try:
        val = int(input(str("""

        Value from 1 to 100

        > """)))
    except (TypeError, ValueError):
        return check_rank()
    else:
        if val > 0:
            if val < 101:
                return val
            else:
                return check_rank()
        else:
            return check_rank()

def check_val(val, todo):
    try:
        val = int(val)
    except (TypeError, ValueError):
        return check_edit_rank(todo)
    else:
        if val > 0:
            if val < 101:
                return val
            else:
                return check_edit_rank(todo)
        else:
            return check_edit_rank(todo)

def add_todos():
    global todos
    global content
    data = list_todos_function()
    select = select_subject()
    sel = data[select]
    name = todos[sel]
    for z in content:
        if z["name"] == sel:
            v = z["rank"]
    print("""
    Subject: {}
        Rank: {}""".format(sel, v))
    add_todo(sel)
    function_selector()

def add_todo(subj):
    global todos
    todo = input(str("""
    Add a Daily Todo:

    > """))
    rank = check_rank()
    try:
        todos[subj].append({"name": todo, "rank": rank})
    except KeyError:
        todos[subj] = [{"name": todo, "rank": rank}]

def select_subject():
    try:
        select = int(input(str("> ")))
    except (TypeError, ValueError):
        return select_subject()
    else:
        select -= 1
        if select < 0:
            return select_subject()
        if select > len(todos):
            return select_subject()
        else:
            return select

def select_req(req):
    try:
        select = int(input(str("> ")))
    except (TypeError, ValueError):
        return select_req(req)
    else:
        select -= 1
        if select < 0:
            return select_req(req)
        if select > len(req):
            return select_req(req)
        else:
            return select

def start_todos(username):
    global content
    todos = {}
    clear()
    x=0
    for item in content:
        if len(item) == 0:
            del content[x]
            x-=1
        else:
            print("""
        Add Daily Todo for {}
                Rank: {}
            """.format(item["name"], item["rank"]))
            items = add_items()
            name = item["name"]
            todos[name] = items
        x+=1
    return todos

def add_items():
    run_mode = 0
    items = []
    while (run_mode == 0):
        item = input(str("> "))
        if "EXIT" in item:
            run_mode = 1
            return None
        elif len(item) == 0:
            if "" in item:
                run_mode = 1
                return items
        else:
            rank = check_rank()
            items.append({"name": item, "rank": rank})
    return items
