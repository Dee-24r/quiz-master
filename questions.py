import os
import json
import random
import html
import requests
import config
from dotenv import load_dotenv
from utils import build_param_list

load_dotenv()

LOCAL_QUESTIONS_FILE = "data/local_questions.json"
FREE_API_QUESTIONS_FILE = "data/opentdb_questions.json"
AUTH_API_QUESTIONS_FILE = "data/quizapi_questions.json"



def load_questions():
    """LOADS all the questions from the questions.json file
        Returnss a list question dictionaries.
    
    """

    with open(LOCAL_QUESTIONS_FILE, "r") as file:
        questions = json.load(file)
    return questions




def get_random_questions(no_of_questions=3):
    """Returns the specified number of random questions from
    the loaded questions list."""

    questions = load_questions()

    if no_of_questions > len(questions):
        no_of_questions = len(questions)

    return random.sample(questions, no_of_questions)




def get_opentdb_questions(game_config):
    """Questions from Open Trivia DB"""
    c_category, c_type, c_difficulty, c_amount = game_config["category"], game_config["type"], game_config["difficulty"], game_config["amount"]

    params = build_param_list(game_config)

    url = "https://opentdb.com/api.php?"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    
    except requests.exceptions.ConnectionError:
        print("Internet connection error! Please check your internet connection and try again.\n")
        return[] #basically, return empty list of questions

    except requests.exceptions.Timeout:
        print("The API call took more than 10 secs. Please try again after a while.\n")
        return []

    except requests.exceptions.HTTPError:
        print(f"\nThe API server returned a {response.status_code} error")
        return []

    except requests.exceptions.RequestException as e:
        print(f"Something unexpected happened: {e}.")
        return []
    data = response.json()

    questions = data.get("results", [])
    formatted_questions = []    

    for question in questions:
        options = question["incorrect_answers"]
        options.append(question["correct_answer"])
        random.shuffle(options)

        formatted_question = {
            "question_statement": html.unescape(question["question"]),
            "options": [html.unescape(option) for option in options],
            "answer": html.unescape(question["correct_answer"]),
            "category": question["category"],
            "difficulty": question["difficulty"]
        }

        formatted_questions.append(formatted_question)

    return formatted_questions

    """with open(FREE_API_QUESTIONS_FILE, "w") as file:
        json.dump(data, file, indent=4)"""




def get_quizapi_questions():
    """Questions from QuizAPI (authenticated key)"""

    api_key = os.getenv("QUIZ_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}

    url = "https://quizapi.io/api/v1/questions?limit=5"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    
    except requests.exceptions.ConnectionError:
        print("Internet connection error! Please check your internet connection and try again.\n")
        return[] #basically, return empty list of questions

    except requests.exceptions.Timeout:
        print("The API call took more than 10 secs. Please try again after a while.\n")
        return []

    except requests.exceptions.HTTPError:
        print(f"\nThe API server returned a {response.status_code} error")
        return []

    except requests.exceptions.RequestException as e:
        print(f"Something unexpected happened: {e}.")
        return []

    data_r = response.json() #data_response - ran out of names, lol. changed from data cuz data is a json key.

    questions = data_r.get("data", [])
    formatted_questions = []
    for question in questions:

        options = []
        answer = ""
        for option in question.get("answers", []):
            options.append(option["text"])
            if option.get("isCorrect"):
                answer = option["text"]

        formatted_question = {
            "question_statement": html.unescape(question["text"]),
            "options": [html.unescape(option) for option in options],
            "answer": html.unescape(answer),
            "category": question["category"],
            "difficulty": question["difficulty"]
        }

        formatted_questions.append(formatted_question)

    return formatted_questions



if __name__ == "__main__":
    get_quizapi_questions()
    print("Done")


"""
if __name__ == "__main__":
    print("Loading questions...\n")

    questions = load_questions()
    print (f"Loaded {len(questions)} questions. \n")

    print("Random Questions:")
    random_questions = get_random_questions()

    for i, question in enumerate(random_questions):
        print(f"{i+1}. {question['question_statement']}")
"""