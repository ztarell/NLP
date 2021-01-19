# Zachary Tarell - zjt170000
# Language Models - Homework 4_Program2
# CS 4395.001 - Fall 2020 - Mazidi

import pickle
from nltk import word_tokenize, ngrams


def compute_prob(text, unigram_dict, bigram_dict, V):

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_laplace = 1

    for b in bigrams_test:
        n = bigram_dict[b] if b in bigram_dict else 0
        d = unigram_dict[b[0]] if b[0] in unigram_dict else 0

        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_laplace


if __name__ == '__main__':

    # a.	Read in your pickled dictionaries.
    english_unigram = pickle.load(open('english_unigram', 'rb'))
    english_bigram = pickle.load(open('english_bigram', 'rb'))

    french_unigram = pickle.load(open('french_unigram', 'rb'))
    french_bigram = pickle.load(open('french_bigram', 'rb'))

    italian_unigram = pickle.load(open('italian_unigram', 'rb'))
    italian_bigram = pickle.load(open('italian_bigram', 'rb'))

    V = len(english_unigram) + len(french_unigram) + len(italian_unigram)

    # b.	For each test file, calculate a probability for each language
    # and write the language with the highest probability to a file.
    with open('LangId.test', 'r') as f:
        test_file = f.readlines()
    f.close()

    # Open the actual solution and append each each line to a list
    with open('LangId.sol', 'r') as f:
        real_solution = f.readlines()
    f.close()

    # Create/Write a new file to store our predicted solution
    f = open("Solution_File.txt", "w")
    f.close()

    # These values are to be used later in the program
    predicted_solution = []
    wrong_lines = []
    correct_count = 0
    line_number = 0

    # c.	Compute and output your accuracy as the percentage of correctly classified instances in the test set.
    # The file LangId.sol holds the correct classifications.
    for line in test_file:

        eng_p = compute_prob(line, english_unigram, english_bigram, V)
        # print(eng_p)
        fre_p = compute_prob(line, french_unigram, french_bigram, V)
        # print(fre_p)
        ita_p = compute_prob(line, italian_unigram, italian_bigram, V)
        # print(ita_p)

        line_number += 1
        english_count = 0
        french_count = 0
        italian_count = 0

        # For each word in the line, analyze which language (English/French/Italian) is being used
        for word in line.split():
            if word in english_unigram:
                english_count += 1
            elif word in english_bigram:
                english_count += 1
            elif word in french_unigram:
                french_count += 1
            elif word in french_bigram:
                french_count += 1
            elif word in italian_unigram:
                italian_count += 1
            elif word in italian_bigram:
                italian_count += 1

        # Write the language with the highest probability to a list and the "Solution_File.txt" file
        # if eng_p > (fre_p and ita_p):
        if eng_p > fre_p and eng_p > ita_p:
            # english_count += 1
            predicted_solution.append(str(line_number) + " English\n")
            f = open("Solution_File.txt", "a")
            f.write(str(line_number) + " English\n")
            f.close()

        # elif fre_p > (eng_p and ita_p):
        elif fre_p > eng_p and fre_p > ita_p:
            # french_count += 1
            predicted_solution.append(str(line_number) + " French\n")
            f = open("Solution_File.txt", "a")
            f.write(str(line_number) + " French\n")
            f.close()

        # elif ita_p > (eng_p and fre_p):
        elif ita_p > eng_p and ita_p > fre_p:
            # italian_count += 1
            predicted_solution.append(str(line_number) + " Italian\n")
            f = open("Solution_File.txt", "a")
            f.write(str(line_number) + " Italian\n")
            f.close()

        else:
            predicted_solution.append(str(line_number) + " Unknown\n")
            f = open("Solution_File.txt", "a")
            f.write(str(line_number) + " Unknown\n")
            f.close()

    # This compares the actual solution to our predicted solution
    for i in range(len(predicted_solution)):
        if predicted_solution[i] == real_solution[i]:
            correct_count += 1
        else:
            wrong_lines.append(i + 1)

    # d.	output your accuracy, as well as the line numbers of the incorrectly classified items
    accuracy = correct_count / len(predicted_solution)
    print("correct =", correct_count)
    print("num_items =", len(predicted_solution))
    print("accuracy =", '%.2f' % accuracy)
    print("incorrect items =", wrong_lines)
