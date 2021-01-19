# Zachary Tarell - zjt170000
# Language Models - Homework 4_Program1
# CS 4395.001 - Fall 2020 - Mazidi

import sys
import re
import pickle
import nltk
from nltk import word_tokenize
from nltk.util import ngrams


# a.	create a function with a filename as argument
def process_lang(raw_text):
    # b.	read in the text and remove newlines
    text = re.sub(r'[.?!,:;()\-\'\"\d]', ' ', raw_text.lower())

    # c.	tokenize the text
    # tokens = word_tokenize(text)
    # print('\nNumber of tokens:', len(tokens))
    unigrams = word_tokenize(text)

    # d.	use nltk to create a bigrams list
    bigrams_list = [(unigrams[k], unigrams[k + 1]) for k in range(len(unigrams) - 1)]
    # print(bigrams_list)

    # e.	create a unigrams list
    # unigrams_list = list(ngrams(unigrams, 1))
    unigrams_list = list(unigrams)

    # f.	use the bigram list to create a bigram dictionary of bigrams and counts
    # [‘token1 token2’] -> count
    bigram_dict = {b: bigrams_list.count(b) for b in set(bigrams_list)}

    # g.	use the unigram list to create a unigram dictionary of unigrams and counts
    # [‘token’] -> count
    unigram_dict = {t: unigrams_list.count(t) for t in set(unigrams_list)}

    # h.	return the unigram dictionary and bigram dictionary from the function
    return unigram_dict, bigram_dict
    # i.	done in main function


# Main function
if __name__ == '__main__':
    # file name
    if len(sys.argv) > 3:
        english = sys.argv[1]
        french = sys.argv[2]
        italian = sys.argv[3]
        print('Input files: ', english, ' ', french, ' ', italian)

        with open('LangId.train.English', 'r') as f:
            english_raw = f.read()
        f.close()
        with open('LangId.train.French', encoding="utf8") as f:
            french_raw = f.read()
        f.close()
        with open('LangId.train.Italian', encoding="utf8") as f:
            italian_raw = f.read()
        f.close()

        # i.	in the main body of code, call the function 3 times for each training file,
        # pickle the 6 dictionaries and save to files with appropriate names.
        # processing function for the english training file
        english_unigram, english_bigram = process_lang(english_raw)

        # pickle the english unigram and bigram dictionaries
        pickle.dump(english_unigram, open('english_unigram', 'wb'))
        pickle.dump(english_bigram, open('english_bigram', 'wb'))

        # call the processing function for the french training file
        french_unigram, french_bigram = process_lang(french_raw)

        # pickle the french unigram and bigram dictionaries
        pickle.dump(french_unigram, open('french_unigram', 'wb'))
        pickle.dump(french_bigram, open('french_bigram', 'wb'))
        # french_bi_pickle = pickle.load(open('french_bigram', 'rb'))

        # call the processing function for the italian training file
        italian_unigram, italian_bigram = process_lang(italian_raw)

        # pickle the italian unigram and bigram dictionaries
        pickle.dump(italian_unigram, open('italian_unigram', 'wb'))
        pickle.dump(italian_bigram, open('italian_bigram', 'wb'))

    else:
        print('File name missing')
    print('\nProgram ended')
