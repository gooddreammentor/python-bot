import credentials
import tweepy
import time
import sqlite3

# Creating a DB
db = "followers.db"
message_list = []
# Creting a table in sqlite3
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        # Creating the table sql query executed
        c.execute(create_table_sql)
    except:
        print("Error")
# Create Twitter API For Your Account
def create_api():
    # Put the keys and make the API
    auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    # Defining the API Options
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    return api

# Detect Followers API
def follow_followers(api):
    # Connect to SQLITE database
    sqliteConnection = sqlite3.connect('followers.db')
    # Create a cursor
    cursor = sqliteConnection.cursor()
    # Track all the followers
    for follower in tweepy.Cursor(api.followers).items():
        try:
            # Add add the values to the database
            cursor.execute("insert into users values(?,?)",(follower.id, follower.name))
            # Commit the connection
            sqliteConnection.commit()
            # Close the database
            cursor.close()
            # Found a new follower
            print("You have a new follower "+follower.name)
            dm = api.send_direct_message(follower.id,"Welcome to my workspace")
            print("You sent a message "+dm.message_create['message_data']['text'])
        except:
            break

def main():
    # Creating the sql table
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS users (
                                            id PRIMARY KEY,
                                            name text
                                        ); """
    # Create the connection
    conn = sqlite3.connect(db)
    if conn is not None:
        create_table(conn, sql_create_projects_table)
    else:
        print("Error! cannot create the database connection.")
    print("Welcome to Twitter Bot !!")
    # Create the api
    api = create_api()
    while True:
        # Detect the followers
        follow_followers(api)
        print("Bot Searching ....")
        time.sleep(20)
        # Get all the dms
        last_dms = api.list_direct_messages()
        for messages in last_dms:
            # Checking if the message not sent by the bot
            if(messages.message_create['message_data']['text'] != "Welcome to my workspace"):
                # Checking if the message is not repeated
                if(messages.message_create['message_data']['text'] not in message_list):
                    print("New Message From Follower "+messages.message_create['message_data']['text'])
                    message_list.append(messages.message_create['message_data']['text'])
                    print("Bot Searching ....")
                    time.sleep(20)
if __name__ == "__main__":
    main()

