"""CodeAlpha Task 1 — Hangman Game.

Classic word-guessing game with a limited number of wrong guesses.
Run:  python hangman.py
"""
import random

WORD_LIST = [
    "python", "hangman", "computer", "science", "physics",
    "keyboard", "notebook", "window", "garden", "river",
]

STAGES = [
    """
     +---+
         |
         |
         |
        ===""",
    """
     +---+
     O   |
         |
         |
        ===""",
    """
     +---+
     O   |
     |   |
         |
        ===""",
    """
     +---+
     O   |
    /|   |
         |
        ===""",
    """
     +---+
     O   |
    /|\\  |
         |
        ===""",
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===""",
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ===""",
]


def pick_word(word_list):
    """Return one random word from word_list."""
    return random.choice(word_list)


def show_progress(secret_word, guessed_letters):
    """Return the word with unguessed letters as '_'."""
    return " ".join(ch if ch in guessed_letters else "_" for ch in secret_word)


def play(secret_word, max_wrong=6):
    """Main game loop."""
    guessed = set()
    wrong = 0
    print("Welcome to Hangman! Guess the word, one letter at a time.")

    while wrong < max_wrong and any(ch not in guessed for ch in secret_word):
        print(STAGES[wrong])
        print("\nWord:  ", show_progress(secret_word, guessed))
        print("Tries left:", max_wrong - wrong)
        letter = input("Your guess: ").strip().lower()

        if len(letter) != 1 or not letter.isalpha():
            print("Please enter a single letter.\n")
            continue
        if letter in guessed:
            print(f"You already tried '{letter}'. Try another.\n")
            continue

        guessed.add(letter)
        if letter in secret_word:
            print(f"Nice! '{letter}' is in the word.\n")
        else:
            wrong += 1
            print(f"Nope — '{letter}' is not in the word.\n")

    if all(ch in guessed for ch in secret_word):
        print(f"You win! The word was '{secret_word}'.")
    else:
        print(STAGES[wrong])
        print(f"Game over! The word was '{secret_word}'.")


if __name__ == "__main__":
    play(pick_word(WORD_LIST))
