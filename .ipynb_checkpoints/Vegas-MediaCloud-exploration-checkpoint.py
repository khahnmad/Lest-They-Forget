# All imports
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import csv
import time
import nltk
import string
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# nltk.download('stopwords')
# nltk.download('movie_reviews')
# nltk.download('vader_lexicon')


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

def get_text(urls_list):
    url_text = []
    count = 0
    for url in urls_list: # takes about a second per url
        start = time.time()
        soup = make_soup(url)
        paragraphs = soup.find_all('p')
        stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]

        url_text.append(" ".join(stripped_paragraph))
        end = time.time()
        print(f'Number {count} complete in {end - start} seconds')
        # print(url)
        if end - start > 2:
            print(url)
        count +=1
    return url_text

# Cleaning Functions
def remove_capitalization(cap_list):
    return [cap_list[i].lower() for i in range(len(cap_list))]


def clean_text(url_list, text_list):
    clean_list, new_url_list = [], []

    for i in range(len(text_list)):

        tokenized = nltk.word_tokenize(text_list[i])  # tokenize

        lowercase = remove_capitalization(tokenized)  # remove capitalization

        no_stopwords = [word for word in lowercase if word not in stopwords]  # remove stopwords

        # remove punctuation
        punct = [str(x) for x in string.punctuation]

        for item in ['’', '”', '—', '‘', '“', '©', '___']:
            punct.append(item)
        no_punct = [item for item in no_stopwords if item not in punct]

        # remove empty strings
        while '' in no_punct:
            no_punct.remove('')

        if len(no_punct) > 25:  # means the the article is so short that it was probably a broken link
            clean_list.append(" ".join(no_punct))  # returns a string of the cleaned text
            new_url_list.append(url_list[i])

    return new_url_list, clean_list


# Variables
csv_file = 'gun-or-gun-control-or-gun-r-all-story-urls-20210518102140.csv'
stopwords = stopwords.words('english')

# Import the file
vegas_media = import_csv(csv_file)

# Filter to just the the most relevant articles
count = 0
gun_shooting_titles = []
for i in range(len(vegas_media)):
    if 'gun' in vegas_media[i][2] or 'shooting' in vegas_media[i][2] and 'kansas' not in vegas_media[i][3]:
        # print(vegas_media[i][2])
        gun_shooting_titles.append(vegas_media[i][3])
        count += 1
print("Number of articles:", count)

# For some reason it gets stuck on certain websites. Couldnt figure out why it gets stuck, so I'm just removing those websites
for url in gun_shooting_titles[:]: # have to make a copy of gun_shooting_titles to iterate through in order to remove things correctly
    if 'kansascity' in url:
        gun_shooting_titles.remove(url)
    if 'miamiherald' in url:
        gun_shooting_titles.remove(url)
    if 'sacbee' in url:
        gun_shooting_titles.remove(url)
    if 'seattle' in url:
        gun_shooting_titles.remove(url)
    if 'feeds.reuters' in url:
        gun_shooting_titles.remove(url)
gun_shooting_titles.remove('http://www.cbsnews.com/videos/calls-capture-first-responders-struggling-to-make-sense-of-shooting-chaos/')
gun_shooting_titles.remove('http://www.cbsnews.com/videos/cbs-news-poll-54percent-support-stricter-gun-laws/')
gun_shooting_titles.remove('http://feeds.cbsnews.com/~r/CBSNewsMain/~3/k9gMP3UNXPE/')


# Get the url text
url_text = get_text(gun_shooting_titles[:500])

# Clean the text
url_list, cleaned_text = clean_text(gun_shooting_titles[:500],url_text)

# Do a sentiment analysis
sia = SentimentIntensityAnalyzer()

sia_sentiment = []
for text in cleaned_text:
    sia_sentiment.append(sia.polarity_scores(text))
print('Get the sentiments')

sia_df = pd.DataFrame({'url':url_list,'text': cleaned_text, 'sentiment':sia_sentiment})


for i in range(len(vegas_media)):
    for index, row in sia_df.iterrows():
        if sia_df.loc[index, 'url'] == vegas_media[i][3]:
            sia_df.loc[index,'publish_date'] = vegas_media[i][1]
            sia_df.loc[index,'title'] = vegas_media[i][2]
            sia_df.loc[index,'themes'] = vegas_media[i][6]

sia_df.to_csv('Vegas_Data.csv')