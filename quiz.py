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
    correct_answers = 0

    for question in list_of_questions:
        display_question(question)

        if select_option(question):
            correct_answers +=1
    handle_and_print_score(correct_answers, len(list_of_questions))




def run_timed_mode(game_config):
    """
    Runs the timed quiz option of the app"""

    list_of_questions = get_opentdb_questions(game_config)
    correct_answers = 0
    questions_answered = 0

    time_limit = 15
    start_time = time.time()
    for question in list_of_questions:
        elapsed_time = time.time() - start_time
        remaining_time = (time_limit - elapsed_time)

        no_of_hours, no_of_minutes, no_of_seconds = format_time_figures(remaining_time)
        print_formatted_time(no_of_hours, no_of_minutes, no_of_seconds)
        questions_answered+=1
        if remaining_time <= 0:
            print("Time's up!")
            print(f"Questions answered {questions_answered}")
            break

        
        display_question(question)

        if select_option(question):
            correct_answers +=1

    handle_and_print_score(correct_answers, len(list_of_questions))


def stop(correct_answers, answered_questions):
    print("Nice Work")
    handle_and_print_score(correct_answers, answered_questions)



def run_endless_mode(game_config):
    """runs the endless option of the app. keep solving quizzzes
    till the user says exit"""

    print("Hmm!! I see you're locked in?")
    print("Get ready! I won't stop until you say so!")
    correct_answers = 0
    answered_questions = 0

    print("Enter 'X' to stop the quiz!")

    while True:
        list_of_questions = get_opentdb_questions(game_config)

        for question in list_of_questions:
            display_question(question)

            result = select_option(question, allow_quit=True)
            if result == "quit":
                stop(correct_answers, answered_questions)
                return
            else:           
                answered_questions+=1
                if result:
                    correct_answers +=1

    

def run_jeopardy_mode(game_config):
    print("sa")


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
    else:
        print("THERE WAS AN ERROR SOMEWHEREE!! - RUN_QUIZ()")



if __name__ == "__main__":
    print("How smart are you? :D\n")
    run_timed_mode()



"""
#list_of_questions = get_random_questions()
    #list_of_questions = get_quizapi_questions()
    # """