from dotenv import load_dotenv

print(load_dotenv())
# Imports
import datetime
import All_Functions as af
import os
import mediacloud.api
import time
import csv

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

def collect_from_collection(collection_id:str, csv_name):
    query = '" " and tags_id_media:'+collection_id
    for x in range(2014,2021):
        print('Starting',x)
        time_range = mc.dates_as_query_clause(datetime.date(x,6,1), datetime.date(x,6,2))
        all_stories = af.all_matching_stories(mc, query, time_range)

        for s in all_stories:
            # see the "language" notebook for more details on themes
            theme_tag_names = ','.join([t['tag'] for t in s['story_tags'] if t['tag_sets_id'] == mediacloud.tags.TAG_SET_NYT_THEMES])
            s['themes'] = theme_tag_names
        # now write the CSV

        fieldnames = ['publish_date', 'language', 'ap_syndicated', 'media_id', 'media_name', 'media_url']
        with open(csv_name+str(x)+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for s in all_stories:
                writer.writerow(s)


def combine_leanings_csvs(csv_name):
    center_left_2012 = af.import_csv(csv_name + '-2012.csv')
    center_left_2013 = af.import_csv(csv_name + '-2013.csv')
    center_left_2014 = af.import_csv(csv_name + '-2014.csv')
    center_left_2015 = af.import_csv(csv_name + '-2015.csv')
    center_left_2016 = af.import_csv(csv_name + '-2016.csv')
    center_left_2017 = af.import_csv(csv_name + '-2017.csv')
    center_left_2018 = af.import_csv(csv_name + '-2018.csv')
    center_left_2019 = af.import_csv(csv_name + '-2019.csv')
    center_left_2020 = af.import_csv(csv_name + '-2020.csv')

    center_left_names = []
    leanings_list = [['Leaning', 'Media name', 'Media url', 'Media Id']]
    count = 0
    for row in center_left_2012:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the first round')

    count = 0
    center_left_names = []
    for row in center_left_2013:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the second round')

    count = 0
    center_left_names = []
    for row in center_left_2014:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the second round')

    count = 0
    center_left_names = []
    for row in center_left_2015:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the second round')

    count = 0
    center_left_names = []
    for row in center_left_2016:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the second round')

    count = 0
    center_left_names = []
    for row in center_left_2017:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the second round')

    count = 0
    center_left_names = []
    for row in center_left_2018:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the second round')

    count = 0
    center_left_names = []
    for row in center_left_2019:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the second round')

    count = 0
    center_left_names = []
    for row in center_left_2020:
        if row[-1] not in center_left_names:
            count += 1
            leanings_list.append([csv_name, row[-2], row[-1], row[-3]])
            center_left_names.append(row[-1])
    print(f'There are {count} new newspapers in the second round')

    print(len(leanings_list))
    import csv
    # af.export_nested_list('center-left.csv', leanings_list)
    with open(csv_name + '.csv', 'w', newline='', encoding='utf-8') as csvfile:  # open csv file
        writer = csv.writer(csvfile)
        for row in leanings_list:
            writer.writerow(row)

center_left_id = '200363048'
center_right_id ='200363062'
center_id = '200363050'
right_id = '200363049'
left_id = '200363061'


## RIGHT
# collect_from_collection(right_id, 'right-')
# combine_leanings_csvs('right')

## LEFT
# collect_from_collection(left_id, 'left-')
# combine_leanings_csvs('left')

## CENTER RIGHT
# collect_from_collection(center_right_id, 'center-right-')
# combine_leanings_csvs('center-right')

## CENTER
collect_from_collection(center_id, 'center-')
combine_leanings_csvs('center')
