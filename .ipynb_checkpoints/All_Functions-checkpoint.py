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

# nltk.download('stopwords')
# nltk.download('movie_reviews')
# nltk.download('vader_lexicon')

stopwords = stopwords.words('english')

# Importing and Set up Functions
def make_soup(url):  # gets soup given a url
    return bs(requests.get(url).text, "html.parser")


def import_csv(csv_file):  # parses data into a nested list
    nested_list = []  # initialize list
    with open(csv_file, newline='',encoding='utf-8') as csvfile:  # open csv file
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            nested_list.append(row)  # add each row of the csv file to a list
    return nested_list  # return nested list

def export_nested_list(csv_name, nested_list):
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in nested_list:
            writer.writerow(row)

def get_text(urls_list):
    ''' Gets the paragraph text from each url in a given list of urls '''
    url_text = []
    count = 0
    for url in urls_list: # takes about a second per url
        start = time.time()
        print(f'working on: {url}')
        soup = make_soup(url)
        paragraphs = soup.find_all('p')
        stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]

        url_text.append(" ".join(stripped_paragraph))
        end = time.time()
        print(f'Number {count} complete in {end - start} seconds')

        if end - start > 2: # Prints the websites that take a long time to extract
            print(url)
        count +=1
    return url_text

def combine_months_to_df(first_path, second_path, third_path):
    first_text = pd.read_csv(first_path)
    second_text = pd.read_csv(second_path)
    third_text = pd.read_csv(third_path)

    first_two_df = first_text.append(second_text, ignore_index=True)
    df = first_two_df.append(third_text, ignore_index=True)
    return df

# Cleaning Functions
def remove_capitalization(cap_list):
    return [cap_list[i].lower() for i in range(len(cap_list))]


def clean_text(url_list, text_list):
    ''' does tokenization, lowercase, stopword removal, punctuation removal, empty space removal, and gets rid of the
    scraped text that is just an error message and not real text.
    Then it returns the urls that go with the text and a list of a string for each article'''
    clean_list, new_url_list = [], []
    extra_stopwords = ['``',"'s",'•',"n't",'.','’', '”', '—', '‘', '“', '©', '___']

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
    extra_stopwords = ['``',"'s",'•',"n't",'.']
    tokenized = nltk.word_tokenize(string)
    cleaned = [string for string in tokenized if string not in extra_stopwords]
    trigrams = extract_ngrams(cleaned, 3)
    return trigrams

def clean_bigram_text(string):
    """
    This takes a string of text, tokenizes it, removes stopwords, and splits it into bigrams
    """
    extra_stopwords = ['``',"'s",'•',"n't",'.']
    tokenized = nltk.word_tokenize(string)
    cleaned = [string for string in tokenized if string not in extra_stopwords]
    bigrams = extract_ngrams(cleaned, 2)
    return bigrams

def tokenize_text(string):
    """
    This takes a string of text, tokenizes it and removes stopwords
    """
    extra_stopwords = ['``',"'s",'•',"n't",'.']
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
    df['text']= df['text'].apply(tokenize_text)

    # Limit the publication date to just the day, instead of the hour and second
    # This makes the following graph more readable
    for index, row in df.iterrows():
        if type(df.loc[index,'publish_date'])==str:
            df.loc[index,'publish_date'] = df.loc[index,'publish_date'][:10]
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
