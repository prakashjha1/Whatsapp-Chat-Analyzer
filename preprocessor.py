import re
import pandas as pd 

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s' 
    messages = re.split(pattern,data)[1:]
    messages = list(map(lambda x:x.replace("*"," "),messages))
    messages = list(map(lambda x:x.replace("\n"," "),messages))
    messages = list(map(lambda x:x.replace("\n\n"," "),messages))
    messages = list(map(lambda x:x.replace(","," "),messages))
    dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_message':messages,'date':dates})
    # # convert message_date type
    df['date'] = pd.to_datetime(df['date'],format='%m/%d/%y, %H:%M - ')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]: #user name
            users.append(entry[1])
            messages.append(entry[2:])
        else:
            users.append('group_notification')
            messages.append(entry[0])
        
    df['user'] = users
    df['message'] = messages
    df['message'] = df['message'].apply(lambda x: str(x) if type(x)== str else str(x).strip("[]"))
    df['message'] = df['message'].apply(lambda x: x.replace("'"," "))
    df['message'] = df['message'].apply(lambda x: x.replace(","," "))
    df.drop(columns=['user_message'],inplace = True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []

    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+" - "+str('00'))
        elif hour == 0:
            period.append(str('00')+" - "+str(hour+1))
        else:
            period.append(str(hour)+" - "+str(hour+1))
    
    df['period'] = period

    return df







