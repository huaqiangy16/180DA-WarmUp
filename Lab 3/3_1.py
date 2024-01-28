#Basic Version
import random

if __name__ == "__main__":
    r, p, s= "Rock","Paper","Scissors"
    Operations = [r, p, s]
    while(True):
        Op = random.choice(Operations)
        print("Please enter Rock, Paper, or Scissors: ", end="")
        User_O = input()

        if(User_O != r and User_O != p and User_O != s):
            print("Invaild Input!")
            continue

        if(Op == User_O):
            print("Result: Tie")
        else:
            if((User_O == r and Op == s) or (User_O == p and Op == r) or (User_O == s and Op == p)):
                print("Result: User Win")
            else:
                print("Result: AI Win")

