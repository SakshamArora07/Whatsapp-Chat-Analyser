# gets text data and converts it into dataframe and returns the dataframe

import regex as re
import pandas as pd

import regex as re
import pandas as pd

# Function to parse the chat data from a string
# format of the chat data - 
# 11/06/22, 3:13 am - Saksham: Hello
# 23/10/22, 11:48 pm - Muskan: hi
def parse_chat(data):
    lines = data.split('\n') # data is the string containing chat logs. We split the string by newline character (\n) to process each line indivisually.

    dates = []
    users = []
    messages = []

    for line in lines: # iterating through each line in the chat
        date_time_match = re.match(r'^(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2})\s([apAP][mM]) - ', line) 
        # ^ indicates the start of the string
        # d{2} matches 2 digits each for MM/DD/YY
        # d{1,2} matches 1 or 2 digits for H:MM or HH:MM
        #\s matches whitespace character
        # [apAP][mM] for am or pm both uppercase and lowercase case insensitively
        # r'' - to ensure that backslashes are treated literally and not as escape characters. 

        if date_time_match: # if regex found a match in the line    
            date = date_time_match.group(1) # first part of the regex match date_time_match
            time = date_time_match.group(2) # second part of the regex match date_time_match 
            period = date_time_match.group(3).upper()# third part of the regex match date_time_match and convert them to uppercase AM PM
            message = line[date_time_match.end():].strip() # remainder of the line is the message and strip() is used to remove whitesace characters like tabs from the string

            # Split user and message at the 1st occurance of ':'
            user_message_split = message.split(": ", 1)
            if len(user_message_split) > 1: # if the split was successful meaning both user and the message exist
                user = user_message_split[0] # first part is the user
                message = user_message_split[1] # second part is the message
            else: # if the split hasnt occured then message belongs to the user - System
                user = "System"
                message = user_message_split[0] # the entire line is considered as the message

            dates.append(f"{date} {time} {period}") # combining the data to the dates list
            users.append(user) # adding the user to the users list
            messages.append(message) # adding the message to the messages list

    df1 = pd.DataFrame({'message_date': dates, 'user': users, 'user_message': messages}) # creating the dataframe
    print(df1)
    # final view of the processed chat data -
    # message_date          user             user_message 
    # 11/06/22 3:13 AM      Saksham          Hello
    # 23/10/22 11:48 PM     Muskan           hi
    return df1

# Function to preprocess data and return a DataFrame
def preprocess_data(data): 
    # Parse the chat data
    df = parse_chat(data)

    # Convert 'message_date' to datetime type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y %I:%M %p') # converting from string to datetime object 

    # Rename 'message_date' to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract additional time-related columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df



