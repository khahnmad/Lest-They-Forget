import All_Functions as af
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# try plotting # killed or injured by # killed for each of the variables of interest

"""
Unusual Offenders:
- female offenders
- multiple offenders
- over 35 years old
- black offenders w/ white victims

"worthy" victims:
- white
- rich
- female
- killed by strangers
"""
# create a simmilarity index for each of the shootings?
vict_ds = af.import_csv('victims/sample_victims.csv')
perp_ds = af.import_csv('v2-sampled_shootings.csv')
intensity = af.import_csv('results/intensity_data.csv')

for i in range(len(intensity)):
    if intensity[i][1]=='Bogue':
        intensity[i][1] = 'Bogue Chitto'
    if intensity[i][1]=='DC':
        intensity[i][1] = 'Washington Navy Yard'
    if intensity[i][1]=='SanBernadino':
        intensity[i][1] = 'San Bernardino'
    if intensity[i][1]=='Vegas':
        intensity[i][1] = 'Las Vegas'
    if intensity[i][1]=='VirginiaBeach':
        intensity[i][1] = 'Virginia Beach'
sampled_shootings = af.import_csv('freq-sampled-shootings.csv')

def generate_similarity(inst_a, inst_b):
    # close_in_time = abs(inst_a[5] - inst_b[5])  # double check all these indices
    close_in_time = 0 # filler for now -- not sure if this is a useful datapoint
    if inst_a[6] == inst_b[6]:
        same_state =1
    else:
        same_state = 0
    no_killed = abs(int(inst_a[8])-int(inst_b[8]))
    no_injured = abs(int(inst_a[9])-int(inst_b[9]))
    total_victims = abs((int(inst_a[9])+int(inst_a[8])) -(int(inst_b[9])+int(inst_b[8])))
    if inst_a[10] == inst_b[10]:
        same_location = 1
    else:
        same_location = 0
    gender_killed = abs(float(inst_a[11])-float(inst_b[11]))
    age_killed = abs(float(inst_a[12]) - float(inst_b[12]))
    race_killed = abs(float(inst_a[13]) - float(inst_b[13]))
    shooter_age = abs(float(inst_a[15]) - float(inst_b[15]))
    if inst_a[16] == inst_b[16]:
        same_race = 1
    else:
        same_race = 0
    if inst_a[17] == inst_b[17]:
        same_after = 1
    else:
        same_after = 0
    summary = [close_in_time, same_state, no_killed, no_injured, total_victims, same_location, gender_killed, age_killed,
               race_killed, shooter_age, same_race, same_after]
    importance_vec = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    similarity_count = 0
    for i in range(len(summary)):
        multiply = summary[i]*importance_vec[i]
        similarity_count += multiply
    return similarity_count


def plot_coverage(controls, interests, characteristic):
    graphable = []
    for i in range(len(intensity)):
        if len(interests)>0:
            if intensity[i][1] in interests:
                graphable.append([intensity[i][0], intensity[i][1], int(intensity[i][2]), int(intensity[i][3]),characteristic])
            elif intensity[i][1] in controls and intensity[i][1] not in interests:
                graphable.append([intensity[i][0], intensity[i][1], int(intensity[i][2]), int(intensity[i][3]), 'not '+ characteristic])
        else:
            if interests == intensity[i][1]:
                graphable.append([intensity[i][0], intensity[i][1], int(intensity[i][2]), int(intensity[i][3]),characteristic])
            elif intensity[i][1] in controls and intensity[i][1] != interests:
                graphable.append([intensity[i][0], intensity[i][1], int(intensity[i][2]), int(intensity[i][3]),'not '+characteristic])
    columns = [x for x in intensity[0]]
    columns.append('Variable of Interest')
    df = pd.DataFrame(data=graphable, columns=columns)
    plt.figure(figsize=(20, 10))
    sns.lineplot(data=df, x="Days Passed", y='# Articles', hue='Location', style='Variable of Interest')
    plt.show()

    # Frequency of coverage
    # avg word count by # of articles
    all = [x for x in controls]
    if type(interests)==list:
        for jj in interests:
            all.append(jj)
    else:
        all.append(interests)
    y = [int(y[-3]) for y in sampled_shootings[1:] if y[0] in all]  # of articles
    x = [float(x[-1]) for x in sampled_shootings[1:] if x[0] in all]  # word count
    labels = [y[0] for y in sampled_shootings[1:] if y[0] in all]
    print(len(y)) # debugging

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    # ax.set_title(title + ": Frequency of Coverage")
    ax.set_ylabel('Number of Articles about the Shooting')
    ax.set_xlabel('Average Word Count')
    print(len(interests)) # debugging
    if len(interests) > 1:
        for i, txt in enumerate(labels):
            if txt in interests:
                ax.annotate(txt, (x[i], y[i]), color='red')
            else:
                ax.annotate(txt, (x[i], y[i]))
    else:
        for i, txt in enumerate(labels):
            if txt in interests:
                ax.annotate(txt, (x[i], y[i]), color='red')
            else:
                ax.annotate(txt, (x[i], y[i]))
    plt.show()

def identify_controls(interests):
    controls = []
    if type(interests[0])==list:
        interest_titles = [x[0] for x in interests]
        for interest in interests:
            for i in range(1, len(perp_ds)):
                score = generate_similarity(interest, perp_ds[i])
                if perp_ds[i][0] not in controls and perp_ds[i][0] not in interest_titles and score < 40:
                    controls.append(perp_ds[i][0])
    else:
        for i in range(1, len(perp_ds)):
            score = generate_similarity(interests, perp_ds[i])
            if perp_ds[i][0] not in controls and perp_ds[i][0]!= interests[0] and score < 40:
                controls.append(perp_ds[i][0])
    return controls
#
# # Female offenders
interest = perp_ds[1]
controls = identify_controls(interest)
plot_coverage(controls,interest[0],'Female Offender')

# # Over 35
interests = [perp_ds[2], perp_ds[5],perp_ds[6],perp_ds[9],perp_ds[10]]
controls = identify_controls(interests)
plot_coverage(controls, [x[0] for x in interests],'Over 35')

# Black offenders w white versus black victims
black_shooters =[]
for i in range(len(perp_ds)):
    if perp_ds[i][16]=='black':
        black_shooters.append(perp_ds[i])
w_white_victims =[x[0] for x in black_shooters if x[13]=='0']
plot_coverage([x[0] for x in black_shooters],  w_white_victims,'White Victims')

"""
Now looking at "worthy" victims
"""
# White Victims
interests = [perp_ds[x] for x in range(len(perp_ds)) if perp_ds[x][13]=='0' and perp_ds[x][0]!= 'Vegas']
controls = identify_controls(interests)
plot_coverage([x[0] for x in sampled_shootings[1:] if x[0]!= 'Las Vegas'],
              [x[0] for x in interests],
              'Majority White Victims')

# Cop Victim
interests = [perp_ds[x] for x in range(1,len(perp_ds)) if int(perp_ds[x][-1])>0] # cop victim variable is the last one
controls = identify_controls(interests)
plot_coverage(controls, [x[0] for x in interests], 'Cop as a Victim')


# Female Victims
interests = [perp_ds[x] for x in range(1,len(perp_ds)) if float(perp_ds[x][11])>0.5]
controls = identify_controls(interests)
plot_coverage(controls, [x[0] for x in interests], 'Majority Female Victims')

# Killed by strangers
perp_ds[0].append('Victims knew shooter')
shooter_names = []
for x in range(1,len(vict_ds)):
    if vict_ds[x][1] not in shooter_names:
        shooter_names.append(vict_ds[x][1])
print(len(shooter_names)) # debugging
for name in shooter_names:
    for i in range(len(vict_ds)):
        if vict_ds[i][1] == name:
            knew_shooter = vict_ds[i][7]

    for i in range(len(perp_ds)):
        if name in perp_ds[i][14]:
            perp_ds[i].append(knew_shooter)
print(len(perp_ds)) # debugging

# aaron alexis, paddock
# farook, craddock, david conley ray, spencer hight, godbolt
interests = [perp_ds[1],perp_ds[2],perp_ds[8],perp_ds[9],perp_ds[10]]
controls = identify_controls(interests)
plot_coverage(controls,  [x[0] for x in interests], 'Not Killed by a Stranger')