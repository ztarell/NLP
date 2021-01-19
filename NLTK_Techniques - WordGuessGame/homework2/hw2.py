# Zachary Tarell - zjt170000
# Preprocessing and Guessing Game - Homework 2
# CS 4395.001 - Fall 2020 - Mazidi

import sys
import random
from random import randint
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy as np


# preprocessing function
def preprocessing(raw_text):
    # Question 2
    # print the Lexical Diversity
    tokens = word_tokenize(raw_text.lower())
    set1 = set(tokens)
    print("\nLexical diversity: %.2f" % (len(set1) / len(tokens)))

    # Question 3a
    # tokenize the lower-case raw text
    # reduce the tokens to only those that are alpha
    # not in the NLTK stopword list, and have length > 5
    stop_words = set(stopwords.words('english'))
    tokens = [t.lower() for t in word_tokenize(raw_text) if t.isalpha() and len(t) > 5 and t not in stop_words]

    # Question 3b
    # lemmatize the tokens and use set() to make a list of unique lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas_unique = sorted(list(set(lemmas)))

    # Question 3c
    # print first 20 tagged items
    tags = nltk.pos_tag(lemmas_unique)
    print('\nFirst 20 Tagged Items:')
    for j in range(50):
        print(tags[j])

    # Question 3d
    # create a list of only those lemmas that are nouns
    nouns = list([x[0] for x in tags if x[1].startswith("N")])

    # Question 3e
    # print the number of tokens (from step a) and the number of nouns (step d)
    print('\nNumber of Tokens:', len(tokens))
    print('\nNumber of Nouns:', len(nouns))

    # Question 3f
    # return tokens(not unique tokens) from step a and nouns from the function
    return tokens, nouns


# Game function
def guessing_game(wordsForGame):
    print("\n\tLet's play a word guessing game!")

    while True:
        # running any random word
        wordlist = wordsForGame[randint(0, 50)]
        ran_word = wordlist[0]

        # Initialize an array which consists of the word as the letters are guessed eventually
        array = ['_' for i in range(len(ran_word))]
        points = 5

        # Loop to take inputs
        while True:
            print(*array)
            # If all the letters are guessed then print the word
            if "_" not in array:
                print("You solved it!")
                print("Current score:", points)
                break

            letter = input("Guess a letter: ")

            # If the letter is !, then break
            if letter == "!":
                print("You have entered !. Terminating the program!")
                return 0

            # If the letter is in word, then update the array and increase score by 1
            if letter in ran_word:
                for i in range(len(ran_word)):
                    if ran_word[i] == letter:
                        array[i] = letter
                points += 1
                print("Right! Score is", points)
                continue

            # If the letter is not in word, then update the array and decrease score by 1
            else:
                points -= 1
                if points == 0:
                    print("Sorry, you are out of your points! The word is", ran_word)
                    return 0
                print("Sorry, guess again. Score is", points)
        print("\n\tGuess another word")


# Main function
if __name__ == '__main__':
    # file name
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print('Input file: ', input_file)

        with open('anat19.txt', 'r') as f:
            raw_text = f.read()

        tokens, nouns = preprocessing(raw_text)

        # Question 4
        # Make a dictionary of {noun:count of noun in tokens} items from the nouns and tokens lists
        # sort the dict by count and print the 50 most common words and their counts
        counts = {t: tokens.count(t) for t in nouns}
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        # Save these words to a list because they will be used in the guessing game.
        wordsForGame = []
        print("\n50 most common words:")
        for i in range(50):
            wordsForGame.append(sorted_counts[i])
            print(sorted_counts[i])

        # start guessing game and pass list of words
        guessing_game(wordsForGame)

    else:
        print('File name missing')
    print('\nProgram ended')
