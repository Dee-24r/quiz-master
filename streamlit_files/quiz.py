#IMPORTS
import time
import streamlit as st

from streamlit_files.questions import get_random_questions, get_opentdb_questions, get_quizapi_questions
from streamlit_files.score import handle_and_print_score
from streamlit_files.utils import configure_quiz, choose_game_mode, format_time_figures

#statrt from length of questions after reload
#rename functions!

def display_question(question):
    """
    Displays the question statement and the options for a given 
    question, one at a time.
    """

    #st.write(question["question_statement"])
    return st.selectbox(f"{question['question_statement']}", 
        options=question["options"],
        key=f"{st.session_state.current_question}"
    )


def select_option(question, allow_quit=False):
    if st.session_state.state_game_config == None:
        return

    if "question_state" not in st.session_state or not st.session_state.question_state:
        st.session_state.question_state = "answering"

    if st.session_state.question_state == "answering":
        st.session_state.answer = display_question(question)
            
        if st.button("Submit", key=f"submit_{st.session_state.current_question}"):
            st.session_state.question_state = "show_answer"
            st.rerun()

    elif st.session_state.question_state == "show_answer":

        if st.session_state.answer == question["answer"]:
            st.write("Correct answer!\n")
            if question not in st.session_state.set_of_questions["correctly_answered"]:
                st.session_state.set_of_questions["correctly_answered"].append(question)
                if (st.session_state.state_game_config["mode"])["name_id"] == "jeopardy_mode":
                    st.session_state.score += st.session_state.added_points
        
        else:
            st.write(f"Wrong answer! The correct answer is: {question['answer']}\n")
            if question not in st.session_state.set_of_questions["correctly_answered"]:
                st.session_state.set_of_questions["wrongly_answered"].append(question)
                if (st.session_state.state_game_config["mode"])["name_id"] == "jeopardy_mode":
                    st.session_state.score += st.session_state.added_points
    

        if st.session_state.current_question < len(st.session_state.questions) - 1:
            if st.button("Next Question", key=f"question_{st.session_state.current_question}"):
                st.session_state.current_question += 1
                st.session_state.question_state = "answering"
                st.session_state.answer = None
                st.rerun()

        else:
            if st.button("Finish Quiz"):
                st.session_state.current_question += 1
                st.session_state.question_state = "answering"
                st.session_state.answer = None
                handle_and_print_score(st.session_state.set_of_questions, st.session_state.state_game_config)
                return


def run_practice_mode(game_config):
    if st.session_state.state_game_config == None:
        return

    if "questions" not in st.session_state or len(st.session_state.questions) == 0:
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

    if st.session_state.current_question < len(st.session_state.questions):
        question = st.session_state.questions[st.session_state.current_question]
        select_option(question)



@st.fragment(run_every=0.5)
def run_timer(time_limit):
    """runs the timer"""
    if st.session_state.ret:
        return
    
    if not "time_limit" in st.session_state or (st.session_state.time_limit == None):
        st.session_state.time_limit = time_limit

    if not "start_time" in st.session_state or (st.session_state.start_time == None):
        st.session_state.start_time = time.time()
        st.session_state.time_up = False

    timer_display = st.empty()

    st.session_state.elapsed_time = time.time() - st.session_state.start_time
    st.session_state.remaining_time = max(0, st.session_state.time_limit - st.session_state.elapsed_time)
    
    st.session_state.hrs, st.session_state.mins, st.session_state.secs = format_time_figures(st.session_state.remaining_time)
    timer_display.text(f"Time remaining: {st.session_state.hrs:02d} : {st.session_state.mins:02d} : {st.session_state.secs:02d}")

    if st.session_state.remaining_time <= 0:
        st.session_state.time_up = True
        handle_and_print_score(st.session_state.set_of_questions, st.session_state.state_game_config)
        return
    
    return st.session_state.time_up
    
    

#NEED to fins a better way to do time - no longer a  terminal.
def run_timed_mode(game_config):
    """Runs the timed quiz option of the app"""

    if "questions" not in st.session_state or len(st.session_state.questions) == 0:
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

    allowed_time = len(st.session_state.questions)*5
    run_timer(allowed_time)

    if st.session_state.current_question < len(st.session_state.questions) or not st.session_state.time_up:
        question = st.session_state.questions[st.session_state.current_question]
        select_option(question)

    if st.session_state.current_question >= len(st.session_state.questions):
        no_of_answered_questions = len(st.session_state.set_of_questions["wrongly_answered"]) + len(st.session_state.set_of_questions["correctly_answered"])
        st.write(f"Questions answered: {no_of_answered_questions}")

        st.session_state.ret = True
        st.session_state.time_limit = None
        st.session_state.start_time = None
        return


def jeopardy_board():
    points = [100, 200, 300, 400, 500]

    for row, no_of_points in enumerate(points):
        cols = st.columns(4)

        for col in cols:
            with col:
                if st.button(str(no_of_points), key=f"ques_{row}_{col}"):
                    st.session_state.added_points = no_of_points
                    st.rerun()


def run_jeopardy_mode(game_config):
    if "questions" not in st.session_state or len(st.session_state.questions) == 0:
        st.session_state.state_game_config = game_config
        st.session_state.questions = []

        for diffic_level in st.session_state.difficulty_levels:
            st.session_state.state_game_config["difficulty"] = diffic_level
            questions_by_diff = get_opentdb_questions(st.session_state.state_game_config)
            for question in questions_by_diff:
                st.session_state.questions.append(question)
            time.sleep(1)


        #st.session_state.questions = get_opentdb_questions(game_config)
        # st.session_state.level_questions = {}
        # st.session_state.questions = []

        #     st.session_state.level_questions[f"{diffic_level}"] = get_opentdb_questions(st.session_state.state_game_config)
        #     for question in st.session_state.level_questions[f"{diffic_level}"]:
        #         st.session_state.questions.append(question)

        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answer = None
        st.session_state.question_state = "answering"

        st.session_state.set_of_questions = {
            "no_of_questions": len(st.session_state.questions),
            "wrongly_answered": [],
            "correctly_answered": []
        }
        st.rerun()

    if st.session_state.current_question < len(st.session_state.questions):
        jeopardy_board()
        question = st.session_state.questions[st.session_state.current_question]
        select_option(question)

    st.write(f"Score: {st.session_state.score}")



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
    st.session_state.ret = False
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