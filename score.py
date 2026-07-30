import json

SCORES_FILENAME = "data/scores.json"

def calculate_score(correct_answers, total_questions):
    percentage_score = (correct_answers/total_questions) * 100
    return round(percentage_score, 2)

def load_scores():
    """
    Loads scores from scores.json"""
    with open(SCORES_FILENAME, "r") as file:
        scores_history = json.load(file)
    return scores_history

def display_top_5():
    """
    Displays top 5 scores.
    """
    print("Your top 5 scores: \n")

    scores = load_scores()
    top_5 = sorted(scores, reverse=True)[:5]
    for i, score in enumerate(top_5):
        print(f"{i+1}. {score}\n")

def record_score(score):
    scores = load_scores()

    scores.append(score)

    with open(SCORES_FILENAME, "w") as file:
        json.dump(scores, file, indent=4)

if __name__ == "__main__":
    record_score(59)
    print("Doneee")