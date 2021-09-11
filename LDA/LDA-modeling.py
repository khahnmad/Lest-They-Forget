# Imports
import glob
import All_Functions as af
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import datetime
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
#
# import pyLDAvis
# import pyLDAvis.sklearn
# pyLDAvis.enable_notebook()

# Get all the version 2 text files
all_files = [x for x in glob.glob('relevancy-files' + "/*.csv")]
# all_text = af.import_text_data(all_files)
def convert_to_datetime(shooting):
    for i in range(len(shooting)):

        if type(shooting[i][4]) == float:
            shooting[i][4] = shooting[i - 1][4]
        else:
            if len(shooting[i][4]) == 19:
                datetime_vers = datetime.strptime(shooting[i][4], "%Y-%m-%d %H:%M:%S").date()
                # days_passed = datetime_vers - oldest
                # shooting[i].append(days_passed)
                shooting[i][4] = datetime_vers
            elif len(shooting[i][4])==0:
                # shooting[i].append(shooting[i-1][-1])
                shooting[i][4] = shooting[i-1][4] # filling in missing values with the nearest one
            else:
                date = shooting[i][4][:-7]
                datetime_vers = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
                shooting[i][4] = datetime_vers
                # days_passed = datetime_vers - oldest
                # shooting[i].append(days_passed)

def run_LDA(file):
    df = pd.read_csv(file)
    relevant_df = df[df['Relevancy']==1]
    print(len(relevant_df))
    count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')
    doc_term_matrix = count_vect.fit_transform(relevant_df['text'].values.astype('U'))
    LDA = LatentDirichletAllocation(n_components=4, random_state=42)
    LDA.fit(doc_term_matrix)

    for i, topic in enumerate(LDA.components_):
        print(f'Top 10 words for topic #{i+1}:')
        print([count_vect.get_feature_names()[i] for i in topic.argsort()[-10:]])
        print('\n')

    topic_values = LDA.transform(doc_term_matrix)
    relevant_df['Topic'] = topic_values.argmax(axis=1)

    # pyLDAvis.sklearn.prepare(LDA, doc_term_matrix, count_vect)
    print(relevant_df.keys())
    return relevant_df.values.tolist()

def plot_time_vs_topic(shooting):
    y = [y[4] for y in shooting]  # time
    x = [x[-1] for x in shooting]  # topic
    # labels = [y[0] for y in sampled_shootings[1:] if y[0] in relevant_shooting_names]

    fig, ax = plt.subplots()
    ax.scatter(y, x)
    # ax.set_title(title + ": Frequency of Coverage")
    # ax.set_ylabel('Number of Articles about the Shooting')
    # ax.set_xlabel('Average Word Count')
    # if len(interests) > 1:
    #     for i, txt in enumerate(labels):
    #         if txt in interests:
    #             ax.annotate(txt, (x[i], y[i]), color='red')
    #         else:
    #             ax.annotate(txt, (x[i], y[i]))
    # else:
    #     for i, txt in enumerate(labels):
    #         if txt in interests:
    #             ax.annotate(txt, (x[i], y[i]), color='red')
    #         else:
    #             ax.annotate(txt, (x[i], y[i]))
    plt.show()

def run_whole_thing(file):
    boulder = run_LDA(file)
    print(f"RUNNING {boulder[1][-3]}")
    convert_to_datetime(boulder)
    plot_time_vs_topic(boulder)

for file in all_files[1:]:
    run_whole_thing(file)

#
# virginiabeach = run_LDA(all_files[-1])
# convert_to_datetime(virginiabeach)
# plot_time_vs_topic(virginiabeach)

