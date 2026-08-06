import requests
import json
import config

#VARIABLES AND DATA
game_config = {}
CATEGORIES_DOC = "data/opentdb_categories.json"

GAME_MODES = [
    {"id": 1, "name": "Practice Mode", "name_id": "practice_mode", "description": "Choose a number of questions and test yourself on them."},
    {"id": 2, "name": "Timed Mode", "name_id": "timed_mode", "description": "Be timed to answer questions. Allowed time will be based on the number and complexity of the questions."},
    {"id": 3, "name": "Jeopardy", "name_id": "jeopardy_mode", "description": "Game style! Get points by answering questions correctly, and lose points by answering questions wrongly."},
    {"id": 4, "name": "Endless Mode", "name_id": "endless_mode", "description": "Solve questions until you're tired. Exit by entering 'X'."},
    {"id": 5, "name": "Exam Mode", "name_id": "exam_mode", "description": "Allows the user to revisit questions, like in an exam."}
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

categories = load_opentdb_categories() #dictionary with
# "id" and "name" KVP's




def choose_game_mode():
    """prompts the user to pick a game type - out of 
    the 5 and returns the id so it can be used in 
    other functions"""

    print("Let's goo! Where do you want to start?: ")
    for game in GAME_MODES:
        print(f"{game["id"]}. {game["name"]}")

    game_mode = input(f"Enter a number from 1 to {len(GAME_MODES)}: ")    
    
    while not game_mode.isdigit() or not (1 <= int(game_mode) <= len(GAME_MODES)):
        game_mode = input(f"Enter a valid number from  1 to {len(GAME_MODES)} to pick a mode: ")

    game_mode = int(game_mode)
    return GAME_MODES[game_mode-1]

    #so we want it to return the game mode object abu dict item.

def choose_category():
    """
    prompts the user to choose an available category
    of questions"""
    print("\nWhat would you like to work on today?:\n")
    for i, category in enumerate(categories):
        print(f"{i+1}. {category["name"]}")
    
    user_category = input(f"Input a number between 1 and {len(categories)}: ")
    while not user_category.isdigit() or not (1 <= int(user_category) <= len(categories)):
        user_category = input(f"Please input a valid number between 1 and {len(categories)}: ")

    user_category = int(user_category)
    chosen_category = categories[user_category-1]
    return chosen_category

def choose_questions_type():
    print("\nPick your kind of questions?\n")
    for i, type in enumerate(QUESTION_TYPES):
        print(f"{type["id"]}. {type["name"]}")

    user_type = input("Enter a number between 1 and 3: ")
    while not user_type.isdigit() or not (1 <= int(user_type) <= 3):
        user_type = input(f"Please input a valid number between 1 and 3: ")

    user_type = int(user_type)
    chosen_type = QUESTION_TYPES[user_type-1]
    return chosen_type


def choose_difficulty():
    print("\nHow far can you go?: ")
    for i, level in enumerate(DIFFICULTY):
        print(f"{level["id"]}. {level["name"]}")

    user_difficulty = input("Enter a number between 1 and 3: ")
    while not user_difficulty.isdigit() or not (1 <= int(user_difficulty) <= 3):
        user_difficulty = input(f"Please input a valid number between 1 and 3: ")

    user_difficulty = int(user_difficulty)
    chosen_difficulty = DIFFICULTY[user_difficulty-1]
    return chosen_difficulty



def choose_amount():
    print("\nOkay, how many questions?: ")
    user_amount = input("Enter a number between 1 and 16: ")
    while not user_amount.isdigit() or not (1 <= int(user_amount) <= 16):
        user_amount = input(f"Please input a valid number between 1 and 100: ")

    chosen_amount = user_amount = int(user_amount)
    return chosen_amount





def configure_quiz(mode):
    """Prompts the user to choose category, difficulty, and 
    number of questions"""

    global game_config

    game_config["mode"] = mode
    game_config["category"] = choose_category()
    game_config["type"] = choose_questions_type()
    game_config["difficulty"] = choose_difficulty()

    if mode["name_id"] in ("endless_mode", "jeopardy_mode"):
        game_config["amount"] = 15
    else:
        game_config["amount"] = choose_amount()

    return game_config
    

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
  