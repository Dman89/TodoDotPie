def p(msg):
    print(msg)

def start_goal_finding():
    p("Enter your life goals, one by one:")
    enter_mode = 1
    x = 0
    goals_arr = []
    while (enter_mode == 1):
        p("\n")
        goal_item = input(str("> "))
        if "EXIT" in goal_item:
            enter_mode = 0
        else:
            goals_arr.append(goal_item)
            x+=1
    return goals_arr

def selecting_priorities(req):
    x=1
    for item in req:
        print("#{} - {}".format(x,item))
        x+=1
    return x


goalsArr = start_goal_finding()
selecting_priorities(goalsArr)
