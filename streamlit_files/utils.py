import requests
import json
import streamlit as st

#VARIABLES AND DATA
game_config = {}
CATEGORIES_DOC = "data/opentdb_categories.json"

GAME_MODES = [
    {"id": 1, "name": "Practice Mode", "name_id": "practice_mode", "description": "Choose a number of questions and test yourself on them."},
    {"id": 2, "name": "Timed Mode", "name_id": "timed_mode", "description": "Be timed to answer questions. Allowed time will be based on the number and complexity of the questions."},
    {"id": 3, "name": "Jeopardy", "name_id": "jeopardy_mode", "description": "Game style! Get points by answering questions correctly, and lose points by answering questions wrongly."},
    {"id": 4, "name": "Endless Mode", "name_id": "endless_mode", "description": "Solve questions until you're tired. Exit by entering 'X'."},
    {"id": 5, "name": "Exam Mode", "name_id": "exam_mode", "description": "Allows the user to revisit questions, like in an exam."},
    {"id": 6, "name": "Streak Mode", "name_id": "streak_mode", "description": "Just like Endless Mode, but you keep correct streaks which reset if you get an answer wrong"},
    {"id": 7, "name": "Survival", "name_id": "survival_mode", "description": "Have a set of questions and only 3 chances to fail questions."},
    {"id": 8, "name": "Who wants to be a Millionaire", "name_id": "millionaire_mode", "description": "Points keep adding up, and if you loose, the game ends."}
    #tbh might or not implement this
]

DIFFICULTY = [
    {"id": 1, "name":"Easy", "name_id": "easy"}, 
    {"id": 2, "name": "Medium", "name_id": "medium"}, 
    {"id": 3, "name": "Hard", "name_id": "hard"}
]

QUESTION_TYPES = [
    {"id": 1, "name": "Multiple Choice", "name_id": "multiple"}, 
    {"id": 2, "name": "True/False", "name_id": "boolean"},
    {"id": 3, "name": "Mixed", "name_id": "mixed"}   
]


def save_opentdb_categories():
    """
    Get the list of categories from opentdb"""

    url = "https://opentdb.com/api_category.php"
    response = requests.get(url)
    data = response.json()

    with open(CATEGORIES_DOC, "w") as file:
        json.dump(data, file, indent=4)


def load_opentdb_categories():
    with open(CATEGORIES_DOC, "r") as file:
        categories = json.load(file)

    return categories["trivia_categories"]

#------------------categoriessss!!------
categories = load_opentdb_categories() #dictionary with
# "id" and "name" KVP's




def choose_game_mode():
    """prompts the user to pick a game type - out of 
    the 5 and returns the id so it can be used in 
    other functions"""

    #st.subheader("Let's goo! Where do you want to start?: ")
    return st.selectbox("Pick a mode", 
                 options=GAME_MODES,
                 format_func= lambda x: x["name_id"]
                 )

def choose_category():
    """
    prompts the user to choose an available category
    of questions"""

    #st.subheader("\nWhat would you like to work on today?:\n")
    return st.selectbox("Choose a category", 
        options=categories,
        format_func= lambda x: x["name"]
        )

def choose_questions_type():
    #st.subheader("\nWhat kind of questions do you want?\n")
    
    return st.selectbox("Choose a question type", 
        options=QUESTION_TYPES,
        format_func= lambda x: x["name_id"]
    )

    
def choose_difficulty():
    #st.subheader("\nHow far can you go?: ")
    difficulty = st.slider("Pick a difficulty level", min_value=1, max_value=3, step=1)

    return DIFFICULTY[difficulty-1]

def choose_amount():
    #st.subheader("\nOkay, how many questions?: ")
    return st.number_input("How many questions?", 1, 16)




def configure_quiz():
    """Prompts the user to choose category, difficulty, and 
    number of questions"""

    mode = st.session_state.state_game_config["mode"] = choose_game_mode()
    st.session_state.state_game_config["category"] = choose_category()
    st.session_state.state_game_config["type"] = choose_questions_type()
    st.session_state.state_game_config["difficulty"] = choose_difficulty()
    if mode["name_id"] in ("endless_mode", "jeopardy_mode"):
            st.session_state.state_game_config["amount"] = 15
    else:
        st.session_state.state_game_config["amount"] = choose_amount()
    
    if st.button("Start Quiz"):
        st.session_state.current_page = "run_selected_quiz"
    

#pass in game_config. then we'll do game_config["id"]
#c_ for chosen
def build_param_list(game_config):
    """
    Build's parameters for the API call. variables received from 
    configure_quiz
    """

    c_category, c_type, c_difficulty, c_amount = game_config["category"], game_config["type"], game_config["difficulty"], game_config["amount"]

    params = {}

    params["difficulty"] = c_difficulty["name_id"]
    params["category"] = c_category["id"]
    params["amount"] = c_amount

    if c_type["name_id"]!= "mixed":
            params["type"] = c_type["name_id"]

    return params
        


def format_time_figures(no_of_seconds):

    no_of_seconds = max(0, no_of_seconds)
    no_of_minutes, no_of_seconds = divmod(no_of_seconds, 60)
    no_of_hours, no_of_minutes = divmod(no_of_minutes, 60)
    return int(no_of_hours), int(no_of_minutes), int(no_of_seconds)


def print_formatted_time(no_of_hours, no_of_minutes, no_of_seconds):
    print(f"{no_of_hours:02d} : {no_of_minutes:02d} : {no_of_seconds:02d}")



if __name__ == "__main__":
    save_opentdb_categories()
  