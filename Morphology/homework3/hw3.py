# Zachary Tarell - zjt170000
# Morphology with Moby Dick - Homework 3
# CS 4395.001 - Fall 2020 - Mazidi

import sys
import re
from operator import itemgetter

import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


# preprocessing function
def processMobyDick(raw):
    # a.	lower case
    # b.	use a string function to replace all occurrences of ‘--‘ with ‘ ‘
    # c.	use regex to remove all digits
    # d.	use regex to replace punctuation with a single space
    text = re.sub(r'[.?!,:;()\-\'\"\d]', ' ', raw_text.lower().replace('--', ''))

    # 3.	Tokenize the text and print the number of tokens
    tokens = word_tokenize(text)
    print('\nNumber of tokens:', len(tokens))
    # Save the list of tokens for step 11
    token_list = list(tokens)

    # 4.    Create a set of unique tokens and print the number of unique tokens
    set_unique = set(tokens)  # find unique tokens
    print('Number of unique tokens:', len(set_unique))

    # 5.	Create a list of important words by removing stop words from the unique tokens list.
    # Display the number of important words.
    tokens_important = [t for t in set_unique if t.isalpha() and
                        t not in stopwords.words('english')]
    print('Number of important words:', len(tokens_important))

    # 6.	Using the list of important words, create a list of tuples of the word and stemmed word, like this:
    # 			[(‘remarkably’,’remark’), (‘prevented’,’prevent’) …]
    stemmer = PorterStemmer()
    stems = [(t, stemmer.stem(t)) for t in tokens_important]

    # 7.	Create a dictionary where the key is the stem, and the value is a list of words with that stem, like this:
    # 			{‘achiev’: [‘achieved’, ‘achieve’]
    # 			  ‘accident’: [‘accidentally’, ‘accidental’] … }
    stem_key_dict = {}
    for t in tokens_important:
        stem = stemmer.stem(t)
        stem_words = [w for w in tokens_important if w.startswith(stem)]
        stem_key_dict[stem] = stem_words
    # to print out the dictionary of stem as key from above...
    # for k, v in sorted(stem_key_dict.items()):
    #     print(k, '-->', v)

    # 8.    Print the number of dictionary entries
    print('Number of Dictionary entries:', len(stem_key_dict))

    # 9.    For the 25 dictionary entries with the longest lists,
    # print the stem and its list.One way to sort a dict by length of values:
    #     for k in sorted(stem_dict, key=lambda k: len(stem_dict[k]), reverse=True):
    print("Top 25 dictionary entries:")
    sort_orders = sorted(stem_key_dict.items(), key=lambda x: x[1], reverse=True)
    # Iterate over the sorted sequence
    count = 0
    for elem in sort_orders:
        if count < 25:
            count += 1
            print(elem)
        else:
            continue

    # max_key, max_value = max(sort_orders)
    # print(max_key, max_value)

    # 10.	Using the dict from step 9, write a function to compute edit distance.
    # Compute and print the edit distance between ‘continue’ and every word in the ‘continu’ list in the stem dict.
    def iterative_levenshtein(s, t):
        """
            iterative_levenshtein(s, t) -> ldist
            ldist is the Levenshtein distance between the strings
            s and t.
            For all i and j, dist[i,j] will contain the Levenshtein
            distance between the first i characters of s and the
            first j characters of t
        """

        rows = len(s) + 1
        cols = len(t) + 1
        dist = [[0 for x in range(cols)] for x in range(rows)]

        # source prefixes can be transformed into empty strings
        # by deletions:
        for i in range(1, rows):
            dist[i][0] = i

        # target prefixes can be created from an empty source string
        # by inserting the characters
        for i in range(1, cols):
            dist[0][i] = i

        for col in range(1, cols):
            for row in range(1, rows):
                if s[row - 1] == t[col - 1]:
                    cost = 0
                else:
                    cost = 1
                dist[row][col] = min(dist[row - 1][col] + 1,  # deletion
                                     dist[row][col - 1] + 1,  # insertion
                                     dist[row - 1][col - 1] + cost)  # substitution

        for r in range(rows):
            print(dist[r])

        return print('Edit distance {} and {}'.format(s,t),dist[row][col])

    # 11.	Perform POS tagging on the original text after step 3
    tags = nltk.pos_tag(token_list)

    # 12.	Create a dictionary of POS counts where the key is the POS,
    # and the value is the number of words with that POS. Print the dictionary.
    token_dict = {}
    for token, pos in tags:
        if pos not in token_dict:
            token_dict[pos] = 1
        else:
            token_dict[pos] += 1
    print('\nPOS counts in descending order:')
    for pos in sorted(token_dict, key=token_dict.get, reverse=True):
        print(pos, ':', token_dict[pos])


# Main function
if __name__ == '__main__':
    # file name
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print('Input file: ', input_file)

        with open('moby_dick.txt', 'r') as f:
            raw_text = f.read()

        processMobyDick(raw_text)

    else:
        print('File name missing')
    print('\nProgram ended')
