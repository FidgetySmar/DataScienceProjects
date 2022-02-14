# to get date and time
def getDate():
    import datetime
    return datetime.datetime.now()


# to select the client
def selectName():
    """Select the client that need to be logged or retrieved"""
    name = {1: "Shashank Smar",
            2: "Saurav Anand",
            3: "Premashish Anand"}
    # a = {1 : "Food",
    #      2 : "Exercise"}
    # print(name)

    for key, value in name.items():
        # print("Press", key, "for", value)
        print("Press", key, "for", value, "\n", end="")
    n = int(input("Enter a number to select a client: "))
    if n > 3:
        print("Please select a number between 1 to 3")
    else:
        return n


# to select the action
def selectFileAction():
    """Select the action that needs to be performed"""
    action = {1: "Log",
              2: "Retrieve"}
    for key, value in action.items():
        print("Press", key, "for", value, "\n", end="")
    a = int(input("Chose your action: "))
    if a > 2:
        print("Please select 1 or 2")
    else:
        return a


# to select the task
def selctTask():
    """Select the the task that is to be logged or retrieved"""
    task = {1: "Food",
            2: "Exercise"}

    for key, value in task.items():
        print("Press", key, "for", value, "\n", end="")
    b = int(input("Chose your task: "))
    if b > 2:
        print("Please select 1 or 2")
    else:
        return b


# actual action is performed
def action(n, a, b):
    """Performs the desired action"""
    # action 1 : food log for Shashank Smar
    if n == 1 and a == 1 and b == 1:
        value = input("Food taken ")
        with open("Shashank Smar Food.txt", "a") as shashankFood:
            shashankFood.write(str([str(getDate())]) + ":" + value + "\n")
            print("write successful")

    # action 2 : exercise log for Shashank Smar
    if n == 1 and a == 1 and b == 2:
        value = input("Exercise performed ")
        with open("Shashank Smar Exercise.txt", "a") as shashankExercise:
            shashankExercise.write(str([str(getDate())]) + ":" + value + "\n")
            print("write successful")

    # action 3 : food log for Saurav Anand
    if n == 2 and a == 1 and b == 1:
        value = input("Food taken ")
        with open("Saurav Anand Food.txt", "a") as sauravFood:
            sauravFood.write(str([str(getDate())]) + ":" + value + "\n")
            print("write successful")

    # action 4 : exercise log Saurav Anand
    if n == 2 and a == 1 and b == 2:
        value = input("Exercise performed ")
        with open("Saurav Anand Exercise.txt", "a") as sauravExercise:
            sauravExercise.write(str([str(getDate())]) + ":" + value + "\n")
            print("write successful")

    # action 5 : food log for Premashish Anand
    if n == 3 and a == 1 and b == 1:
        value = input("Food taken ")
        with open("Premashish Anand Food.txt", "a") as premashishFood:
            premashishFood.write(str([str(getDate())]) + ":" + value + "\n")
            print("write successful")

    # action 6 : exercise log Premashish Anand
    if n == 3 and a == 1 and b == 2:
        value = input("Exercise performed ")
        with open("Premashish Anand Exercise.txt", "a") as premashishExercise:
            premashishExercise.write(str([str(getDate())]) + ":" + value + "\n")
            print("write successful")

    # action 7 : retrieve food info for Shashank Smar
    if n == 1 and a == 2 and b == 1:
        with open("Shashank Smar Food.txt", "r") as shashankFood:
            p = shashankFood.read()
            print(p)

    # action 8 : retrieve exercise info for Shashank Smar
    if n == 1 and a == 2 and b == 2:
        with open("Shashank Smar Exercise.txt", "r") as shashankExercise:
            q = shashankExercise.read()
            print(q)

    # action 9 : retrieve food info for Saurav Anand
    if n == 2 and a == 2 and b == 1:
        with open("Saurav Anand Food.txt", "r") as sauravFood:
            r = sauravFood.read()
            print(r)

    # action 10 : retrieve exercise info for Saurav Anand
    if n == 2 and a == 2 and b == 2:
        with open("Saurav Anand Exercise.txt", "r") as sauravExercise:
            s = sauravExercise.read()
            print(s)

    # action 11 : retrieve food info for Premashish Anand
    if n == 3 and a == 2 and b == 1:
        with open("Premashish Anand Food.txt", "r") as premashishFood:
            t = premashishFood.read()
            print(t)

    # action 12 : retrieve exercise info for Premashish Anand
    if n == 3 and a == 2 and b == 2:
        with open("Premashish Anand Exercise.txt", "r") as premashishExercise:
            u = premashishExercise.read()
            print(u)


n = selectName()
a = selectFileAction()
b = selctTask()
action(n, a, b)

# print(type(str([str(getDate())])))
