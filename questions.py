import json
import random
import html
import requests

QUESTIONS_FILE = "data/questions.json"
API_QUESTIONS_FILE = "data/opentdb_questions.json"



def load_questions():
    """LOADS all the questions from the questions.json file
        Returnss a list question dictionaries.
    
    """

    with open(QUESTIONS_FILE, "r") as file:
        questions = json.load(file)
    return questions




def get_random_questions(no_of_questions=3):
    """Returns the specified number of random questions from
    the loaded questions list."""

    questions = load_questions()

    if no_of_questions > len(questions):
        no_of_questions = len(questions)

    return random.sample(questions, no_of_questions)



def get_opentdb_questions():
    """Questions from Open Trivia DB"""

    url = "https://opentdb.com/api.php?amount=5"
    response = requests.get(url)
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

    """with open(API_QUESTIONS_FILE, "w") as file:
        json.dump(questions, file, indent=4)"""



if __name__ == "__main__":
    get_opentdb_questions()
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