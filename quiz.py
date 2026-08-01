#IMPORTS
from questions import get_random_questions, get_opentdb_questions, get_quizapi_questions
from score import calculate_score, record_score
from utils import load_opentdb_categories


#VARIABLES AND DATA
categories = load_opentdb_categories()
DIFFICULTY = ["Easy", "Medium", "Hard"]


def display_question(question):
    """
    Displays the question statement and the options for a given 
    question, one at a time.
    """

    print(question["question_statement"])

    for i, option in enumerate(question["options"]):
        print(f"{i+1}. {option}")



def select_option(question):
    """
    Prompts the user to pick and option for the question and check
    the asnwer"""

    user_answer = input(f"Pick an option (1-{len(question['options'])}): ")

    while not user_answer.isdigit() or not (1 <= int(user_answer) <= len(question["options"])):
        print(f"Invalid input. Please enter a number between 1 and {len(question['options'])}.")
        user_answer = input(f"Pick an option (1-{len(question['options'])}): ")

    if question["options"][int(user_answer) - 1] == question["answer"]:
        print("Correct answer!\n")
        return True
    else:
        print(f"Wrong answer! The correct answer is: {question['answer']}\n")
        return False



def choose_game():
    """Prompts the user to choose category, difficulty, and 
    number of questions"""

    print("What would you like to work on today?:\n")
    for i, category in enumerate(categories):
        print(f"{i+1}. {category["name"]}")

    user_category = input(f"Input a number between 1 and {len(categories)}: ")
    while not (1 <= int(user_category) <= len(categories)):
        user_category = input(f"Please input a valid number between 1 and {len(categories)}: ")

    user_category = int(user_category)
    chosen_category = categories[user_category-1]

    print("How far can you go?: ")
    for i, level in enumerate(DIFFICULTY):
        print(f"{i+1}. {level}")

    user_difficulty = input("Enter a number between 1 and 3: ")
    
    

    params = {id = chosen_category}




def run_quiz():
    list_of_questions = get_random_questions()
    #list_of_questions = get_opentdb_questions()
    #list_of_questions = get_quizapi_questions()
    correct_answers = 0

    for question in list_of_questions:
        display_question(question)

        if select_option(question):
            correct_answers +=1

    score = calculate_score(correct_answers, len(list_of_questions))
    print(f"""You scored {correct_answers} out of {len(list_of_questions)}. 
    Your percentage score is: {score}\n""")
    record_score(score)


if __name__ == "__main__":
    print("How smart are you? :D\n")
    run_quiz()