from terminal_files.quiz import run_quiz
from terminal_files.score import display_stats

def exit_game():
    print("Thank you for playing! Goodbye!")



def main():
    print("Welcome, Welcome! What would you like to do today?\n")
    while choose_and_run_task():
        print("\nWhat would you like to do next?\n")
        pass


def choose_and_run_task():

    print("1. Start Quiz")
    print("2. View Scores")
    print("3. Exit\n")

    user_response = input("Input 1, 2, or 3: ")
    while not user_response.isdigit() or not (1 <= int(user_response) <= 3):
        user_response = input("Please input a valid option between 1 and 3: ")

    user_response = int(user_response)

    if user_response == 1:
        run_quiz()
    if user_response == 2:
        display_stats()
    if user_response == 3:
        exit_game()
        return False

    return True

"""
#make a choose_game_mode function when the user chooses the game, it 
returns the id of the game they chose, and pick game runs on all 
of that.
so most of the functions take in the id of the game type



"""
if __name__ == "__main__":
    main()