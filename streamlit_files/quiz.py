#IMPORTS
import time
import streamlit as st
from streamlit_files.questions import get_random_questions, get_opentdb_questions, get_quizapi_questions
from streamlit_files.score import handle_and_print_score
from streamlit_files.utils import configure_quiz, choose_game_mode, format_time_figures, print_formatted_time

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

    #st.write(question["question_statement"])
    return st.selectbox(f"{question["question_statement"]}", 
        options=question["options"],
        key=f"{st.session_state.current_question}"
    )

    #for i, option in enumerate(question["options"]):
     #   print(f"{i+1}. {option}")


def select_option(question, allow_quit=False):
    if "question_state" not in st.session_state: #or st.session_state.question_state == "next_question":
        st.session_state.question_state = "answering"

    #question = st.session_state.set_of_questions[st.session_state.current_question] #continue from here tmr

    if st.session_state.question_state == "answering":
        st.session_state.answer = display_question(question)
            
        if st.button("Submit", key=f"submit_{st.session_state.current_question}"):
            st.session_state.question_state = "show_answer"

    if st.session_state.question_state == "show_answer":

        if st.session_state.answer == question["answer"]:
            st.write("Correct answer!\n")
            (st.session_state.set_of_questions["correctly_answered"]).append(question)
        
        elif st.session_state.answer != question["answer"]:
            st.write(f"Wrong answer! The correct answer is: {question['answer']}\n")
            st.session_state.set_of_questions["wrongly_answered"].append(question)
        
        else:
            st.write("Error from answering...")

        if st.button("Next Question", key=f"question_{st.session_state.current_question}"):
            st.session_state.current_question += 1
            st.session_state.question_state = "answering"
            st.session_state.answer = None
            st.rerun()
        

    """
    #Prompts the user to pick and option for the question and check
    #the asnwer
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
    """


def run_practice_mode(game_config):
    if "questions" not in st.session_state:
        st.session_state.questions = get_opentdb_questions(game_config)
        st.session_state.current_question = 0
        st.session_state.answer = None

        st.session_state.question_state = "answering"
        st.session_state.set_of_questions = {
            "no_of_questions": len(st.session_state.questions),
            "wrongly_answered": [],
            "correctly_answered": []
        }
        st.rerun()

    if st.session_state.current_question >= len(st.session_state.questions):
        handle_and_print_score(st.session_state.set_of_questions, game_config)
        st.session_state.question_state = None
        st.session_state.current_page = "home"
        st.rerun()
        return

    question = st.session_state.questions[st.session_state.current_question]
    select_option(question)



def run_timed_mode(game_config):
    """
    Runs the timed quiz option of the app"""

    st.session_state.questions = get_opentdb_questions(game_config)
    if "questions" not in st.session_state:
        st.session_state.set_of_questions = {}

    st.session_state.set_of_questions["no_of_questions"] = len(st.session_state.questions)
    st.session_state.set_of_questions["wrongly_answered"] = []
    st.session_state.set_of_questions["correctly_answered"] = []

    time_limit = 15
    start_time = time.time()

    for question in st.session_state.questions:
        elapsed_time = time.time() - start_time
        remaining_time = (time_limit - elapsed_time)

        no_of_hours, no_of_minutes, no_of_seconds = format_time_figures(remaining_time)
        print_formatted_time(no_of_hours, no_of_minutes, no_of_seconds)

        if remaining_time <= 0:
            print("Time's up!")
            no_of_answered_questions = len(st.session_state.set_of_questions["wrongly_answered"]) + len(st.session_state.set_of_questions["correctly_answered"])
            print(f"Questions answered {no_of_answered_questions}")
            break

        
        display_question(question)
        result = select_option(question)
        if result:
            st.session_state.set_of_questions["correctly_answered"].append(question)
        elif not result:
            st.session_state.set_of_questions["wrongly_answered"].append(question)

    handle_and_print_score(st.session_state.set_of_questions, game_config)
    st.session_state.current_page = "home"




def run_jeopardy_mode(game_config):
    st.session_state.questions = get_opentdb_questions(game_config)
    score = 0
    if "questions" not in st.session_state:
        st.session_state.set_of_questions = {}
    st.session_state.set_of_questions["no_of_questions"] = len(st.session_state.questions)
    st.session_state.set_of_questions["wrongly_answered"] = []
    st.session_state.set_of_questions["correctly_answered"] = []
    
    for question in st.session_state.questions:
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
            (st.session_state.set_of_questions["wrongly_answered"]).append(question)
        elif result:
            score + score_addition
            (st.session_state.set_of_questions["correctly_answered"]).append(question)

    handle_and_print_score(st.session_state.set_of_questions, game_config)
    print(f"Score: {score}")
    st.session_state.current_page = "home"




def run_endless_mode(game_config):
    """runs the endless option of the app. keep solving quizzzes
    till the user says exit"""

    print("Hmm!! I see you're locked in?")
    print("Get ready! I won't stop until you say so!")
    if "questions" not in st.session_state:
        st.session_state.set_of_questions = {}
    st.session_state.set_of_questions["no_of_questions"] = 0
    st.session_state.set_of_questions["wrongly_answered"] = []
    st.session_state.set_of_questions["correctly_answered"] = []

    print("Enter 'X' to stop the quiz!")

    while True:
        st.session_state.questions = get_opentdb_questions(game_config)
        for question in st.session_state.questions:
            display_question(question)
            
            result = select_option(question, allow_quit=True)
            if result == "quit":
                print("Nice Work")
                handle_and_print_score(st.session_state.set_of_questions, game_config)
                st.session_state.current_game = "home"
                return
            
            else:
                st.session_state.set_of_questions["no_of_questions"] += 1
                if result:
                    (st.session_state.set_of_questions["correctly_answered"]).append(question)
                elif not result:
                    (st.session_state.set_of_questions["wrongly_answered"]).append(question)



def run_exam_mode(game_config):
    print("Not yet implemented")
    st.session_state.current_page = "home"
    

def run_survival_mode(game_config):
    st.session_state.questions = get_opentdb_questions(game_config)
    if "questions" not in st.session_state:
        st.session_state.set_of_questions = {}
    st.session_state.set_of_questions["no_of_questions"] = len(st.session_state.questions)
    st.session_state.set_of_questions["wrongly_answered"] = []
    st.session_state.set_of_questions["correctly_answered"] = []

    lives, score = 3, 0
    for question in st.session_state.questions:
        print(f"You have {lives} lives remaining!")
        display_question(question)
        result = select_option(question)

        if not result:
            st.session_state.set_of_questions["wrongly_answered"].append(question)
            lives-=1
            if lives <= 0:
                print("Game Over!")
                return
        else:
            st.session_state.set_of_questions["correctly_answered"].append(question)
            score + 100

    handle_and_print_score(st.session_state.set_of_questions, game_config)
    st.session_state.current_page = "home"


def run_streak_mode(game_config):
    st.session_state.questions = get_opentdb_questions(game_config)

    if "questions" not in st.session_state:
        st.session_state.set_of_questions = {}
    st.session_state.set_of_questions["no_of_questions"] = len(st.session_state.questions)
    st.session_state.set_of_questions["wrongly_answered"] = []
    st.session_state.set_of_questions["correctly_answered"] = []
    
    longest_streak = current_streak = 0
    for question in st.session_state.questions:
        print(f"Longest streak {longest_streak}")
        print(f"Current streak: {current_streak} ")
        display_question(question)

        result = select_option(question)
        
        if not result:
            st.session_state.set_of_questions["wrongly_answered"].append(question)
            current_streak = 0
        else:
            st.session_state.set_of_questions["correctly_answered"].append(question)
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak

    handle_and_print_score(st.session_state.set_of_questions, game_config)
    st.session_state.current_page = "home"


def run_millionaire_mode(game_config):
    print("Not yet implemented!")
    


def run_quiz():
    game_config = st.session_state.state_game_config

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
    #st.session_state.set_of_questions = None






if __name__ == "__main__":
    print("How smart are you? :D\n")
    run_timed_mode()



"""
#st.session_state.questions = get_random_questions()
    #st.session_state.questions = get_quizapi_questions()
    # """