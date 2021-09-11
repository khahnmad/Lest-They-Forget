# IMPORTS
import All_Functions as af
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import random

# the keywords for each shooting
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
def manualCheck(shooting_list, keywords, relevant):
    two_percent = len(shooting_list) * 0.02

    validation = [2 for x in range(len(shooting_list))]

    sample = random.sample(range(1, len(shooting_list)), int(two_percent))
    for i in sample:
        print(shooting_list[1][-1])  # location
        print(shooting_list[i][1])  # url
        print(keywords[i])  # keywords

        reply = input()  # get input

        if reply == 'y':
            print(f'article IS related to this shooting')
            if relevant[i] == 1:
                validation[i] = 1  # 1 means correct
            elif relevant[i] == 0:
                validation[i] = 0  # 0 in the validation list means incorrect
        if reply == 'n':
            print('not related')
            if relevant[i] == 1:
                validation[i] = 0
            elif relevant[i] == 0:
                validation[i] = 1

    # Count the number of errors
    errors = []
    for i in range(len(validation)):
        if validation[i] == 0:
            errors.append(i)
    print(f"There were {len(errors)} errors, {len(errors)/two_percent}")
    for index in errors:
        print(relevant[index])
        print(shooting_list[index][1])  # url
        print(keywords[index])  # keywords
    print('--BREAK--')


def get_numb_articles(shooting_list):
    """ INPUT: a list of lists where each sublist is an article w/ corresponding data from a given shooting
        ASSUMPTIONS: We're asserting that if an article contains more than 3 keywords, the article is *about* the
        shooting
        OUTPUT: a list of the shooting we're talking about, the # of articles about the shooting, the total # of
        articles in the dataset, the avg word count of the relevant articles
    """
    # Initialize variables
    count = [0 for x in range(len(shooting_list))]  # set up an index to keep track of when/ how many keywords appear
    keywords = [[] for x in range(len(shooting_list))] # for the keywords detected
    location = shooting_list[1][-1]  # the "name" of the shooting which links to the dictionary
    relevant = [0 for x in range(len(shooting_list))] # for labeling as "relevant" or not

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
        if len(keywords[i]) > 3: # ASSUMPTION: at least 2
            word = keywords[i][0]
            length = len(keywords[i])
            hypothetical = [word]*length
            if hypothetical != keywords[i]: # ASSUMPTION: must be more than 1 unique word
                relevant[i] = 1

    # manualCheck(shooting_list, keywords, relevant)

    # # Make csv files real quick
    # shooting_list[0].append("Relevancy")
    # for i in range(1, len(shooting_list)):
    #     shooting_list[i].append(relevant[i])
    # af.export_nested_list(location+'_relevancy.csv', shooting_list)

    # Count number of relevant articles
    relevant_articles = 0
    for x in relevant:
        relevant_articles += x

    # Find the average word count of the relevant articles
    word_counts = []
    for j in range(len(shooting_list)):
        if relevant[j] == 1:
            word_counts.append(len(shooting_list[j][2].split()))
    if sum(word_counts) > 0:
        avg_wc = sum(word_counts) / len(word_counts)
    else:
        avg_wc = 0

    return [location, relevant_articles, len(shooting_list), avg_wc]

# ACTION
# Get all the version 2 text files
all_files = [x for x in glob.glob('newspaper-text' + "/*.csv") if "v2" in x]
all_text = af.import_text_data(all_files)


# Find the number of relevant articles in each dataset
article_freq = [['City Or County','# Articles','Total Articles','Avg Word Count']]
for article in all_text:
    article_freq.append(get_numb_articles(article))



# Change the names of the locations so that it will fit with the "City Or County" category in the shooting database
cityorcounty =['Bogue Chitto', 'Boulder', 'Washington Navy Yard', 'Houston',  'Odessa', 'Pittsburgh',
 'Plano', 'San Bernardino','Las Vegas', 'Virginia Beach']

for i in range(1,len(article_freq)):
    article_freq[i][0] = cityorcounty[i-1]

# import the shootings information
sampled_shootings = af.import_csv('v2-sampled_shootings.csv')
# sampled_shootings: list of 11, in which each list has 18 elts

# merge the datasets
for i in range(len(sampled_shootings)):
    for j in range(len(article_freq)):
        if sampled_shootings[i][0] == article_freq[j][0]: # if the location from ss == location from art_freq
            sampled_shootings[i].append(article_freq[j][1])
            sampled_shootings[i].append(article_freq[j][2])
            sampled_shootings[i].append(article_freq[j][3])

# Plot the collected information
## Bar plot of the number of articles for each shooting
fig, ax = plt.subplots()
ax.set_ylabel('Number of Articles')
ax.set_title("Number of Articles about each Shooting")
pps = ax.bar(x=[sampled_shootings[i][0] for i in range(1, len(sampled_shootings))], height=[float(sampled_shootings[i][1]) for i in range(1,len(sampled_shootings))])
for p in pps:
   height = p.get_height()
   ax.annotate('{}'.format(height),
      xy=(p.get_x() + p.get_width() / 2, height),
      xytext=(0, 3), # 3 points vertical offset
      textcoords="offset points",
      ha='center', va='bottom')
plt.show()


## Barplot of the Average Word Count for each Shooting
fig, ax = plt.subplots()
ax.set_ylabel('Average Word Count')
ax.set_title("Average Word Count of Articles about each Shooting")
pps = ax.bar(x=[sampled_shootings[i][0] for i in range(1, len(sampled_shootings))], height=[float(sampled_shootings[i][3]) for i in range(1,len(sampled_shootings))])
for p in pps:
   height = p.get_height()
   ax.annotate('{}'.format(height),
      xy=(p.get_x() + p.get_width() / 2, height),
      xytext=(0, 3), # 3 points vertical offset
      textcoords="offset points",
      ha='center', va='bottom')
plt.show()

## Scatterplot of the Number of Articles by the Number of fatalities
y = [y[18] for y in sampled_shootings[1:]] # number of articles
x = [int(x[8]) for x in sampled_shootings[1:]] # number killed
labels = [y[0] for y in sampled_shootings[1:]] # labels

X = np.array(x).reshape(-1, 1)
reg = LinearRegression().fit(X, y)
art_killed_score = reg.score(X,y)

lr_x = x
lr_y = reg.predict(np.array(X))

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.plot(lr_x, lr_y)
ax.set_title("Shootings' Number of Articles and Number of Fatalities")
ax.set_ylabel('# of Articles about the Shooting')
ax.set_xlabel('# of Fatalities')
for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))
plt.show()



## Scatter plot of the avg word count by the number of fatalities
y = [y[-1] for y in sampled_shootings[1:]] # avg word count
x = [int(x[8]) for x in sampled_shootings[1:]] # number of fatalities
labels = [y[0] for y in sampled_shootings[1:]]

X = np.array(x).reshape(-1, 1)
reg = LinearRegression().fit(X, y)

lr_x = x
lr_y = reg.predict(np.array(X))
wc_killed_score = reg.score(X,y)
fig, ax = plt.subplots()
ax.scatter(x, y)
ax.plot(lr_x, lr_y)
ax.set_title("Shootings' Average Word Count and Number of Fatalities")
ax.set_ylabel('# of Fatalities')
ax.set_xlabel('Average Word Count')
for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))
plt.show()

## Scatterplot of Number of articles by Number of fatalities w/o Vegas
y = [y[18] for y in sampled_shootings[1:] if y[0]!='Las Vegas'] # number of articles
x = [int(x[8]) for x in sampled_shootings[1:] if x[0]!='Las Vegas'] # number of fatalities
labels = [y[0] for y in sampled_shootings[1:]if y[0]!='Las Vegas'] # labels

X = np.array(x).reshape(-1, 1)
reg = LinearRegression().fit(X, y)
art_killed_score_wg_vegas = reg.score(X,y)
lr_x = x
lr_y = reg.predict(np.array(X))

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.plot(lr_x, lr_y)
ax.set_title("Shootings' Number of Articles and Number of Fatalities")
ax.set_ylabel('# of Articles')
ax.set_xlabel('# of Fatalities')
for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))
plt.show()


# Scatterplot of the avg word count by the number of fatalities w/o Vegas
y = [y[-1] for y in sampled_shootings[1:]if y[0]!='Las Vegas'] # avg word count
x = [int(x[8]) for x in sampled_shootings[1:]if x[0]!='Las Vegas'] # killed
labels = [y[0] for y in sampled_shootings[1:]if y[0]!='Las Vegas']

X = np.array(x).reshape(-1, 1)
reg = LinearRegression().fit(X, y)
wc_killed_score_wo_vegas = reg.score(X,y)
lr_x = x
lr_y = reg.predict(np.array(X))

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.plot(lr_x, lr_y)
ax.set_title("Shootings' Average Word Count and Number of Fatalities")
ax.set_ylabel('Average Word Count')
ax.set_xlabel('# of Fatalities')
for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))
plt.show()


# Create the Regression Table
columns = ['# Articles','Avg Word Count','Shooting Name Sum', 'Shooting Sum','Shooter Name Sum','# Killed', '# Injured','Gender of Killed',  'Avg Age of Killed', 'Majority racialized victims','Shooter Age']

# get the index numbers for each of the columns we're interested in
column_numbers = [x for x in range(len(sampled_shootings[0])) if sampled_shootings[0][x] in columns]

# put the numbers we're interested in in one list: regression_list
regression_list = []
for i in range(len(sampled_shootings)):
    relevant = []
    for j in column_numbers:
        relevant.append(sampled_shootings[i][j])
    regression_list.append(relevant)
regression_prep = pd.DataFrame(columns=regression_list[0], data=regression_list[1:])

df = pd.DataFrame(columns=['# Articles','Avg Word Count','Shooting Name Sum', 'Shooting Sum','Shooter Name Sum',
                           '# Killed', '# Injured','Gender of Killed',  'Avg Age of Killed',
                           'Majority racialized victims','Shooter Age'])
for column in columns:
    for copy in columns[:]:
        h=regression_prep[copy]
        j=regression_prep[column]
        lr= af.get_lr(regression_prep[column], regression_prep[copy])
        df.loc[copy, column] = lr

# Save data as csv file
df.to_csv('results/linear-regression-frequency-variables.csv')
af.export_nested_list('results/freq-sampled-shootings.csv', sampled_shootings)

# Print coefficients
print(f"# Articles/ # Killed: {art_killed_score}")
print(f"Avg wc/ # Killed: {wc_killed_score}")
print(f"# Articles/ # Killed W/o vegas: {art_killed_score_wg_vegas}")
print(f"Avg wc/ # Killed W/o vegas: {wc_killed_score_wo_vegas}")