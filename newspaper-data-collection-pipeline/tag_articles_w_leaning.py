"""
This py file takes each of the csv files with article text and appends a new column "leaning" with the partisan leaning
of the paper that the article comes from. It then writes a new csv file with 'v2-' attached to the beginning with the
new info
"""
# IMPORTS
import glob
import All_Functions as af
import sys
import csv

# Import all the leanings files
all_leanings = glob.glob('newspaper-leanings' + "/*.csv")
combined_leanings = [['Leaning','Media name','Media url','Media Id']]
for filename in all_leanings:
    single_file = af.import_csv(filename)
    for row in single_file[1:]:
        combined_leanings.append(row)

# Get rid of duplicates in the leanings files
cleaned_leanings =[]
for i in range(len(combined_leanings)):
    if combined_leanings[i] not in cleaned_leanings:
        cleaned_leanings.append(combined_leanings[i])

# Resolves the huge fields error that you get from importing some of the csv files
maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

# Tag each article in each directory
all_text = glob.glob('newspaper-text' + "/*.csv")
print(f'There are {len(all_text)} csv files being examined')
tagged_text = []
for filename in all_text:
    text_list = af.import_csv(filename)
    print(f'Checking out {filename} which has {len(text_list)-1} articles')
    for i in range(1,len(text_list)):
        for j in range(len(cleaned_leanings)):
            if text_list[i][7] == cleaned_leanings[j][3]:
                text_list[i].append(cleaned_leanings[j][0])
    print(f'Text list size: {len(text_list)}')
    text_list[0].append('Leaning')
    tagged_text.append(text_list)
    print(f'Tagged text size: {len(tagged_text)}')

#check to see if all the articles have been tagged
untagged_newspapers = []
another_version = []
for file in tagged_text:
    for article in file:
        if '.' in article[-1] and article[-1] not in untagged_newspapers:
            untagged_newspapers.append(article[-1])
print('Untagged newspapers:')
print(len(untagged_newspapers))
print(untagged_newspapers)

# rewrite the csv files
for i in range(len(tagged_text)):
    af.export_nested_list('v2-'+all_text[i][15:],tagged_text[i])