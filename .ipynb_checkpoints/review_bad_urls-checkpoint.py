import csv
import glob
import All_Functions as af

all_text = glob.glob('newspaper-text/bad-urls' + "/*.csv")
# print(len(all_text))
# print(all_text[24])
# csv_file = 'C:\Users\khahn\Documents\SEDS_Seminar\Use-News-Seminar\newspaper-text\bad-urls\BadUrlsBogue_Text-first-month.csv'
# csv_file = all_text[0]
nested_list = []
special_case = []
for i in range(len(all_text)):
    # print(f'csv number {i}')
    if i != 24:
        with open(all_text[i], newline='', encoding='utf-8') as csvfile:  # open csv file
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                # print("     ",len(row))
                for item in row:
                    nested_list.append(item)
                # print(len(nested_list))

cleaned = []
for x in nested_list:
    if x not in cleaned:
        cleaned.append(x)
print(len(cleaned))

websites = []
count = 0
for url in cleaned:
    for i in range(len(url)):
        if url[i-3] == 'c' and url[i-2] == 'o' and url[i-1] == 'm' and url[i]=='/':
        # if url[i-3:i] == 'com/':
            count +=1
            if url[:i+1] not in websites:
                websites.append(url[:i+1])
print(count)
# for x in websites[:25]:
#     print(x)

for x in range(len(cleaned[0])):
    print(f'getting {x}')
    soup = af.make_soup(cleaned[x])
    # if len(soup) > 25:
    #     print(soup)
    print(cleaned[x])
    # print(soup.prettify())
    print(soup.get_text())