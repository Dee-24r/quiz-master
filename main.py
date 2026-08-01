from quiz import run_quiz
from score import display_top_5
from utils import choose_game


def main():
    print("Welcome, Welcome! What would you like to do today?\n")

    print("1. Start Quiz")
    print("2. View Scores\n")

    user_response = input("Input 1 or 2: ")
    while not (1 <= int(user_response) <= 2):
        user_response = input("Please input a valid option between 1 and 2: ")

    if int(user_response) == 1:
        run_quiz()
    if int(user_response) == 2:
        display_top_5()

if __name__ == "__main__":
    main()