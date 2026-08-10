import json

SCORES_FILENAME = "data/scores.json"
SCORES_DATA_FILENAME = "data/scores_data.json"
STATS_FILENAME = "data/stats.json"

categ_scores = {}

def load_stats():
    with open(STATS_FILENAME, "r") as file:
        stats = json.load(file)
    return stats

def write_update_stats(categ_scores):
    with open(STATS_FILENAME, "w") as file:
        json.dump(categ_scores, file, indent=4)

    
def update_stats(categ_name, correct_answers, wrong_answers, no_of_questions):
    score_info = {}
    score_info["categ_name"], score_info["correct_answers"], score_info["wrong_answers"], score_info["no_of_questions"], 
    score_info["percentage"] = categ_name, correct_answers, wrong_answers, no_of_questions, (correct_answers/no_of_questions)*100

    categ_scores = load_stats()

    if categ_name not in categ_scores:
        categ_scores[categ_name] = [] #appends a list of dicts
        categ_scores[categ_name].append(score_info)
    else:
        categ_scores[categ_name].append(score_info)

    write_update_stats(categ_scores)


def handle_and_print_score(set_of_questions, game_config, printScore=True):

    correct_answers, wrong_answers, no_of_questions = len(set_of_questions["correctly_answered"]), len(set_of_questions["wrongly_answered"]), set_of_questions["no_of_questions"]

    percentage_score = calculate_score(correct_answers, no_of_questions)

    if printScore:
        print(f"""You scored {correct_answers} out of {no_of_questions}.
        Your percentage score is: {percentage_score}\n""")

    record_score_data(set_of_questions, game_config)
    categ_name = (game_config["category"])["name"]
    update_stats(categ_name, correct_answers, wrong_answers, no_of_questions)


def calculate_score(correct_answers, total_questions):
    if total_questions == 0:
        return 0.0
    percentage_score = (correct_answers/total_questions) * 100
    return round(percentage_score, 2)


def load_scores_data():
    """Loads scores data from scores_data.json"""
    with open(SCORES_DATA_FILENAME, "r") as file:
        scores_data_history = json.load(file)
    return scores_data_history

def record_score_data(set_of_questions, game_config):

    score_data = {}
    score_data["category"] = game_config["category"]
    score_data["amount"] = game_config["amount"]#consider endless mode
    score_data["mode"] = game_config["mode"]

    score_data["wrongly_answered"] = set_of_questions["wrongly_answered"]
    score_data["correctly_answered"] = set_of_questions["correctly_answered"]
    score_data["no_of_questions"] = set_of_questions["no_of_questions"]
    
    scores_data = load_scores_data()
    scores_data.append(score_data)

    with open(SCORES_DATA_FILENAME, "w") as file:
        json.dump(scores_data, file, indent=4)
        
"""
stats = {
    "Math": [ {"categ_name": "sc", "wrongly_asnwered": 32, "correctly_asnwered": 32, "no_ofques": 323 }, {"categ_name": "sc", "wrongly_asnwered": 32, "correctly_asnwered": 32, "no_ofques": 323 },  ]
}
"""

def ret_high_and_low_categs(scores):
    stats = load_stats()
    largest_score = 0
    sorted_stats = []

    for i, item in enumerate(stats):
        percentage_score = item[i]["percentage_score"]
        if percentage_score > largest_score = 


def display_categorical_stats():
    print("ds")

def display_score_based_performance(scores_data):
    num_correct_answers = num_wrong_answers = 0
    for record in scores_data:
        if (record["category"])["id"] == ""
        num_wrong_answers += len(record["wrongly_answered"])
        num_correct_answers += len(record["correctly_answered"])

    no_of_questions = num_correct_answers + num_wrong_answers
    percentage_wrong = (num_wrong_answers/no_of_questions) * 100
    percentage_correct = (num_correct_answers/no_of_questions) * 100

    print(f"Total answereed questions: {no_of_questions}")
    print(f"Wrongly answered questions: {num_wrong_answers}")
    print(f"Correctly answered questions: {num_correct_answers}")

    print(f"You have a percentage of {percentage_correct:.2f} correct answers and a percentage of {percentage_wrong:.2f} wrong answers\n")


def display_stats(stats_type):
    with open(SCORES_DATA_FILENAME, "r") as file:
        scores_data = load_scores_data()

    if stats_type == "categorical_performance":
        display_categorical_performance(scores_data)
    elif stats_type == "score_based_performance":
        display_score_based_performance(scores_data)



"""so, in handle scores, we shud pass a dictionary for
 what category of questions we answered for. and
the questions we got right and wrong, in case we want 
to do practice later on
"""

if __name__ == "__main__":
    display_stats("score_based_performance")
    print("Doneee")



"""
def compute_stats(scores_data):
    categ_scores = {} #dict storing kvp of name of categ and lists of all scores in the categ
    for record in scores_data:
        categ_name = (record["category"])["name"]
        score = compute_score(record) #record's score :(

        if categ_name not in categ_scores:
            categ_scores[categ_name] = []
            categ_scores[categ_name].append(score)
        else:
            categ_scores[categ_name].append(score)

    #shud probably store this, and fins a way to add only new ones, or just store immediately a quiz
"""

"""
def load_scores():
    
    #Loads scores from scores.json
    with open(SCORES_FILENAME, "r") as file:
        scores_history = json.load(file)
    return scores_history
"""

"""
#no longer of useee
def record_score(score, game_config):
    scores = load_scores()

    scores.append(score)

    with open(SCORES_FILENAME, "w") as file:
        json.dump(scores, file, indent=4)
"""



"""
we want to be able to display:
- performance per topic for the top 5 topics, and bottom 3 topics if applicable
- number of questions failed, number of questions passed, 
percentage performance, 

Number of quizzes completed

Average score 

Number of quizzes completed 

Best score 

Worst score
- 
"""

def display_categorical_performance(scores_data):
    print("kmd,,")

#have function that return s the percentage adn numbers
#have function taht matches to the category, when needed
#function that checks the first 5 and last 4

#first compute categs scores

"""
{

{"name": "NAEMME", "scores": [893, 32, 32]},
{"name": "NAEMME", "scores": [893, 32, 32]}

}


def display_top_5():

    Displays top 5 scores.

    print("Your top 5 scores: \n")

    scores = load_scores()
    top_5 = sorted(scores, reverse=True)[:5]
    for i, score in enumerate(top_5):
        print(f"{i+1}. {score}\n")

"""