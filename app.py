import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.sidebar.title('Whatsapp chat analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocess.preprocess_data(data)


    #fetch unique users
    user_list=df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall Analysis',)

    selected_user=st.sidebar.selectbox('Show connections',user_list)
    if(selected_user!='Overall Analysis'):
        st.title(f'Chat Analysis of {selected_user}')
        df = df[df['users'] == selected_user]
    else:
        st.title('Overall Analysis')

    st.dataframe(df)
    if st.sidebar.button('Show Analysis'):
        st.sidebar.text('welcome to chat analyzer')
        num_mesg,total_word,total_media,total_links=helper.show_statistic(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        df = df[df['users'] != 'group_notification']

        with col1:
            st.header('Total Messages')
            st.title(num_mesg)

        with col2:
            st.header('Total words')
            st.title(total_word)
            st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace
            st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace

        with col3:
            st.header('Total media items shared')
            st.title(total_media)
            st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace

        with col4:
            st.header('Total links shared')
            st.title(total_links)
            st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace

        st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace
        st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace


        #monthly timeline
        st.title('Monthly Chart')
        timeline=helper.timelime_stats(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace
        st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace

        #daily timeline
        st.title('Daily Chart')
        timeline = helper.timeline_daily(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['date_only'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #active days in week
        st.title('Weekly Activity')
        col1,col2=st.columns(2)
        with col1:
            st.header('Busy Days')
            timeline = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(timeline.index, timeline.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            # active months in year

            st.header('Busy Months')
            timeline = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(timeline.index, timeline.values, color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title('Heatmap')
        activity_heatmap=helper.heatmap(selected_user,df)
        fig,ax=plt.subplots()
        sns.heatmap(activity_heatmap,ax=ax)
        st.pyplot(fig)

        if selected_user=='Overall Analysis':
                st.title('Most Busy Users')
                x,new_df = helper.most_busy_users(df)
                col1,col2=st.columns(2)
                fig, ax = plt.subplots()


                with col1:
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)




                with col2:
                    st.dataframe(new_df)

                col1, col2 = st.columns(2)
                sentiment_results = {}

                with col1:
                    st.title('User Sentiment Analysis')


                    for user in df['users'].unique():
                        if(user!='Overall Analysis'):

                            user_messages=df[df['users']==user]['message']
                            pos_percent,neg_percent=helper.calculate_sentiment(user_messages,df)
                            sentiment_results[user]={'positive':pos_percent,'negative':neg_percent}

                        #display results
                    sentiment_df = pd.DataFrame(sentiment_results).T
                    sentiment_df = sentiment_df[(sentiment_df.T != 0).any()]  # Drop users with no sentiment scores

                    st.dataframe(sentiment_df)


              #  user_list=list(sentiment_results.keys())[0:5]
            #    positive_per=[sentiment_results[user]['positive'] for user in user_list]

        else:
            with col2:

                usermsg_=df[df['users']==selected_user]['message']
                post,negt=helper.calculate_sentiment(usermsg_,df)
                if post+negt>0:
                    st.markdown("<h3>Sentiment Analysis</h3>", unsafe_allow_html=True)

                    sentiments={'positive':post,'negative':negt}
                    sentiment_labels=list(sentiments.keys())
                    sentiment_val=list(sentiments.values())

                    fig, ax = plt.subplots(figsize=(20, 16))  # Adjust figure size
                    ax.bar(sentiment_labels, sentiment_val, color=['blue', 'salmon'])

                    ax.set_xlabel('Sentiment', fontsize=84)
                    ax.set_ylabel('Percentage', fontsize=84)
                    ax.set_title(f'Analysis of {selected_user}', fontsize=80)
                    plt.xticks(fontsize=82)
                    plt.yticks(fontsize=82)
                    st.pyplot(fig)


        #wordcloud
        df_wc=helper.create_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        ax.set_title(f'Major used words of {selected_user}')
        st.pyplot(fig)

        st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace
        st.markdown('<br><br>', unsafe_allow_html=True)  # Adding whitespace


        col1,col2=st.columns(2)

        #most common words
        with col1:

            most_common=helper.most_common_words(selected_user,df)
            st.title('Most Common Words')
            st.dataframe(most_common)

        with col2:
            fig,ax=plt.subplots()
            ax.bar(most_common[0],most_common[1],color='skyblue')
            ax.set_title('Most Used Words')
            ax.set_xlabel('Words')
            ax.set_ylabel('count')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
