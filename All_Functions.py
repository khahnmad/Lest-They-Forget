# All imports
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import csv
import time
import nltk
import string
from nltk.corpus import stopwords
from nltk.util import ngrams
import numpy as np
from sklearn.linear_model import LinearRegression
import re
import sys

# nltk.download('stopwords')
# nltk.download('movie_reviews')
# nltk.download('vader_lexicon')

# Variables
shooting_keywords = {'Plano': ["spencer hight", "dallas cowboys", "meredith hight", "dallas", "plano", "sunday",
                               "caleb edwards", "deffner", "rushin"],
                     'Pittsburgh': ["pittsburgh", "synagogue", "bowers", "tree of life", "squirrel hill", "jewish",
                                    "anti-semitism", "jews"],
                     'Vegas': ["paddock", "mandalay bay hotel", "route 91 harvest", "las vegas", "aldean", "concert",
                               "mesquite", "hotel", "lombardo"],
                     'SanBernadino': ['syed', 'rizwan', 'farook', 'tashfeen', 'malik', 'SUV', "inland regional center",
                                      "san bernardino", "redlands", "christmas party", "public health department",
                                      "bomb"],
                     'Houston': ['david', 'conley', 'harris county', 'ex-girlfriend', 'houston', 'saturday',
                                 'valerie jackson', 'window', 'black', 'arrested'],
                     'Odessa': ['saturday', 'midland', 'odessa', 'seth', 'aaron', 'ator', 'west texas', 'traffic stop',
                                'white van', 'movie theater', 'random', 'white'],
                     'Bogue': ['willie', 'cory', 'godbolt', 'arrested', 'lincoln county', 'bogue chitto', 'brookhaven',
                               'barbara mitchell'],
                     'DC': ['washington navy yard', 'aaron alexis', 'monday', 'contractor', '12 people'],
                     'Boulder': ['king soopers', 'boulder', 'ahmad al', 'aliwi', 'al-issa', 'arrested', '9mm handgun',
                                 'table mesa drive', 'eric talley', 'boulder police', 'monday', 'in custody'],
                     'VirginiaBeach': ['virginia beach', 'dewayne', 'craddock', 'employee', 'nettleton', '.45-caliber',
                                       'engineer', 'municipal']
                     }
stopwords = stopwords.words('english')


# Importing and Set up Functions
def make_soup(url):  # gets soup given a url
    return bs(requests.get(url).text, "html.parser")


def import_csv(csv_file):  # parses data into a nested list
    nested_list = []  # initialize list
    with open(csv_file, newline='', encoding='utf-8') as csvfile:  # open csv file
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            nested_list.append(row)  # add each row of the csv file to a list
    return nested_list  # return nested list

def manage_overflow():
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)


def import_text_data(all_files):
    # Import all the text data
    # Resolves the huge fields error that you get from importing some of the csv files
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    # Get the text for each of the articles
    all_text = []
    for file in all_files:

        as_list = import_csv(file)  # import the file as a nested list

        # This regex works for the v2 files only
        location = re.findall(r"(?<=2\-)(.*?)(?=\_)",
                              file)  # use this regex to extract the location from the name of the file
        # For example: newspaper-text\v2-Bogue_Text-first-month.csv -> gets between 2- and _
        # This regex works for the unclean files
        if len(location) < 1:
            location = re.findall(r"(?<=clean)(.*?)(?=\_)", file)
            # gets everything between clean and _

        as_list[0].append('Location')  # add a location category to the beginning of each file
        for article in as_list[1:]:
            article.append(location[0])  # tag the location to each article

        # if the location of the last appened file matches the current appended file
        if len(all_text) > 0 and all_text[-1][1][-1] == location[0]:
            for item in as_list[1:]:
                all_text[-1].append(item)  # then add the current file to the list for the last file
            # this part combines the three files for each of the shootings into one list
        else:
            all_text.append(as_list)
        """ OUTPUT: list all_text contains a list for each of the *shooting* in all_files
            So, 10 lists, one for each of the ten shootings 
        """
    return all_text


def export_nested_list(csv_name, nested_list):
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in nested_list:
            writer.writerow(row)


def export_list(csv_name, list_):
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(list_)


def get_text(urls_list):
    ''' Gets the paragraph text from each url in a given list of urls '''
    url_text = []
    count = 0
    for url in urls_list:  # takes about a second per url
        start = time.time()
        print(f'working on: {url}')
        soup = make_soup(url)
        paragraphs = soup.find_all('p')
        stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]

        url_text.append(" ".join(stripped_paragraph))
        end = time.time()
        print(f'Number {count} complete in {end - start} seconds')

        if end - start > 2:  # Prints the websites that take a long time to extract
            print(url)
        count += 1
    return url_text


def combine_months_to_df(paths):
    first_text = pd.read_csv(paths[0])
    second_text = pd.read_csv(paths[1])
    third_text = pd.read_csv(paths[2])

    first_two_df = first_text.append(second_text, ignore_index=True)
    df = first_two_df.append(third_text, ignore_index=True)
    return df

def combine_files_to_df(paths):
    first_df = pd.read_csv(paths[0])
    for path in paths[1:]:
        df = first_df.append(pd.read_csv(path), ignore_index=True)
    return df



# Cleaning Functions
def remove_capitalization(cap_list):
    return [cap_list[i].lower() for i in range(len(cap_list))]


def clean_text(url_list, text_list):
    ''' does tokenization, lowercase, stopword removal, punctuation removal, empty space removal, and gets rid of the
    scraped text that is just an error message and not real text.
    Then it returns the urls that go with the text and a list of a string for each article'''
    clean_list, new_url_list = [], []
    extra_stopwords = ['``', "'s", '•', "n't", '.', '’', '”', '—', '‘', '“', '©', '___', "''", '==\\']

    for i in range(len(text_list)):

        tokenized = nltk.word_tokenize(text_list[i])  # tokenize

        lowercase = remove_capitalization(tokenized)  # remove capitalization

        no_stopwords = [word for word in lowercase if word not in stopwords]  # remove stopwords

        # remove punctuation
        punct = [str(x) for x in string.punctuation]

        for item in extra_stopwords:
            punct.append(item)
        no_punct = [item for item in no_stopwords if item not in punct]

        # remove empty strings
        while '' in no_punct:
            no_punct.remove('')

        if len(no_punct) > 25:  # means the the article is so short that it was probably a broken link
            clean_list.append(" ".join(no_punct))  # returns a string of the cleaned text
            new_url_list.append(url_list[i])

    return new_url_list, clean_list


# Text cleaning functions
def clean_trigram_text(string):
    """
    This takes a string of text, tokenizes it, removes stopwords, and splits it into trigrams
    """
    extra_stopwords = ['``', "'s", '•', "n't", '.']
    tokenized = nltk.word_tokenize(string)
    cleaned = [string for string in tokenized if string not in extra_stopwords]
    trigrams = extract_ngrams(cleaned, 3)
    return trigrams


def clean_bigram_text(string):
    """
    This takes a string of text, tokenizes it, removes stopwords, and splits it into bigrams
    """
    extra_stopwords = ['``', "'s", '•', "n't", '.']
    tokenized = nltk.word_tokenize(string)
    cleaned = [string for string in tokenized if string not in extra_stopwords]
    bigrams = extract_ngrams(cleaned, 2)
    return bigrams


def tokenize_text(string):
    """
    This takes a string of text, tokenizes it and removes stopwords
    """
    extra_stopwords = ['``', "'s", '•', "n't", '.']
    tokenized = nltk.word_tokenize(string)
    cleaned = [string for string in tokenized if string not in extra_stopwords]
    return cleaned


# Processing Functions
def extract_ngrams(data, num):
    '''
    input: tokenized list of data, type of ngram
    output: readable ngrams
    '''
    n_grams = ngrams(data, num)
    return [' '.join(grams) for grams in n_grams]


def apply_ngrams(df):
    # Apply ngram/cleaning functions to the text in the df
    df['trigrams'] = df['text'].apply(clean_trigram_text)
    df['bigrams'] = df['text'].apply(clean_bigram_text)
    df['text'] = df['text'].apply(tokenize_text)

    # Limit the publication date to just the day, instead of the hour and second
    # This makes the following graph more readable
    for index, row in df.iterrows():
        if type(df.loc[index, 'publish_date']) == str:
            df.loc[index, 'publish_date'] = df.loc[index, 'publish_date'][:10]
    return df


def freq_analysis(df, search_phrase):
    # For trigram search phrases
    if len(search_phrase.split()) == 3:
        for index, row in df.iterrows():
            count = 0
            for trigram in df.loc[index, 'trigrams']:
                if trigram == search_phrase:
                    count += 1
            df.loc[index, search_phrase[:3]] = count

    # For bigram search phrases
    if len(search_phrase.split()) == 2:
        for index, row in df.iterrows():
            count = 0
            for bigram in df.loc[index, 'bigrams']:
                if bigram == search_phrase:
                    count += 1
            df.loc[index, search_phrase[:3]] = count

    # For single word searches
    if len(search_phrase.split()) == 1:
        for index, row in df.iterrows():
            count = 0
            for item in df.loc[index, 'text']:
                if item == search_phrase:
                    count += 1
            df.loc[index, search_phrase[:3]] = count


def get_lr(ex, why):
    X = np.array(ex).reshape(-1, 1)
    y = why
    reg = LinearRegression().fit(X, y)
    return reg.score(X, y)


# Media Cloud functions
def all_matching_stories(mc_client, q, fq):
    """
    Return all the stories matching a query within Media Cloud. Page through the results automatically.
    :param mc_client: a `mediacloud.api.MediaCloud` object instantiated with your API key already
    :param q: your boolean query
    :param fq: your date range query
    :return: a list of media cloud story items
    """
    last_id = 0
    more_stories = True
    stories = []
    while more_stories:
        page = mc_client.storyList(q, fq, last_processed_stories_id=last_id, rows=500, sort='processed_stories_id')
        print("  got one page with {} stories".format(len(page)))
        if len(page) == 0:
            more_stories = False
        else:
            stories += page
            last_id = page[-1]['processed_stories_id']
    return stories
