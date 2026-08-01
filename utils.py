import requests
import json
CATEGORIES_DOC = "data/opentdb_categories.json"

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

if __name__ == "__main__":
    save_opentdb_categories()