from dotenv import load_dotenv

print(load_dotenv())

# Imports
import os, mediacloud.api
import datetime
import time
import mediacloud.tags
import csv
from dateutil.relativedelta import *
import All_Functions as af

# Functions
# def all_matching_stories(mc_client, q, fq):
#     """
#     Return all the stories matching a query within Media Cloud. Page through the results automatically.
#     :param mc_client: a `mediacloud.api.MediaCloud` object instantiated with your API key already
#     :param q: your boolean query
#     :param fq: your date range query
#     :return: a list of media cloud story items
#     """
#     last_id = 0
#     more_stories = True
#     stories = []
#     while more_stories:
#         page = mc_client.storyList(q, fq, last_processed_stories_id=last_id, rows=500, sort='processed_stories_id')
#         print("  got one page with {} stories".format(len(page)))
#         if len(page) == 0:
#             more_stories = False
#         else:
#             stories += page
#             last_id = page[-1]['processed_stories_id']
#     return stories


def collect_stories(query, dates):
    # Check how many stories are there
    print(f'There are {mc.storyCount(query, dates)} stories for the query')

    # Fetch all the stories that match the query
    a = time.time()
    all_stories = af.all_matching_stories(mc, query, dates)
    b = time.time()
    print(f'Takes {b - a} seconds to run')

    # flatten things a little bit to make writing a CSV easier
    for s in all_stories:
        # see the "language" notebook for more details on themes
        theme_tag_names = ','.join(
            [t['tag'] for t in s['story_tags'] if t['tag_sets_id'] == mediacloud.tags.TAG_SET_NYT_THEMES])
        s['themes'] = theme_tag_names
    return all_stories


def write_csv(all_stories, name):
    fieldnames = ['stories_id', 'publish_date', 'title', 'url', 'language', 'ap_syndicated', 'themes', 'media_id',
                  'media_name', 'media_url']
    with open(name, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for s in all_stories:
            writer.writerow(s)


def collection_pipeline(year: int, month: int, day: int, shooting_name):
    # establish query - mass shooting = search word, US national media = collection
    ms_us_query = '"mass shooting" and tags_id_media:34412234'

    # establish date range
    start_date = datetime.date(year, month, day)
    end_first_month = start_date + relativedelta(months=+1)
    end_second_month = end_first_month + relativedelta(months=+1)
    end_third_month = end_second_month + relativedelta(months=+1)

    first_month = mc.dates_as_query_clause(start_date, end_first_month)  # default is start & end inclusive
    second_month = mc.dates_as_query_clause(end_first_month, end_second_month)
    third_month = mc.dates_as_query_clause(end_second_month, end_third_month)

    first_month_stories = collect_stories(ms_us_query, first_month)
    second_month_stories = collect_stories(ms_us_query, second_month)
    third_month_stories = collect_stories(ms_us_query, third_month)
    print('COLLECTED ALL STORIES')

    write_csv(first_month_stories, shooting_name + '_first_month.csv')
    write_csv(second_month_stories, shooting_name + '_second_month.csv')
    write_csv(third_month_stories, shooting_name + '_third_month.csv')
    print('PROCESS COMPLETE')


# Read the personal API key from the .env file
my_mc_api_key = os.getenv('MC_API_KEY')

# Check that the key works with mediacloud
mc = mediacloud.api.MediaCloud(my_mc_api_key)
print('MEDIACLOUD VERSION:', mediacloud.__version__)

# make sure your connection and API key work by asking for the high-level system statistics
a = time.time()
mc.stats()
b = time.time()
print('CONNECTION CHECK:', b - a)

## ROUND ONE
# collection_pipeline(2013,9,16, 'DC') # DC
# collection_pipeline(2015, 8, 8, 'Houston') # Houston
# collection_pipeline(2017, 9, 10, 'Plano') # Plano
# collection_pipeline(2017, 10, 1, 'Vegas') # Vegas

## ROUND TWO
# collection_pipeline(2017, 5, 27, 'Bogue') # Bogue Chito
# collection_pipeline(2021, 3, 22, 'Boulder')
# collection_pipeline(2019, 8, 31, 'Odessa')
# collection_pipeline(2015, 12, 2, 'SanBernadino')

## ROUND THREE
# collection_pipeline(2018, 10, 27, 'Pittsburgh')
# collection_pipeline(2019, 5, 31, 'VirginiaBeach')