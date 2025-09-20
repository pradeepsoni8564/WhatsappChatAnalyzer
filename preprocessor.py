import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s?(?:am|pm)\s-\s'

    msg = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_massage': msg, 'message_date': dates})
    #  convert message_data type
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M %p - ")
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df.head()

    # separate user and message
    users = []
    msges = []
    for msg in df['user_massage']:
        entry = re.split('([\\w\\W]+?):\\s', msg)
        if entry[1:]:  # user name
            users.append(entry[1])
            msges.append(entry[2])

        else:
            users.append('group_notification')
            msges.append(entry[0])

    df['user'] = users
    df['message'] = msges
    df.drop(columns=['user_massage'], inplace=True)

    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []

    # Make sure we are only iterating over the 'hour' column
    for hour in df['hour']:
        start_hour = hour
        end_hour = (hour + 1) % 24  # wrap around after 23

        # Convert to AM/PM format
        start = pd.to_datetime(str(start_hour), format="%H").strftime("%I%p")
        end = pd.to_datetime(str(end_hour), format="%H").strftime("%I%p")

        period.append(f"{start}-{end}")

    df['period'] = period

    return df