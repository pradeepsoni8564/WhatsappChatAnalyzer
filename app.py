import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for responsive design
st.markdown("""
<style>
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .stColumn {
            padding: 0.5rem 0.25rem !important;
        }
        .stMetric {
            font-size: 0.9rem;
        }
        h1 {
            font-size: 1.8rem !important;
        }
        h2 {
            font-size: 1.4rem !important;
        }
        h3 {
            font-size: 1.2rem !important;
        }
    }

    /* Desktop optimizations */
    @media (min-width: 769px) {
        .main .block-container {
            max-width: 1200px;
            padding: 2rem 1rem;
        }
    }

    /* General improvements */
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title('📱 WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis WRT", user_list)

    if st.sidebar.button("Show Analysis", use_container_width=True):

        # ================= Stats Section =================
        num_messages, num_words, num_media_message, num_links = helper.fetch_stats(selected_user, df)

        st.title("📊 Top Statistics")

        # Responsive columns - 4 on desktop, 2 on mobile
        col1, col2, col3, col4 = st.columns(4)

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
            st.header("Links Shared")
            st.title(num_links)

        st.divider()

        # ================= Timelines =================
        st.header("📅 Timeline Analysis")

        # Monthly Timeline
        st.subheader("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(timeline['time'], timeline['message'], color='brown', linewidth=2)
        ax.set_xlabel('Month')
        ax.set_ylabel('Messages')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

        # Daily Timeline
        st.subheader("Daily Timeline")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(daily['only_date'], daily['message'], color='black', linewidth=2)
        ax.set_xlabel('Date')
        ax.set_ylabel('Messages')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

        st.divider()

        # ================= Activity Map =================
        st.header("📊 Activity Patterns")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(busy_day.index, busy_day.values, color='black')
            ax.set_ylabel('Messages')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(busy_month.index, busy_month.values, color='orange')
            ax.set_ylabel('Messages')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

        # Weekly Heatmap
        st.subheader("🔥 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(user_heatmap, ax=ax, cmap="YlOrRd", linewidths=0.5)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

        st.divider()

        # ================= Busy Users (Group Level) =================
        if selected_user == "Overall":
            st.header("👥 Most Busy Users")
            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns([2, 1])

            with col1:
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.bar(x.index, x.values, color="purple")
                ax.set_ylabel('Message Count')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

            with col2:
                st.dataframe(new_df, use_container_width=True)

            st.divider()

        # ================= Word Cloud =================
        st.header("☁️ Word Cloud")
        df_wc = helper.create_word_cloud(selected_user, df)

        if df_wc is not None:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(df_wc)
            ax.axis("off")
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.warning("⚠️ No messages available to generate WordCloud for this user.")

        st.divider()

        # ================= Most Common Words =================
        st.header("🔤 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)

        col1, col2 = st.columns([2, 1])

        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(most_common_df[0], most_common_df[1], color="orange")
            ax.set_xlabel('Frequency')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

        with col2:
            st.dataframe(most_common_df, use_container_width=True)

        st.divider()

        # ================= Emoji Analysis =================
        st.header("😊 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Emoji Frequency")
            st.dataframe(emoji_df, use_container_width=True)

        with col2:
            st.subheader("Top 5 Emojis")
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%", startangle=90)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

else:
    st.info("👈 Please upload a WhatsApp chat file from the sidebar to begin analysis.")