#######
# File: CS4395_HW5_drb160130_zjt170000.py
# Author 1: Dorian Benitez (drb160130)
# Author 2: Zachary Tarell (zjt170000)
# Date: 10/4/2020
# Purpose: CS 4395.001 - Homework #5 (Web Scraping - Web Crawler)
#######

import pickle
import re
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from urllib import request
import urllib.request
import nltk


# Function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


# Main function
if __name__ == '__main__':

    # Build a web crawler function that starts with a URL representing a topic and outputs a list of 40 relevant URLs.
    starter_url = "https://www.wsj.com/news"
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    url_list = []
    count = 0

    print("\nStarter URL: " + starter_url)
    print("\nRelevant URLs: ")

    # Print top 40 relevant URLs and append each one to a list
    for link in soup.find_all('a'):
        if "login" not in link.get('href') and "getnewsmart" not in link.get('href') and "centralbanking" not in link.get('href') and len(link.get('href')) > 5:
            url_list.append((str(link.get('href'))))
            print("\t" + str(count + 1) + ". " + link.get('href'))
            count += 1
        if count > 39:
            break
    count = 0

    # Write a function to loop through the URLs and scrape all text off each page.
    # Store each page’s text in its own file, up to 15 files.
    for i in range(len(url_list)):
        try:
            html = urllib.request.urlopen(url_list[i])
        except:
            pass
        soup = BeautifulSoup(html, "html.parser")
        data = soup.findAll(text=True)
        result = filter(visible, data)
        temp_list = list(result)
        temp_str = ' '.join(temp_list)

        # Only write the top 15 URLs with the best scraped text to a new file
        if len(temp_str) > 1500 and count < 15 and "javascript" not in temp_str.lower() and "unsupported browser" not in temp_str.lower():
            count += 1
            with open("raw_" + str(count) + ".txt", 'w') as f:
                f.write(str(temp_str.encode("utf-8")))

        if count == 15:
            break

    # Write a function to clean up the text.
    for i in range(1, 16):
        with open("raw_" + str(i) + ".txt", 'r') as f:
            raw = f.read().replace('\\n', '').replace('\\t', '').replace('\\r', '')
        count += 1

        # Extract sentences with NLTK’s sentence tokenizer.
        sent_tokens = nltk.sent_tokenize(raw)

        # Write the processed text sentences from each file to a new file.
        with open("processed_" + str(count) + ".txt", 'w') as f:
            for t in range(len(sent_tokens)):
                if '\\' not in sent_tokens[t]:
                    f.write(str(sent_tokens[t].encode("utf-8")) + '\n')

    tf_dict = {}  # Dictionary to hold the words found in the URL text files

    # Function to extract 40 important terms from the pages using the importance measure tf-idf.
    for i in range(16, 30):

        # Lower-case everything, remove stopwords and punctuation.
        with open("processed_" + str(i) + ".txt", 'r') as f:
            lower_raw = f.read().lower()
        tokens = word_tokenize(lower_raw)
        tokens = [w for w in tokens if w.isalpha()
                  and w not in stopwords.words('english')]

        # Update the dictionary to store the words found in the text files
        for t in tokens:
            if t in tf_dict:
                tf_dict[t] += 1
            else:
                tf_dict[t] = 1

        # Use the tf-idf importance measure to extract important terms
        for t in tf_dict.keys():
            tf_dict[t] = tf_dict[t] / len(tokens)
        count += 1

    # Print the top 40 important terms.
    sort_orders = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
    print("\nMost important words: ")
    for i in range(0, 40):
        if next(iter(sort_orders[i])) != "b":
            print("\t" + str(i + 1) + ". " + next(iter(sort_orders[i])))

    # Manually determine the top 10 terms based on your domain knowledge.
    dk_10_list = ["home", "buy", "sell", "rates", "marketplace", "new", "insights", "property", "area", "information"]

    # Build a searchable knowledge base of facts that a ChatBot can share related to the 10 terms.
    knowledge_base = "Hello, my name is ChatBot.\n" \
                     "A homeowner's net worth is over thirty times greater than that of a renter.\n" \
                     "61.4% of the average American family's net worth is in home equity.\n" \
                     "The average mortgage interest rate in the United States is 3.21%.\n" \
                     "North Carolina is leading the United States in millennial population.\n" \
                     "The best day of the week to list your home for sale is on a Friday.\n" \
                     "On average, 500 people move to Atlanta, Georgia every day.\n" \
                     "Dallas, Texas has the highest employment rate in the United States.\n" \
                     "The median sale price of a home is $328,419 in the United States.\n" \
                     "In 2019, the number of homes sold was 652,878 in the United States.\n" \
                     "In 2019, the number of American homes that went up for sale was 1,066,903.\n" \
                     "The number of American homes newly listed on the market is 691,785.\n" \
                     "The number of homes sold above their original listing price is 32%.\n" \
                     "The three most competitive cities in the U.S. housing market are Tacoma, WA, Grand Rapids, MI, and Spokane, WA.\n" \
                     "The three fastest growing metropolitan cities in the U.S. housing market are Cleveland, OH, Memphis, TN, and Toms River, NJ.\n" \
                     "A large amount of people have relocated from California to Texas within the past couple of years.\n" \
                     "Houston, Texas is the fourth largest city in the United States by population.\n" \
                     "52.9% of Dallas, Texas residents are renters vs. the national average of 33%.\n" \
                     "In 2017, investors owned/rented out 18.2 million one-unit homes, including detached homes, town homes, and duplexes, providing housing for 42% of the nation’s renter households.\n" \
                     "Rental properties often guarantee a steady rate of return on your investment.\n" \
                     "The two most important benefits of owning rental properties is generating cash flow and earning value from appreciation.\n" \
                     "In 2019, there were about 14.7 million households and 45.2 million residents renting single-family homes in the United States.\n" \
                     "In 2013, NAR reported that the median age of first-time buyers was 31. On average these buyers purchased a 1,670 square-foot home costing $170,000.\n" \
                     "The nationwide nominal house price index is now 40% above its 2012 low-point and 4% above the peak reached in 2006.\n" \
                     "The mountain region has the highest home price increases each year.\n" \
                     "Residential construction activity continues to rise strongly, partly driven by lower mortgages rates.\n" \
                     "According to a NAR Community Preference Survey, 78% of respondents said that the neighborhood is more important to them than the size of the home.\n" \
                     "The most affordable zip codes with the best schools in the U.S. are 64014, 46060, and 75023.\n" \
                     "The worst time to buy a home is when inventory is running low, meaning that prices are running high.\n" \
                     "According to the U.S. Census Bureau, the average person will move 12 times within their lifetime.\n" \
                     "80% of people aged 65 and older own their own homes.\n" \
                     "The number of people renting homes aged over 59 grew 43% in the last 10 years."

    # Extract the knowledge base sentences with NLTK’s sentence tokenizer.
    kb_sents = sent_tokenize(knowledge_base)

    # Write the knowledge base sentences to a new file
    with open('KnowledgeBase.txt', 'w') as f:
        for i in range(len(kb_sents)):
            f.write(str(kb_sents[i]) + '\n')

    dict_counter = 1
    kb_dict = {}

    # Write the knowledge base list to a dictionary and pickle dump it
    for sentence in kb_sents:
        kb_dict.update({sentence: dict_counter})
        dict_counter += 1
    pickle.dump(kb_dict, open("KnowledgeBasePickle", 'wb'))
