from questions import get_random_questions

def run_quiz():
    random_questions = get_random_questions()
    for question in random_questions:
        display_question(question)
        pick_options(question)

def display_question(question):
    """
    Displays the question statement and the options for a given 
    question, one at a time.
    """

    print(question["question_statement"])

    for i, option in enumerate(question["options"]):
        print(f"{i+1}. {option}")

def pick_options(question):
    """
    Prompts the user to pick and option for the question and check
    the asnwer"""

    user_answer = input(f"Pick an option (1-{len(question['options'])}): ")

    while not user_answer.isdigit() or not (1 <= int(user_answer) <= len(question["options"])):
        print(f"Invalid input. Please enter a number between 1 and {len(question['options'])}.")
        user_answer = input(f"Pick an option (1-{len(question['options'])}): ")

    if question["options"][int(user_answer) - 1] == question["answer"]:
        print("Correct answer!\n")
    else:
        print(f"Wrong answer! The correct answer is: {question['answer']}\n")


if __name__ == "__main__":
    print("How smart are you? :D\n")
    run_quiz()