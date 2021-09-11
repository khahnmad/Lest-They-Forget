# All imports
import pandas as pd
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import random
import All_Functions as af

# nltk.download('stopwords')
# nltk.download('movie_reviews')
# nltk.download('vader_lexicon')

# Variables
stopwords = stopwords.words('english')


# Functions
def processing_urls_pipeline(csv_file, final_csv_name, sample_size):
    # Import the file
    media_file = af.import_csv(csv_file)
    print('IMPORTED FILE')

    # Get a list of just unique urls
    urls = []
    for i in range(1, len(media_file)):
        if media_file[i][3] not in urls:
            urls.append(media_file[i][3])
    print("Number of articles:", len(urls))

    '''For some reason it gets stuck on certain websites. Couldnt figure out why it gets stuck, so I'm just 
    removing those websites'''
    bad_websites = ['kansascity', 'miamiherald', 'sacbee', 'seattle', 'feeds.reuters', 'cbsnews.com/videos/',
                    'feeds.cbsnews', 'usnews.com', 'ledger-enquirer.com/', 'google.com/~r/bu',
                    'ssfeeds.cincinnati.com/~/468240148', 'work.com/news/native-news/o',
                    'chicagotribune.com/ho', 'newsweek.com/', 'norwichbulletin.com/opin', 'azcentral.com/~/4',
                    'huffingtonpost.com/entry/', 'sfgate.com/', 'washingtonpost.com/', 'aol.com/article/',
                    'huffpost.com/entry/', 'o-got-voted-off-dancing-with-', 'rssfeeds.usatoday.', 'blogs.reuters.com',
                    'ww.policymic.com/ar', 'eds.foxnews.com/~r/blogs', 'st-gazette.com/stories/opinio',
                    '//origin-www.businessweek.com', 'feeds.huffingtonpost.com', '/rssfeeds.cincinnati.com/~/',
                    'p://theweek.com/articles/5', 'feeds.feedblitz.com/~/366051284/',
                    '/rssfeeds.indystar.com/~/649258664'
        , '/upstract.com/p/aie', 'ics.mcclatchyinteractive.com/ne', '/feedproxy.google.com/~r/M',
                    '://videos.mlive.com/mlive/', '/www.espn.com/nfl/story/_/id/254',
                    '/www.npr.org/2018/11/28/671353612','www.npr.org/2018/10/30/662335612/leg',
                    's://www.thedailybeast.com/third-dylann-roof-f', 'ds.feedblitz.com/~/46',
                    'ssfeeds.azcentral.com/~/513474612/', 'eds.jsonline.com/~/464601244/0/milwaukee/news~Bice-',
                    'm/watch-heres-how-late-night-tv-hosts-responded-las-vegas-shooting-259',
                    'm/entertainment/tv/late-night-tv-hosts-decry-las-ve', '://www.tmz.com/2015/10/08/tmz-liv',
                    '//www.tmz.co','w.salon.com/2017/05/30/w','om/~r/dailysourceorg/~3/hc7vttO',
                    'edpress.it/link/9499/12203338','proxy.google.com/~r/Newshou',
                    'w.realclearpolitics.com/articles/2017/10/02/at_l','ilencer-bill-15','www.wsj.com/articles',
                    'rg/newshour/rundown/twitter-chat-gun','rpolitics.com/2017/10/02/039','www.pbs.org/newshou',
                    'www.realclearpolitics.com/articl','.com/mma/story/_/id/20908846/ufc-hea','learpolitics.com/2017',
                    'w.npr.org/2017/1','ribune.com/nation/4490','le.com/country/ch',
                    'n.com/college-football/story/_/id/209','ww.espn.com/nhl/story','itics.com/video/2017/10/02/ra',
                    'www.norwichbulletin.com','/www.cnbc.com/2017/10/04/','salon.com/2017/10/20/nra-',
                    '/www.weeklystandard.com/afternoon-links-millennia','www.salon.com/2017/10/03/h',
                    '/www.salon.com/2017','w.csmonitor.com/USA/Society/2017','/video.cnbc.com/gallery/?video',
                    'www.espn.com/nba/story/_/id/20899','www.espn.com','.cbsnews.com/video/wom',
                    '//www.npr.org/sections/thetwo-way/2017/10/02/555','//www.npr.org/sections/',
                    'tp://feedproxy.google.com/~r/dailysourceorg/~3','/feedproxy.google.com/~r/dailysourceorg/~3/Lb',
                    '/tracking.feedpress.it/link/94','ttp://wonkwire.com/2015/12/17/americans-m',
                    'tp://wonkwire.com/2015/12/','s://www.csmonitor.com/USA/2018/1105/','//www.npr.org/2',
                    '/www.salon.com/2018','tp://transcripts.cnn.com/TRANSCRIPTS/18',
                    '/www.csmonitor.com/USA/Politics/monitor_breakfast/2018/1113/Breakfa',
                    '/www.realclearpolitics.com/video/2018/12/14/rep_l','p://feedproxy.google.com/~r/breitbart/~3/cE',
                    's://www.csmonitor.com/USA','://www.salon.com/2019',
                    '://www.thedailybeast.com/a-simple-plan-to-do-something-ab','ww.realclearpolitics.com/video/2019']
    for url in urls[:]:  # have to make a copy to iterate through in order to remove things correctly
        for bad_website in bad_websites:
            if bad_website in url and url in urls:
                urls.remove(url)
    print('BAD WEBSITES REMOVED')
    print("Number of articles:", len(urls))

    # # Get a random sample of 1000 of the articles
    # list_of_indexes = [x for x in range(len(urls))]
    # random_indexes = random.sample(list_of_indexes, sample_size)
    # sampled_urls = [urls[x] for x in range(len(urls)) if x in random_indexes]
    # print(f'Number of sampled titles: {len(sampled_urls)}')

    # Get the text from each of the urls
    text = af.get_text(urls)
    print('GOT TEXT')

    # Clean the text
    # url_list, cleaned_text = af.clean_text(urls, text)
    print('These urls are not in the cleaned urls list so there must be something wrong with them:')
    # bad_urls = []
    # for url in urls:
    #     if url not in url_list:
    #         print(url)
    #         bad_urls.append(url)
    # af.export_list('BadUrls' + final_csv_name, bad_urls)
    # print('CLEANED TEXT')

    # Do a sentiment analysis
    # sia = SentimentIntensityAnalyzer()
    #
    # sia_sentiment = []
    # for text in cleaned_text:
    #     sia_sentiment.append(sia.polarity_scores(text))
    # print('SENTIMENT ANALYSIS COMPLETE')

    sia_df = pd.DataFrame({'url': urls, 'text': text})

    for i in range(len(media_file)):
        print(f'loading {i}...')
        for index, row in sia_df.iterrows():
            if sia_df.loc[index, 'url'] == media_file[i][3]:
                sia_df.loc[index, 'publish_date'] = media_file[i][1]
                sia_df.loc[index, 'title'] = media_file[i][2]
                sia_df.loc[index, 'themes'] = media_file[i][6]
                sia_df.loc[index, 'media_id'] = media_file[i][7]
                sia_df.loc[index, 'media_url'] = media_file[i][9]

    sia_df.to_csv('unclean' + final_csv_name)
    print('PROCESS COMPLETE')


## ROUND ONE
# processing_urls_pipeline('newspaper-urls\Vegas_first_month', 'Vegas_Text-first-month.csv', 1000)
# processing_urls_pipeline('newspaper-urls\Vegas_second_month', 'Vegas_Text-second-month.csv', 1000)
# processing_urls_pipeline('newspaper-urls\Vegas_third_month', 'Vegas_Text-third-month.csv', 400)

# processing_urls_pipeline('newspaper-urls\DC_first_month', 'DC_Text-first-month.csv', 400)
# processing_urls_pipeline('newspaper-urls\DC_second_month', 'DC_Text-second-month.csv', 68)
# processing_urls_pipeline('newspaper-urls\DC_third_month', 'DC_Text-third-month.csv', 124)

# processing_urls_pipeline('newspaper-urls\Plano_first_month', 'Plano_Text-first-month.csv', 1000)
# processing_urls_pipeline('newspaper-urls\Plano_second_month', 'Plano_Text-second-month.csv', 1000)
# processing_urls_pipeline('newspaper-urls\Plano_third_month', 'Plano_Text-third-month.csv', 400)
# #
# processing_urls_pipeline('newspaper-urls\Houston_first_month', 'Houston_Text-first-month.csv', 149)
# processing_urls_pipeline('newspaper-urls\Houston_second_month', 'Houston_Text-second-month.csv', 843)
# processing_urls_pipeline('newspaper-urls\Houston_third_month', 'Houston_Text-third-month.csv', 472)

## ROUND TWO
# processing_urls_pipeline('newspaper-urls\Bogue_first_month.csv', 'Bogue_Text-first-month.csv', 483)
# processing_urls_pipeline('newspaper-urls\Bogue_second_month.csv', 'Bogue_Text-second-month.csv', 204)
# processing_urls_pipeline('newspaper-urls\Bogue_third_month.csv', 'Bogue_Text-third-month.csv', 120)

# processing_urls_pipeline('newspaper-urls\Boulder_first_month.csv', 'Boulder_Text-first-month.csv', 1000)
# processing_urls_pipeline('newspaper-urls\Boulder_second_month.csv', 'Boulder_Text-second-month.csv', 408)
# processing_urls_pipeline('newspaper-urls\Boulder_third_month.csv', 'Boulder_Text-third-month.csv', 562)

# processing_urls_pipeline('newspaper-urls\Odessa_first_month.csv', 'Odessa_Text-first-month.csv',1000)
# processing_urls_pipeline('newspaper-urls\Odessa_second_month.csv', 'Odessa_Text-second-month.csv',464)
# processing_urls_pipeline('newspaper-urls\Odessa_third_month.csv', 'Odessa_Text-third-month.csv',470)

# processing_urls_pipeline('newspaper-urls\SanBernadino_first_month.csv', 'SanBernadino_Text-first-month.csv',1000)
# processing_urls_pipeline('newspaper-urls\SanBernadino_second_month.csv', 'SanBernadino_Text-second-month.csv',472)
# processing_urls_pipeline('newspaper-urls\SanBernadino_third_month.csv', 'SanBernadino_Text-third-month.csv',398)
#
# ROUND THREE
# processing_urls_pipeline('newspaper-urls\Pittsburgh_first_month.csv', 'Pittsburgh_Text-first-month.csv',1000)
# processing_urls_pipeline('newspaper-urls\Pittsburgh_second_month.csv', 'Pittsburgh_Text-second-month.csv',415)
# processing_urls_pipeline('newspaper-urls\Pittsburgh_third_month.csv', 'Pittsburgh_Text-third-month.csv',317)

# processing_urls_pipeline('newspaper-urls\VirginiaBeach_first_month.csv', 'VirginiaBeach_Text-first-month.csv', 586)
# processing_urls_pipeline('newspaper-urls\VirginiaBeach_second_month.csv', 'VirginiaBeach_Text-second-month.csv', 261)
processing_urls_pipeline('newspaper-urls\VirginiaBeach_third_month.csv', 'VirginiaBeach_Text-third-month.csv', 1000)
