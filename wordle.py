import random
import string
import readline

from good_guesser import good_guesser


with open("words.txt", "r") as f:
    wordles = tuple(line.strip() for line in f)

NUM_CHANCES = 6

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
dim = "\033[2m"
reset = "\033[0m"


colors = {
    "wrong": dim,
    "misplaced": yellow,
    "right": green,
    "nothing": reset,
}

codes = {
    colors["wrong"]: "0",
    colors["misplaced"]: "1",
    colors["right"]: "2",
}

word = None
status = None

LINE_NUMBER = None
guesses = []

def reset_vars():
    global word, status, LINE_NUMBER, guesses
    guesses = []
    word = random.choice(wordles)
    status = {c: "nothing" for c in string.ascii_lowercase}
    LINE_NUMBER = 5

reset_vars()

def print_status():
    print("[ ", end="")
    for c in string.ascii_lowercase:
        print(colors[status[c]] + c + reset, end="")
    print(reset + " ]", end="")


def move_up(n: int = 1):
    print(f"\033[{n}A", end="")


def move_down(n: int = 1):
    print(f"\033[{n}B", end="")


def move_leftest():
    print("\r", end="")


# def move_right(n: int = 1):
#     print(f"\033[{n}C", end="")


def update_guess(guess, guess_raw):
    cnt = {}
    for c in word:
        if c not in cnt:
            cnt[c] = 0
        cnt[c] += 1
    paint = [colors["wrong"]] * 5
    for i, c in enumerate(guess):
        if c == word[i]:
            paint[i] = colors["right"]
            cnt[c] -= 1
    for i, c in enumerate(guess):
        if paint[i] != colors["right"] and c in cnt and cnt[c] > 0:
            paint[i] = colors["misplaced"]
            cnt[c] -= 1
        print(paint[i] + guess_raw[i] + reset, end="")
    guesses.append((guess, "".join(codes[col] for col in paint)));


def check_alphabet(word: str):
    for c in word:
        if c not in string.ascii_lowercase:
            return False
    return True


def print_error(guess_raw: str, msg: str):
    print(dim + red + guess_raw + reset + dim + " - " + msg + reset)

def print_start_guessing(guess_remaining):
    print(f"Start Guessing.. ({guess_remaining} left)", end="")

def change_title(word : str):
    move_up(LINE_NUMBER)
    move_leftest()
    print(blue + f"{word.title()} " + reset, end="")
    move_down(LINE_NUMBER)
    move_leftest()

def start():
    global word, status, LINE_NUMBER

    print("\033[H\033[J" + blue + f"Wordle\n" + reset)

    print_status()
    print("\n")

    chance = 0

    print_start_guessing(NUM_CHANCES-chance)
    print()

    correct_guessed = False

    for chance in range(NUM_CHANCES):
        while True:
            # guess not in words list
            guess_raw = input()
            guess = guess_raw.lower()
            LINE_NUMBER += 1

            if guess == "guwahati":
                change_title(word)
            elif guess == "pune":
                change_title(good_guesser(guesses))

            if not check_alphabet(guess):
                move_up()
                print_error(guess_raw, "Word should only contain alphabets")
            elif len(guess) != 5:
                move_up()
                print_error(guess_raw, "Word should be 5-lettered")
            elif guess not in wordles:
                move_up()
                print_error(guess_raw, "Word not in dictionary")
            else:
                break

        if guess.lower() == word:
            print(colors["right"] + "\nCorrect Guess!!" + reset)
            correct_guessed = True
            break

        for i, ch in enumerate(guess):
            if ch == word[i]:
                status[ch] = "right"
            elif ch in word:
                if status[ch] != "right":
                    status[ch] = "misplaced"
            else:
                status[ch] = "wrong"
        lines_to_move = LINE_NUMBER - 2
        move_up(lines_to_move)
        print_status()
        move_leftest()
        move_down(2)
        print_start_guessing(NUM_CHANCES-chance-1)
        move_down(lines_to_move - 3)
        move_leftest()
        update_guess(guess, guess_raw)
        move_down()
        move_leftest()

    if not correct_guessed:
        print("\nCorrect word was " + green + word.upper() + reset)

    if input("\nPlay again (y/N)? ").lower() == "y":
        reset_vars()
        start()

start()
