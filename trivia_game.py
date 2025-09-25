from os import system, name
import requests
from html import unescape
from random import shuffle
from time import sleep

def get_questions(category=None, difficulty=None, type=None):
    # Code to get the questions from the API
    endpoint = "https://opentdb.com/api.php?amount=10"
    if category:
        endpoint += f"&category={category}"
    if difficulty:
        endpoint += f"&difficulty={difficulty}"
    if type:
        endpoint += f"&type={type}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json() if response.json()["response_code"] == 0 else print("")
    else:
        return response.status_code

def settings_menu():
    # This is where the user can configure the above mentioned parameters. For selecting categories, I will use an API call to list every category and the amount of questions in each category. Every setting (except for amount) will probably lead into a sub-menu where the user can select from the possible choices.

    # Amount of Questions
    #     Parameter: amount
    #     Data type: int
    #     I may remove this if I decide to make the game go on forever
    # Question Categories
    #     Parameter: category
    #     Data type: int
    # Question Difficulty
    #     Parameter: difficulty
    #     Data type: string
    # Type of Question
    #     Parameter: type
    #     Data type: string
    system("cls" if name == "nt" else "clear")
    print("Settings \n")

    while True:
        try: 
            choice = int(input("""
1) Question Categories
2) Question Difficulty
3) Type of Question
                   
Enter the number of the option you want to select: """))
            if (choice < 0 and choice > 3):
                print("Invalid input: Please enter a number between 1 and 3")
            match choice:
                case 1:
                    
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass 
        except ValueError:
            print("Invalid input: Please enter a number between 1 and 3")
    pass

def start_game(category=None, difficulty=None, type=None):
    # Code to start the game
    answers = []
    score = 0
    questions_json = get_questions(category, difficulty, type)
    for question in questions_json["results"]:
        sleep(1)
        system("cls" if name == "nt" else "clear")
        for answer in question["incorrect_answers"]:
            answers.append(unescape(answer))
        answers.append(unescape(question["correct_answer"]))
        shuffle(answers)
        print(f"{unescape(question['question'])}\n")
        for idx, answer in enumerate(answers):
            print(f"{idx + 1}) {answer}")
        user_input = input("Enter the number of the correct answer: ")
        if int(user_input) == answers.index(unescape(question["correct_answer"])) + 1:
            print("Correct!")
            if question["difficulty"] == "easy":
                score += 100
            elif question["difficulty"] == "medium":
                score += 200
            elif question["difficulty"] == "hard":
                score += 300
        else:
            system("cls" if name == "nt" else "clear")
            print(r"""
  ________                        ________                     
 /  _____/_____    _____   ____   \_____  \___  __ ___________ 
/   \  ___\__  \  /     \_/ __ \   /   |   \  \/ // __ \_  __ \
\    \_\  \/ __ \|  Y Y  \  ___/  /    |    \   /\  ___/|  | \/
 \______  (____  /__|_|  /\___  > \_______  /\_/  \___  >__|   
        \/     \/      \/     \/          \/          \/       """)
            print(f"\nYour Score: {score}")
            while True:
                try:
                    continue_game = int(input("""
1) Continue
2) Main Menu
3) Exit

Enter the number of the option you want to select: """))
                    if (continue_game > 0 and continue_game < 4):
                        break
                    else:
                        print("Invalid input: Please enter a number between 1 and 3")
                except ValueError:
                    print("Invalid input: Please enter a number between 1 and 3")
            if continue_game == 1:
                continue
            elif continue_game == 2:
                start_game()
            elif continue_game == 3:
                exit()
        answers.clear()

start_game(category="31", difficulty="easy")