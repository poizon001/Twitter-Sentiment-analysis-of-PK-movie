import json
import pandas as pd
import matplotlib.pyplot as plt
import re

# tweets_data_path = 'output_short.json'
tweets_data_path = 'twitterdata.txt'
sentiment_data_path = 'AFINN-111.txt' #2477 words have score between -5 to +5

def get_tweet_list_dict():  
    twitter_list_dict = []
    twitterfile = open(tweets_data_path)
    for line in twitterfile:
    	#twitter_list_dict.append(json.loads(line.decode('utf-8-sig')))
    	try:
    		tweet = json.loads(line)
    		twitter_list_dict.append(tweet)
    	except Exception, e:
    		continue
        
    return twitter_list_dict
 
def get_sentiment_wordsdict():
    afinnfile = open(sentiment_data_path)
    scores = {}
    for line in afinnfile:
        term, score  = line.split("\t")   
        scores[term] = float(score)  
       
    return scores 

def getnumberof_posneg(tweets,sentiment):
        # tweets = get_tweet_list_dict()
        # sentiment = get_sentiment_wordsdict()
        n_pos = 0
        n_neg = 0
        for index in range(len(tweets)):
                tweet_words = tweets[index]["text"].split()
                sent_score = 0
                for word in tweet_words:
                        word = word.rstrip('?:!.,;"!@')
                        word = word.replace("\n", "")
                        
                        if not (word.encode('utf-8', 'ignore') == ""):
                            if word.encode('utf-8') in sentiment.keys():
                                sent_score = sent_score + float(sentiment[word.encode('utf-8','ignore')])
                            else:
                                sent_score = sent_score
                        else:
                            continue

                # print index,sent_score
                if sent_score >= 0.0:
                    n_pos = n_pos + 1
                else:
                    n_neg = n_neg + 1

        return n_pos,n_neg

def getsentiment(tweet,sentiment):

    tweet_words = tweet["text"].split()
    sent_score = 0
    for word in tweet_words:
        word = word.rstrip('?:!.,;"!@')
        word = word.replace("\n", "")
        # print word
        if not (word.encode('utf-8', 'ignore') == ""):
            if word.encode('utf-8') in sentiment.keys():
                sent_score = sent_score + float(sentiment[word])
            else:
                sent_score = sent_score 

	if sent_score >= 0:
		return "happy"
	else:
		return "sad"

def getdataframe(tweets_data,sentiment_data):

    	tweets = pd.DataFrame()
    	tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
    	tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
    	tweets['date'] = map(lambda tweet: tweet['created_at'], tweets_data)
    	tweets['fav']  = map(lambda tweet: tweet['favorite_count'], tweets_data)
    	tweets['rtc']  = map(lambda tweet: tweet['retweet_count'], tweets_data)
    	tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None  and tweet['place']['country'] != None else None, tweets_data)
    	tweets['sentiment'] = map(lambda tweet: getsentiment(tweet, sentiment_data), tweets_data)
        return tweets 

def plotbarcharts(df,label,colname):
    tweets_by_label = df[colname].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel(label, fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title( label, fontsize=15, fontweight='bold')
    if label == 'sentiment':
        tweets_by_label[:2].plot(ax=ax, kind='bar', color='red')
    else:    
        tweets_by_label[:5].plot(ax=ax, kind='bar', color='red')
    plt.show()

def piechart(labels,data):
    fig=plt.figure(figsize=(5,5))
    plt.pie(data,labels=labels,autopct='%1.2f%%')
    plt.show()

# if __name__ == '__main__':
tweets_data = get_tweet_list_dict()
sentiment_data = get_sentiment_wordsdict()
# print getsentiment(tweets_data[1], sentiment_data)
df = getdataframe(tweets_data, sentiment_data)
#trends
plotbarcharts(df,'Languages','lang')
plotbarcharts(df,'Countries','country')
plotbarcharts(df,'Sentiments','sentiment')
n_pos,n_neg = getnumberof_posneg(tweets_data, sentiment_data)
# print n_pos
# print n_neg
piechart(['happy','sad'],[n_pos,n_neg])
# tweets_by_label = df['lang'].value_counts()
# piechart(['happy','sad'],tweets_by_label[0:5])

# print 
# print pd.to_datetime(df['date'])


