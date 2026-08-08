#IMPORTS
import time
from questions import get_random_questions, get_opentdb_questions, get_quizapi_questions
from score import handle_and_print_score
from utils import configure_quiz, choose_game_mode, format_time_figures, print_formatted_time

"""this will have mode, set by pick_game_mode, and cat, diff, type, and number set by
configure_quiz


game_config = {
    "mode": {
        "id":1,
        "name": "Practice Mode",
        "name_id": "practice_mode",
        "description": "kms"
    },
    "category":{
        "id": 2,
        "name": "dsmn",
        "name_id": "aboni_"
    },
    "difficulty":{
        "id": 2,
        "name": "dsmn",
        "name_id": "aboni_"
    },
    "type":{
        "id": 2,
        "name": "dsmn",
        "name_id": "aboni_"
    },
    "amount": 20
}
"""



def display_question(question):
    """
    Displays the question statement and the options for a given 
    question, one at a time.
    """

    print(question["question_statement"])

    for i, option in enumerate(question["options"]):
        print(f"{i+1}. {option}")



def select_option(question, allow_quit=False):
    """
    Prompts the user to pick and option for the question and check
    the asnwer"""
    prompt = f"Pick an option (1-{len(question['options'])})"

    if allow_quit == True:
        prompt += " or enter 'X' to cancel"
    prompt += ": "

    user_answer = input(prompt)

    if allow_quit and user_answer.upper() == 'X':
        return "quit"
    while not (allow_quit and user_answer.upper() == 'X') and not (user_answer.isdigit() and 1 <= int(user_answer) <= len(question["options"])):
        print("Invalid input!")
        user_answer = input(prompt)

    if allow_quit and user_answer.upper() == 'X':
        return "quit"
    if question["options"][int(user_answer) - 1] == question["answer"]:
        print("Correct answer!\n")
        return True
    else:
        print(f"Wrong answer! The correct answer is: {question['answer']}\n")
        return False


def run_practice_mode(game_config):
    
    list_of_questions = get_opentdb_questions(game_config)
    set_of_questions = {}
    set_of_questions["no_of_questions"] = len(list_of_questions)
    set_of_questions["wrongly_answered"] = []
    set_of_questions["correctly_answered"] = []

    for question in list_of_questions:
        display_question(question)
        result = select_option(question)

        if result:
            (set_of_questions["correctly_answered"]).append(question)
        elif not result:
            set_of_questions["wrongly_answered"].append(question)

    handle_and_print_score(set_of_questions, game_config)


def run_timed_mode(game_config):
    """
    Runs the timed quiz option of the app"""

    list_of_questions = get_opentdb_questions(game_config)
    set_of_questions = {}
    set_of_questions["no_of_questions"] = len(list_of_questions)
    set_of_questions["wrongly_answered"] = []
    set_of_questions["correctly_answered"] = []

    time_limit = 15
    start_time = time.time()

    for question in list_of_questions:
        elapsed_time = time.time() - start_time
        remaining_time = (time_limit - elapsed_time)

        no_of_hours, no_of_minutes, no_of_seconds = format_time_figures(remaining_time)
        print_formatted_time(no_of_hours, no_of_minutes, no_of_seconds)

        if remaining_time <= 0:
            print("Time's up!")
            no_of_answered_questions = len(set_of_questions["wrongly_answered"]) + len(set_of_questions["correctly_answered"])
            print(f"Questions answered {no_of_answered_questions}")
            break

        
        display_question(question)
        result = select_option(question)
        if result:
            set_of_questions["correctly_answered"].append(question)
        elif not result:
            set_of_questions["wrongly_answered"].append(question)

    handle_and_print_score(set_of_questions, game_config)




def run_jeopardy_mode(game_config):
    list_of_questions = get_opentdb_questions(game_config)
    score = 0
    set_of_questions = {}
    set_of_questions["no_of_questions"] = len(list_of_questions)
    set_of_questions["wrongly_answered"] = []
    set_of_questions["correctly_answered"] = []
    
    for question in list_of_questions:
        #should implement the dict here if something is easy
        #meaning we shud get questions of different difficulties. (will come back to this tbh)
        
        if question["difficulty"] == "easy":
            score_addition = 10
        if question["difficulty"] == "medium":
            score_addition = 20
        if question["difficulty"] == "hard":
            score_addition = 30
        display_question(question)

        result = select_option(question)
        if not result:
            score - score_addition
            (set_of_questions["wrongly_answered"]).append(question)
        elif result:
            score + score_addition
            (set_of_questions["correctly_answered"]).append(question)

    handle_and_print_score(set_of_questions, game_config)
    print(f"Score: {score}")




def run_endless_mode(game_config):
    """runs the endless option of the app. keep solving quizzzes
    till the user says exit"""

    print("Hmm!! I see you're locked in?")
    print("Get ready! I won't stop until you say so!")
    set_of_questions = {}
    set_of_questions["no_of_questions"] = 0
    set_of_questions["wrongly_answered"] = []
    set_of_questions["correctly_answered"] = []

    print("Enter 'X' to stop the quiz!")

    while True:
        list_of_questions = get_opentdb_questions(game_config)
        for question in list_of_questions:
            display_question(question)
            
            result = select_option(question, allow_quit=True)
            if result == "quit":
                print("Nice Work")
                handle_and_print_score(set_of_questions, game_config)
                return
            
            else:
                set_of_questions["no_of_questions"] += 1
                if result:
                    (set_of_questions["correctly_answered"]).append(question)
                elif not result:
                    (set_of_questions["wrongly_answered"]).append(question)




def run_exam_mode(game_config):
    print("Not yet implemented")
    

def run_survival_mode(game_config):
    list_of_questions = get_opentdb_questions(game_config)

    set_of_questions = {}
    set_of_questions["no_of_questions"] = len(list_of_questions)
    set_of_questions["wrongly_answered"] = []
    set_of_questions["correctly_answered"] = []

    lives, score = 3, 0
    for question in list_of_questions:
        print(f"You have {lives} lives remaining!")
        display_question(question)
        result = select_option(question)

        if not result:
            lives-=1
            if lives <= 0:
                print("Game Over!")
                return
        else:
            score + 100

    handle_and_print_score(set_of_questions, game_config)


def run_streak_mode(game_config):
    list_of_questions = get_opentdb_questions(game_config)

    set_of_questions = {}
    set_of_questions["no_of_questions"] = len(list_of_questions)
    set_of_questions["wrongly_answered"] = []
    set_of_questions["correctly_answered"] = []
    
    longest_streak = current_streak = 0
    for question in list_of_questions:
        print(f"Longest streak {longest_streak}")
        print(f"Current streak: {current_streak} ")
        display_question(question)

        result = select_option(question)
        
        if not result:
            current_streak = 0
        else:
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak


    handle_and_print_score(set_of_questions, game_config)


def run_millionaire_mode(game_config):
    print("Not yet implemented!")
    


def run_quiz():
    mode = choose_game_mode()
    game_config = configure_quiz(mode)

    mode = game_config["mode"]["name_id"]
    if mode == "practice_mode":
        run_practice_mode(game_config)
    elif mode == "timed_mode":
        run_timed_mode(game_config)
    elif mode == "jeopardy_mode":
        run_jeopardy_mode(game_config)
    elif mode == "endless_mode":
        run_endless_mode(game_config)
    elif mode == "exam_mode":
        run_exam_mode(game_config)
    elif mode == "streak_mode":
        run_streak_mode(game_config)
    elif mode == "survival_mode":
        run_survival_mode(game_config)
    elif mode == "millionaire_mode":
        run_millionaire_mode(game_config)
    else:
        print("THERE WAS AN ERROR SOMEWHEREE!! - RUN_QUIZ()")

    




if __name__ == "__main__":
    print("How smart are you? :D\n")
    run_timed_mode()



"""
#list_of_questions = get_random_questions()
    #list_of_questions = get_quizapi_questions()
    # """