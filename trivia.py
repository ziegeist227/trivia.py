import os
import requests
import json
from html import unescape
from random import shuffle
from time import sleep


def get_questions(category=None, difficulty=None, token=None):
    # Code to get the questions from the API
    category_question_count = 50
    if category:
        endpoint = f"https://opentdb.com/api_count.php?category={category}"
        while True:
            response = requests.get(endpoint)
            if response.status_code == 200:
                category_question_count = response.json()["category_question_count"]
                if difficulty == "easy":
                    category_question_count = category_question_count[
                        "total_easy_question_count"
                    ]
                elif difficulty == "medium":
                    category_question_count = category_question_count[
                        "total_medium_question_count"
                    ]
                elif difficulty == "hard":
                    category_question_count = category_question_count[
                        "total_hard_question_count"
                    ]
                elif not difficulty:
                    category_question_count = category_question_count[
                        "total_question_count"
                    ]
                break
            elif response.status_code == 429:
                sleep(5)
                continue
            return response.status_code
    category_question_count = min(category_question_count, 50)
    endpoint = f"https://opentdb.com/api.php?amount={category_question_count}"
    if category:
        endpoint += f"&category={category}"
    if difficulty:
        endpoint += f"&difficulty={difficulty}"
    if token:
        endpoint += f"&token={token}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        response_code = response.json()["response_code"]
        if response_code == 0:
            return response.json()
        elif response_code == 5:
            sleep(5)
            return get_questions(category, difficulty, type)
        else:
            return response_code
    elif response.status_code == 429:
        sleep(5)
        return get_questions(category, difficulty, type)
    return response.status_code


def get_categories():
    endpoint = "https://opentdb.com/api_category.php"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()["trivia_categories"]
    elif response.status_code == 429:
        sleep(5)
        return get_categories()
    return response.status_code


def get_settings():
    if not os.path.exists("settings.json"):
        try:
            with open("settings.json", "w") as f:
                json.dump(
                    {"category": None, "difficulty": None},
                    f,
                    indent=2,
                )
        except IOError:
            print("Error: Unable to write to settings.json")
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except IOError:
        print("Error: Unable to read settings.json")


def main_menu():
    settings = get_settings()
    os.system("cls" if os.name == "nt" else "clear")
    print(r"""
   /$$               /$$            /$$                                  
  | $$              |__/           |__/                                  
 /$$$$$$    /$$$$$$  /$$ /$$    /$$ /$$  /$$$$$$       /$$$$$$  /$$   /$$
|_  $$_/   /$$__  $$| $$|  $$  /$$/| $$ |____  $$     /$$__  $$| $$  | $$
  | $$    | $$  \__/| $$ \  $$/$$/ | $$  /$$$$$$$    | $$  \ $$| $$  | $$
  | $$ /$$| $$      | $$  \  $$$/  | $$ /$$__  $$    | $$  | $$| $$  | $$
  |  $$$$/| $$      | $$   \  $/   | $$|  $$$$$$$ /$$| $$$$$$$/|  $$$$$$$
   \___/  |__/      |__/    \_/    |__/ \_______/|__/| $$____/  \____  $$
                                                     | $$       /$$  | $$
                                                     | $$      |  $$$$$$/
                                                     |__/       \______/ """)
    print("1) Play")
    print("2) Settings")
    print("3) Exit")
    while True:
        try:
            choice = int(input("\nSelect an option: "))
            if choice < 1 or choice > 3:
                print("Invalid input: Please enter a number between 1 and 3")
                continue
            break
        except ValueError:
            print("Invalid input: Please enter a number")
    match choice:
        case 1:
            start_game(category=settings["category"], difficulty=settings["difficulty"])
        case 2:
            settings_menu()
        case 3:
            exit()


def settings_menu():
    settings = get_settings()
    categories = get_categories()
    difficulties = {3: "easy", 4: "medium", 5: "hard"}
    category = settings["category"] if settings["category"] else None
    difficulty = settings["difficulty"] if settings["difficulty"] else None
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(r"""
                       /$$     /$$     /$$                              
                      | $$    | $$    |__/                              
  /$$$$$$$  /$$$$$$  /$$$$$$ /$$$$$$   /$$ /$$$$$$$   /$$$$$$   /$$$$$$$
 /$$_____/ /$$__  $$|_  $$_/|_  $$_/  | $$| $$__  $$ /$$__  $$ /$$_____/
|  $$$$$$ | $$$$$$$$  | $$    | $$    | $$| $$  \ $$| $$  \ $$|  $$$$$$ 
 \____  $$| $$_____/  | $$ /$$| $$ /$$| $$| $$  | $$| $$  | $$ \____  $$
 /$$$$$$$/|  $$$$$$$  |  $$$$/|  $$$$/| $$| $$  | $$|  $$$$$$$ /$$$$$$$/
|_______/  \_______/   \___/   \___/  |__/|__/  |__/ \____  $$|_______/ 
                                                     /$$  \ $$          
                                                    |  $$$$$$/          
                                                     \______/           """)
        print(
            "Current Question Category: "
            + (
                categories[category - 9]["name"]
                if category is not None
                else "All Categories"
            )
        )
        print(
            "Current Question Difficulty: "
            + (difficulty.capitalize() if difficulty is not None else "Any Difficulty")
        )

        try:
            choice = int(
                input("""
1) Question Categories
2) Question Difficulty
3) Back to Main Menu
                      
Select the setting you wish to change: """)
            )
            if choice < 1 and choice > 3:
                print("Invalid input: Please enter a number between 1 and 3")
            match choice:
                case 1:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("1) Back")
                    print("2) All Categories")
                    for idx, category in enumerate(categories):
                        print(f"{idx + 3}) {category['name']}")
                    while True:
                        try:
                            choice = int(
                                input(
                                    "\nSelect the category of questions you wish to answer: "
                                )
                            )
                            if choice < 1 or choice > len(categories) + 2:
                                print(
                                    "Invalid input: Please enter a number between 1 and "
                                    + str(len(categories) + 2)
                                )
                                continue
                            elif choice == 2:
                                category = None
                            elif choice == 1:
                                settings_menu()
                            else:
                                category = choice + 6
                            break
                        except ValueError:
                            print("Invalid input: Please enter a number")
                    try:
                        with open("settings.json", "w") as f:
                            json.dump(
                                {"category": category, "difficulty": difficulty},
                                f,
                                indent=2,
                            )
                    except IOError:
                        print("Error: Unable to write to settings.json")
                case 2:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("1) Back")
                    print("2) Any Difficulty")
                    print("3) Easy")
                    print("4) Medium")
                    print("5) Hard")
                    while True:
                        try:
                            choice = int(
                                input(
                                    "\nSelect the difficulty of questions you wish to answer: "
                                )
                            )
                            if choice < 1 or choice > 5:
                                print(
                                    "Invalid input: Please enter a number between 1 and 5"
                                )
                                continue
                            elif choice == 2:
                                difficulty = None
                            elif choice == 1:
                                settings_menu()
                            else:
                                difficulty = difficulties[choice]
                            break
                        except ValueError:
                            print("Invalid input: Please enter a number")
                    try:
                        with open("settings.json", "w") as f:
                            json.dump(
                                {"category": category, "difficulty": difficulty},
                                f,
                                indent=2,
                            )
                    except IOError:
                        print("Error: Unable to write to settings.json")
                case 3:
                    main_menu()
        except ValueError:
            print("Invalid input: Please enter a number between 1 and 3")


def start_game(category=None, difficulty=None):
    # Code to start the game
    token = requests.get("https://opentdb.com/api_token.php?command=request")
    if token.status_code == 200:
        if token.json()["response_code"] == 0:
            token = token.json()["token"]
        else:
            return (
                f"Error getting token\n Response Code: {token.json()['response_code']}"
            )
    else:
        return token
    answers = []
    score = 0
    while True:
        questions_json = get_questions(category, difficulty, token)
        if questions_json == 1:
            print("Not enough questions in category, expanding to all categories...")
            questions_json = get_questions(
                difficulty=difficulty, type=type, token=token
            )
            if questions_json == 1:
                print(
                    "How... How did you answer ALL of the questions? That's simply impossible. You must be cheating. Thats the only way. You HAD to have cheated. Do it again."
                )
                start_game(category=category, difficulty=difficulty, type=type)

        for question in questions_json["results"]:
            sleep(1)
            os.system("cls" if os.name == "nt" else "clear")
            for answer in question["incorrect_answers"]:
                answers.append(unescape(answer))
            answers.append(unescape(question["correct_answer"]))
            shuffle(answers)
            print(f"{unescape(question['question'])}\n")
            for idx, answer in enumerate(answers):
                print(f"{idx + 1}) {answer}")
            user_input = input("Enter the number of the correct answer: ")
            if (
                int(user_input)
                == answers.index(unescape(question["correct_answer"])) + 1
            ):
                os.system("cls" if os.name == "nt" else "clear")
                print(r"""
                                                               /$$    /$$
                                                              | $$   | $$
  /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$ /$$$$$$ | $$
 /$$_____/ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$_____/|_  $$_/ | $$
| $$      | $$  \ $$| $$  \__/| $$  \__/| $$$$$$$$| $$        | $$   |__/
| $$      | $$  | $$| $$      | $$      | $$_____/| $$        | $$ /$$   
|  $$$$$$$|  $$$$$$/| $$      | $$      |  $$$$$$$|  $$$$$$$  |  $$$$//$$
 \_______/ \______/ |__/      |__/       \_______/ \_______/   \___/ |__/""")
                if question["difficulty"] == "easy":
                    score += 100
                elif question["difficulty"] == "medium":
                    score += 200
                elif question["difficulty"] == "hard":
                    score += 300
            else:
                os.system("cls" if os.name == "nt" else "clear")
                print(r"""
                                                                                          
                                                                                          
  /$$$$$$   /$$$$$$  /$$$$$$/$$$$   /$$$$$$         /$$$$$$  /$$    /$$ /$$$$$$   /$$$$$$ 
 /$$__  $$ |____  $$| $$_  $$_  $$ /$$__  $$       /$$__  $$|  $$  /$$//$$__  $$ /$$__  $$
| $$  \ $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$      | $$  \ $$ \  $$/$$/| $$$$$$$$| $$  \__/
| $$  | $$ /$$__  $$| $$ | $$ | $$| $$_____/      | $$  | $$  \  $$$/ | $$_____/| $$      
|  $$$$$$$|  $$$$$$$| $$ | $$ | $$|  $$$$$$$      |  $$$$$$/   \  $/  |  $$$$$$$| $$      
 \____  $$ \_______/|__/ |__/ |__/ \_______/       \______/     \_/    \_______/|__/      
 /$$  \ $$                                                                                
|  $$$$$$/                                                                                
 \______/                                                                                 """)
                print(f"\nYour Score: {score}")
                while True:
                    try:
                        continue_game = int(
                            input("""
1) Continue
2) Main Menu
3) Exit

Enter the number of the option you want to select: """)
                        )
                        if continue_game > 0 and continue_game < 4:
                            break
                        else:
                            print(
                                "Invalid input: Please enter a number between 1 and 3"
                            )
                    except ValueError:
                        print("Invalid input: Please enter a number between 1 and 3")
                if continue_game == 1:
                    pass
                elif continue_game == 2:
                    main_menu()
                elif continue_game == 3:
                    exit()
                score = 0
            answers.clear()
        os.system("cls" if os.name == "nt" else "clear")
        print("Grabbing more questions...")


if __name__ == "__main__":
    main_menu()
