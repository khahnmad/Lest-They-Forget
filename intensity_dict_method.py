# IMPORTS
import All_Functions as af
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from datetime import datetime, timedelta


# VARIABLES
shooting_keywords = {'Plano':["spencer hight","dallas cowboys","meredith","dallas","plano","caleb edwards","deffner",
                              "rushin",'hight','husband killed wife','estranged wife','eight people',
                              'football-watching party'],
                     'Pittsburgh':["pittsburgh","synagogue","bowers","tree life","squirrel hill","jewish",
                                   "anti-semitism","jews",'11 people','anti-Semitism','11 dead','anti-semitic'],
                     'Vegas':["paddock","mandalay bay","route 91 harvest","las vegas","aldean","concert","mesquite",
                              "hotel","lombardo",'country music event','music festival','64-year-old man','58 people',
                              '500 injured','killed 58','500 injured','59 people','injured 500','59 deaths','58 dead'],
                     'SanBernadino':['syed','rizwan','farook','tashfeen','malik','SUV',"inland regional center",
                                     "san bernardino","redlands","christmas party","public health department","bomb",
                                     '14 people','14 injured','14 lives','fourteen people','multiple shooters','gunmen',
                                     '14 dead','14 victims','developmental disabilities','disabled','17 injured',
                                     'san bernadino','public facility','sheriff deputy','muslim','islamic'],
                     'Houston':['conley','harris county','ex-girlfriend','houston','saturday','valerie jackson','window'],
                     'Odessa':['saturday','midland','odessa','seth','aaron','ator','west texas','traffic stop',
                               'white van','movie theater','random','5 people','21 injured','zack owens','rifle',
                               'midland-odessa','seven people','eight deaths'],
                     'Bogue':['lincoln county','brookhaven','killed eight people','2017 mississippi'],
                     'DC':['washington navy yard','alexis','monday','contractor','12 people','navy yard',
                           'military facility','armed military','12 victims','13 dead'],
                     'Boulder':['king soopers','boulder','ahmad al','aliwi','al-issa','alissa','arrested','9mm handgun',
                                'table mesa drive','eric talley','boulder police','in custody','ten people','10 people',
                                'grocery store','21-year-old','10 dead'],
                     'VirginiaBeach':['virginia beach','dewayne','craddock','employee','nettleton','.45-caliber',
                                      'engineer','municipal','11 people','12 people','cervera','police chief',
                                      '.45 handgun','12 dead']
                    }


# FUNCTIONS
def get_date_numbers(shooting):
    """
    :param shooting: takes a list of lists in which each sublist is an article and the big list is one shooting
    output: adds a 5-day interval range to the end of each article, indicating at which point in the the 3-month period
    the article was written
    """
    # FIRST: find the earliest date in the dataset - this is the day the shooting took place
    just_dates = [x[4] for x in shooting] # list of just the dates - [4] is the date index
    # convert to datetime so we can compare
    dates_list = []
    for i in range(len(just_dates)):
        if len(just_dates[i]) == 26: # this is for the cases where there are 7 random numbers at the end of the date
            fixed = just_dates[i][:-7]
            date_obj = datetime.strptime(fixed, "%Y-%m-%d %H:%M:%S").date()
            dates_list.append(date_obj)
        if len(just_dates[i]) == 0: # this is for the cases where there is no date information
            dates_list.append(dates_list[i-1])
        if len(just_dates[i])==19: # this is for the "normal" cases
            date_obj = datetime.strptime(just_dates[i], "%Y-%m-%d %H:%M:%S").date()
            dates_list.append(date_obj)
    oldest = min(dates_list)

    # SECOND: append the number of days passed to each of the individual shooting articles
    for i in range(len(shooting)):
        if len(shooting[i][4]) == 19:
            datetime_vers = datetime.strptime(shooting[i][4], "%Y-%m-%d %H:%M:%S").date()
            days_passed = datetime_vers - oldest
            shooting[i].append(days_passed)
        elif len(shooting[i][4])==0:
            shooting[i].append(shooting[i-1][-1])
        else:
            date = shooting[i][4][:-7]
            datetime_vers = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
            days_passed = datetime_vers - oldest
            shooting[i].append(days_passed)

def get_numb_articles(shooting_list):
    """ INPUT: a list of lists where each sublist is an article w/ corresponding data from a given shooting
        ASSUMPTIONS: We're asserting that if an article contains more than 3 keywords, the article is *about* the shooting
        OUTPUT: a list of the shooting we're talking about, the # of articles about the shooting, the total # of articles in the dataset
    """
    # Initialize variables
    count = [0 for x in range(len(shooting_list))]  # set up an index to keep track of when/ how many keywords appear
    keywords = [[] for x in range(len(shooting_list))]  # for the keywords detected
    location = shooting_list[1][-1]  # the "name" of the shooting which links to the dictionary
    relevant = [0 for x in range(len(shooting_list))]  # for labeling as "relevant" or not

    # Identify keywords from the relevant dictionary for each article
    for i in range(len(shooting_list)):
        for word in shooting_list[i][2].split():  # for single words in the dict
            if word in shooting_keywords[location]:
                count[i] += 1
                keywords[i].append(word)
        for word in af.extract_ngrams(shooting_list[i][2].split(), 2):  # for bigrams in the dict
            if word in shooting_keywords[location]:
                count[i] += 1
                keywords[i].append(word)
        for word in af.extract_ngrams(shooting_list[i][2].split(), 3):  # for trigrams in the dict
            if word in shooting_keywords[location]:
                count[i] += 1
                keywords[i].append(word)
        # Identify if the number of keywords (at least 3) and the diversity of vocab (can't all be the same word) is
        #       enough to designate the article as relevant
    for i in range(len(shooting_list)):
        if len(keywords[i]) > 3:  # ASSUMPTION: at least 2
            word = keywords[i][0]
            length = len(keywords[i])
            hypothetical = [word] * length
            if hypothetical != keywords[i]:  # ASSUMPTION: must be more than 1 unique word
                # shooting_list[i].append(len(keywords[i]))
                shooting_list[i].append(keywords[i])
            else:
                # shooting_list[i].append(0)
                shooting_list[i].append([])
        else:
            # shooting_list[i].append(0)
            shooting_list[i].append([])

    # for index in range(len(shooting_list)): # I THINK THIS CAN BE DELeted
    #     shooting_list[index].append(count[index])
    # here is the assumption that if there are 3 keywords in the article, the article is about the shooting
    # subset = [article for article in shooting_list if article[-1]>0]
    subset = [article for article in shooting_list if len(article[-1]) > 0]


    if len(subset) == 0:
        summary = []
        day_ranges = [i for i in range(90)]
        for day in day_ranges:
            summary.append([location, day, 0])
    else:
        get_date_numbers(subset)
        for elt in subset:
            date = elt[-1]
            if len(elt) < 14:
                for i in range(10):
                    if str(date.days)[-1] == '0' or str(date.days)[-1] == '5':
                        if len(elt) == 13:
                            elt.append(date.days)
                    date += timedelta(days=1)
    return subset
    ### HERE'S the normal ending for this function
    #     day_ranges = []
    #     for elt in subset:
    #         if elt[-1] not in day_ranges:
    #             day_ranges.append(elt[-1])
    #
    #     day_count = [0 for x in range(len(day_ranges))]
    #     for elt in subset:
    #         for i in range(len(day_ranges)):
    #             if elt[-1] == day_ranges[i]:
    #                 day_count[i] += 1
    #
    #     summary = []
    #     for i in range(len(day_ranges)):
    #         location = subset[1][10] # double check that this is the right index
    #         summary.append([location, day_ranges[i], day_count[i]])
    #
    # return summary

# GET & CLEAN TEXT FILES
all_files = [x for x in glob.glob('newspaper-text' + "/*.csv") if "v2" in x]
all_text = af.import_text_data(all_files)
for i in range(len(all_text)):
    for j in range(len(all_text[i])):
        if len(all_text[i][j]) == 10:
            all_text[i][j].insert(9, 'No partisan leaning')

# ACTION
intensity_db = [get_numb_articles(shooting) for shooting in all_text]
"""
Query articles in a specific time
"""

for i in range(len(intensity_db)):
    count = 0
    for j in range(len(intensity_db[i])):
        if count < 10:
            if intensity_db[i][j][13] == 20 and intensity_db[i][j][10]=='Plano':
                count += 1
                print(f"LOCATION: {intensity_db[i][j][10]}")
                print(f"URL: {intensity_db[i][j][1]}")
                print(f"KEYWORDS:{intensity_db[i][j][11]}")



#
# # Visualize the data
#
# unnested = []
# for x in intensity_db:
#     for y in x:
#         unnested.append(y)
#
#
# summary_df = pd.DataFrame(data=unnested, columns=['Location','Days Passed','# Articles'])
# # plt.figure(figsize=(20, 10))
# sns.lineplot(data=summary_df, x="Days Passed", y='# Articles',hue='Location').set_title('Intensity of coverage')
# plt.show()
#
# # Without Las Vegas
# wo_vegas = [x for x in unnested if x[0] !='Vegas']
# wo_vegas_df = pd.DataFrame(data=wo_vegas, columns=['Location','Days Passed','# Articles'])
# # plt.figure(figsize=(20, 10))
# sns.lineplot(data=wo_vegas_df, x="Days Passed", y='# Articles',hue='Location').set_title('Intensity of coverage - '
#                                                                                          'without Las Vegas')
# plt.show()
#
# # Save data as a csv file
# summary_df.to_csv('results/intensity_data.csv')