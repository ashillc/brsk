import random
import time

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORD_LIST_URL = "http://www.mieliestronk.com/corncob_lowercase.txt"


def get_lookup_word_list() -> list:
    """Get the word list lookup."""
    words_str = requests.get(WORD_LIST_URL).text  # Get the list of lookup words from the internet.
    words_list = words_str.split("\r\n")  # Split the words

    return words_list


def generate_lookup_dict(word_list: list) -> dict:
    """Generate a lookup dict for quick reference.
       e.g.
       {
         "a": {
                "6" : ['ashill']
              }
        "c": {
                "9" : ['chiranjan']
              }
       }
    """

    lookup_dict = {}
    for word in word_list:  # Loop through the words in the list
        if not word:
            continue  # If its a blank word, skip it
        first_letter = word[0]  # Extract the first letter
        word_len = str(len(word))

        if first_letter not in lookup_dict:
            lookup_dict[first_letter] = {}  # If lookup doesnt already exist, create it

        if word_len not in lookup_dict[first_letter]:
            lookup_dict[first_letter][word_len] = [word]  # If lookup list doesnt exist, initialise it
        else:
            if word not in lookup_dict[first_letter][word_len]:  # Check if word is in list already
                lookup_dict[first_letter][word_len].append(word)  # Add it to the list

    return lookup_dict


def lookup_and_replace(input_str: str, lookup_dict: dict) -> str:
    """Find and replace the words in the input string."""

    output_str = input_str

    for word in input_str.split():  # Split the word list and loop through each word
        word_len = str(len(word))
        first_letter = word[0]
        letter_lookup = lookup_dict.get(first_letter)
        if not letter_lookup:  # Check if first letter is in dict else continue with next iteration
            continue

        lookup_list = letter_lookup.get(word_len)
        if not lookup_list:  # Check if nested lookup_list is in lookup dictionary else continue with next iteration
            continue

        replacement = random.choice(lookup_list)  # Get a random choice from the list, (I googled random.choice :))
        output_str = output_str.replace(word, replacement)  # Get the replacement words

    return output_str


def main():
    """Main function to run the scrabble game."""
    print("Welcome to the Scrabble Word Program!")
    time.sleep(2)
    print("Ready to begin playing?...")

    word_list = get_lookup_word_list()  # Get the word list from the web
    lookup_dict = generate_lookup_dict(word_list)  # Generate lookup dictionary

    while True:  # Loop until exit
        print("Enter a word or phrase OR type quit to exit: ")
        try:
            input_str = input().strip().lower()  # Get user input
            if not input_str:
                print("Incorrect input! Please try again")
            elif input_str == "quit" or input_str == "exit":
                print("Thanks for playing! See you next time")
                exit()
            else:
                replacement_str = lookup_and_replace(input_str, lookup_dict)
                print(f"The replacement for '{input_str}' is '{replacement_str}'")
                print("Lets try again...")
        except Exception:
            print("I'm sorry. We failed to capture that. Please try again")


if __name__ == "__main__":
    main()
