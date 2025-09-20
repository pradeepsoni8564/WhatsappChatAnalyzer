import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Upload a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    user_list.remove('group_notification')

    selected_user = st.sidebar.selectbox("Show Analysis WRT", user_list)

    if st.sidebar.button("Show analysis"):

        num_messages, num_words, num_media_message , num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statists")
        col1, col2 , col3 , col4  = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_message)

        with col4:
            st.header("links Shared")
            st.title(num_links)

        # monthly timeline

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='brown')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline

        st.title("Daily Timeline")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Active Map")
        col1, col2  = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='Black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Day")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='Orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Timeline")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest users in the group(group level)
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x , new_df= helper.most_busy_users(df)
            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color="Purple")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Wordcloud
        st.title("Wordcloud Analysis")
        df_wc = helper.create_word_cloud(selected_user,df)

        if df_wc is not None:
            fig, ax = plt.subplots()
            ax.imshow(df_wc)  # ✅ safe now, because df_wc is guaranteed not None
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.warning("No messages available to generate WordCloud for this user.")

        # Most common words

        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1],color="Orange")
        plt.xticks(rotation='vertical')

        st.title("Most Common Words")
        st.pyplot(fig)

        st.dataframe(most_common_df)

        # emoji analysis

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
