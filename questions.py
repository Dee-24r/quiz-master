import json
import random

QUESTIONS_FILE = "data/questions.json"

def load_questions():
    """LOADS all the questions from the questions.json file
        Returnss a list question dictionaries.
    
    """

    with open(QUESTIONS_FILE, "r") as file:
        questions = json.load(file)
    return questions

def get_random_questions(no_of_questions=3):
    """Retruns the specified number of random questions from
    the loaded questions list."""

    questions = load_questions()

    if no_of_questions > len(questions):
        no_of_questions = len(questions)

    return random.sample(questions, no_of_questions)

if __name__ == "__main__":
    print("Loading questions...\n")

    questions = load_questions()
    print (f"Loaded {len(questions)} questions. \n")

    print("Random Questions:")
    random_questions = get_random_questions()

    for i, question in enumerate(random_questions):
        print(f"{i+1}. {question['question_statement']}")