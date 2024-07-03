
from urlextract import URLExtract
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud,STOPWORDS
from collections import Counter
import pandas as pd
analyzer = SentimentIntensityAnalyzer()

extractor=URLExtract()

def show_statistic(selected_user,df):

    if(selected_user!='Overall Analysis'):
        df=df[df['users']==selected_user]

    total_msg=df.shape[0]
    words = []
    for word in df['message']:
        words.extend(word.split())

    total_media=df[df['message']=='<Media omitted>\n'].shape[0]

    links=[]
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))

    return total_msg,len(words),total_media,len(links)




def most_busy_users(df):
    x=df['users'].value_counts().head()
    df=round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={
        "users":"name","count":"percent"
    })
    return x,df

def calculate_sentiment(messages,df):
    positive=0
    negative=0

    for message in messages:
        score=analyzer.polarity_scores(message)
        if score['compound']>=0.05:
            positive+=1

        elif score['compound']<=-0.05:
            negative+=1

        total=positive+negative

    return (positive/total)*100 if total!=0 else 0,(negative/total)*100 if total!=0 else 0



def create_cloud(selected_user, df):
    with open('stopwords.txt') as f:
        custom_stopwords = set(f.read().split())

    if selected_user != 'Overall Analysis':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in custom_stopwords:
                words.append(word)

    word_string = ' '.join(words)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black', stopwords=STOPWORDS.union(custom_stopwords))
    df_wc = wc.generate(word_string)
    return df_wc



def most_common_words(selected_user,df):
    f=open('stopwords.txt')
    stopwords=f.read()


    if selected_user!='Overall Analysis':
        df=df[df['users']==selected_user]

    temp=df[df['users']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    word_df=pd.DataFrame(Counter(words).most_common(20))
    return word_df


def timelime_stats(selected_user,df):
    if selected_user!='Overall Analysis':
        df=df[df['users']==selected_user]

    timeline=df.groupby(['year','month_number','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] +"-"+ str(timeline['year'][i]))

    timeline['time'] = time
    return timeline



def timeline_daily(selected_user,df):
    if selected_user!='Overall Analysis':
        df=df[df['users']==selected_user]

    timeline=df.groupby('date_only').count()['message'].reset_index()


    return timeline


def week_activity(selected_user,df):
    if selected_user!='Overall Analysis':
        df=df[df['users']==selected_user]

    return df['day_name'].value_counts()

def month_activity(selected_user,df):
    if selected_user!='Overall Analysis':
        df=df[df['users']==selected_user]

    return df['month'].value_counts()


def heatmap(selected_user,df):
    if selected_user != 'Overall Analysis':
        df = df[df['users'] == selected_user]

    activity_heatmap=df.pivot_table(index='day_name',columns='period',values='message'
                                    ,aggfunc='count').fillna(0)

    return activity_heatmap