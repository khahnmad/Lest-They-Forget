# Imports
import All_Functions as af

# Functions
def sort_dates(shooting):
    numbers = [x[2] for x in shooting]
    numbers.sort()
    new = []
    for item in numbers:
        for elt in shooting:
            if item == elt[2]:
                new.append(elt)
    print(len(new)) # debugging
    return new

def meets_percent_at(value):
    ninety_percents = [int(total_articles[i] * value) for i in range(len(total_articles))]
    meets_ninety_at = []
    for i in range(len(shooting_names)):
        if shooting_names[i] == 'Bogue':
            meets_ninety_at.append(0)
        else:
            shooting = [x for x in sorted_intensity if x[1]==shooting_names[i]]
            for j in range(len(shooting)):
                if j > 0:
                    if ninety_percents[i] - shooting[j-1][-1] >0 and  ninety_percents[i] - shooting[j][-1] <=0:
                        shooting_meets_ninety_at = shooting[j][2]
                        meets_ninety_at.append(shooting_meets_ninety_at)
    for i in range(len(shooting_names)):
        print(f"{shooting_names[i]}: {meets_ninety_at[i]}")


# Import data
intensity = af.import_csv('results/intensity_data.csv')

# Action
# make the relevant data into integers
for i in range(1,len(intensity)):
    days_passed = int(intensity[i][2])
    articles = int(intensity[i][3])
    intensity[i][2] = days_passed
    intensity[i][3] = articles

# Get the total number of articles for each shooting
shooting_names = []
total_articles = [0 for x in range(10)]

for i in range(1,len(intensity)):
    if intensity[i][1] not in shooting_names:
        shooting_names.append(intensity[i][1])
    for j in range(len(shooting_names)):
        if intensity[i][1] == shooting_names[j]:
            total_articles[j] += intensity[i][3]

# How many occur in the first x days?
first_five = [0 for x in range(len(shooting_names))]
for i in range(1,len(intensity)):

    for j in range(len(shooting_names)):
        if intensity[i][1] == shooting_names[j] and intensity[i][2] <= 20:
            first_five[j] += intensity[i][3]

# percent of articles in the first x days
all_first_five = 0
total_total_articles = 0
for i in range(len(shooting_names)):
    if total_articles[i] > 0:
        print(f"{shooting_names[i]}: {(first_five[i]/total_articles[i])*100}% of articles after the first ten days")
        all_first_five+= first_five[i]
        total_total_articles += total_articles[i]
print(f'TOTAL: {(all_first_five/total_total_articles)*100}% ')

# For each shooting, at what day have 90% of the articles been published?
# have to first sort each shooting so that the days_passed numbers are in order
sorted_intensity = []
for i in range(len(shooting_names)):
    shooting = [x for x in intensity if x[1]==shooting_names[i]]
    sorted_shooting = sort_dates(shooting)
    for item in sorted_shooting:
        sorted_intensity.append(item)

for i in range(len(shooting_names)):
    article_count = 0
    for j in range(len(sorted_intensity)):
        if sorted_intensity[j][1] == shooting_names[i]:
            article_count += sorted_intensity[j][-1]
            sorted_intensity[j].append(article_count)

meets_percent_at(0.85)
