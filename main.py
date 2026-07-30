from quiz import run_quiz
from score import display_scores # leaderboard


def main():
    print("Pick an option!\n")
    print("1. Start Quiz\n")
    print("2. View Scores\n")
    print("3. Exit\n")

    user_response = input("Option: ")
    while not user_response.isdigit() or not (user_response <= 1 && >= 3)
        if user_response == 1:
            run_quiz()
        if user_response == 2:
            