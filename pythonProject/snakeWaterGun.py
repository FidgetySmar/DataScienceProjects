import random

def userInput(n):
    """This function will return items according to the key selected by player"""
    a = {"s": "Snake", "w": "Water", "g": "Gun"}
    return a.get(n)


lst = ["Snake", "Water", "Gun"] # list that is used for random selection
i = 0
rounds = int(input("Enter number of rounds: "))
count_win = 0
count_loss = 0
count_draw = 0
while i < rounds:
    print("Press s to select Snake:")
    print("Press w to select Water:")
    print("Press g to select Gun:")
    plr_input = input("Type here: ")    # input to be selected by player
    if plr_input != 's' and plr_input != 'w' and plr_input != 'g':
        print("Wrong selection \n PLEASE TRY AGAIN")
        continue

    plr_out = userInput(plr_input)  # storing player output
    comp_out = random.choice(lst)   # storing random output
    print(f"Computer selected {comp_out}")
    if plr_out == comp_out:
        count_draw += 1
        print("!!!DRAW!!!")
    elif plr_out == "Snake" and comp_out == "Water":
        count_win += 1
        print("!!!YOU WIN!!!")
    elif plr_out == "Gun" and comp_out == "Snake":
        count_win += 1
        print("!!!YOU WIN!!!")
    elif plr_out == "Water" and comp_out == "Gun":
        count_win += 1
        print("!!!YOU WIN!!!")
    else:
        count_loss += 1
        print("!!!COMPUTER WIN!!!")
    i += 1

# print("Round won by player is ", count_win, "whereas by computer is ", count_loss)
print(f"Round won by player is {count_win} whereas by computer is {count_loss} and number of draws are {count_draw}")
if count_win > count_loss:
    print("Player win")
elif count_win < count_loss:
    print("Computer win")
else:
    print("It's a draw!!")
