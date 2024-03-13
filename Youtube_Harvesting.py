import pandas as pd
import pymongo
import plotly.express as px
import streamlit as st
from googleapiclient.discovery import build
from PIL import Image
from streamlit_option_menu import option_menu

# FUNCTION FOR CHANNEL DETAILS
def get_channel_details(channel_id):
    ch_data = []
    response = youtube.channels().list(part='snippet,contentDetails,statistics',
                                       id=channel_id).execute()

    for item in response['items']:
        data = {
            'Channel_id': item['id'],
            'Channel_name': item['snippet']['title'],
            'Playlist_id': item['contentDetails']['relatedPlaylists']['uploads'],
            'Subscribers': item['statistics']['subscriberCount'],
            'Views': item['statistics']['viewCount'],
            'Total_videos': item['statistics']['videoCount'],
            'Description': item['snippet']['description'],
            'Country': item['snippet'].get('country')
        }
        ch_data.append(data)
    return ch_data


# FUNCTION FOR VIDEO IDS
def get_channel_videos(channel_id):
    video_ids = []
    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, part='snippet', maxResults=50,
                                           pageToken=next_page_token).execute()

        for item in res['items']:
            video_ids.append(item['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')

        if not next_page_token:
            break
    return video_ids


# FUNCTION FOR VIDEO DETAILS
def get_video_details(video_ids):
    video_stats = []

    for i in range(0, len(video_ids), 50):
        response = youtube.videos().list(part="snippet,contentDetails,statistics",
                                         id=','.join(video_ids[i:i + 50])).execute()
        for item in response['items']:
            video_details = {
                'Channel_name': item['snippet']['channelTitle'],
                'Channel_id': item['snippet']['channelId'],
                'Video_id': item['id'],
                'Title': item['snippet']['title'],
                'Tags': item['snippet'].get('tags'),
                'Thumbnail': item['snippet']['thumbnails']['default']['url'],
                'Description': item['snippet']['description'],
                'Published_date': item['snippet']['publishedAt'],
                'Duration': item['contentDetails']['duration'],
                'Views': item['statistics']['viewCount'],
                'Likes': item['statistics'].get('likeCount'),
                'Comments': item['statistics'].get('commentCount'),
                'Favorite_count': item['statistics']['favoriteCount'],
                'Definition': item['contentDetails']['definition'],
                'Caption_status': item['contentDetails']['caption']
            }
            video_stats.append(video_details)
    return video_stats


# FUNCTION FOR COMMENT DETAILS
def get_comments_details(video_id):
    comment_data = []
    try:
        next_page_token = None
        while True:
            response = youtube.commentThreads().list(part="snippet,replies",
                                                      videoId=video_id,
                                                      maxResults=100,
                                                      pageToken=next_page_token).execute()
            for item in response['items']:
                data = {
                    'Comment_id': item['id'],
                    'Video_id': item['snippet']['videoId'],
                    'Comment_text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'Comment_author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'Comment_posted_date': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                    'Like_count': item['snippet']['topLevelComment']['snippet']['likeCount'],
                    'Reply_count': item['snippet']['totalReplyCount']
                }
                comment_data.append(data)
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
    except Exception as e:
        print(f"Error: {e}")
    return comment_data


# FUNCTION FOR CHANNEL NAMES FROM MONGODB
def channel_names():
    ch_name = []
    for item in db.channel_details.find():
        ch_name.append(item['Channel_name'])
    return ch_name

# PAGE CONFIGURATIONS
logo = Image.open("Youtube_logo.png")
st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing",
                   page_icon= logo,
                   layout= "centered",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This is an app used to harvest data from youtube and process it to do different task on it..... Made by *Sarthak Singh!*"""})

# MongoDB Connection and Creating a new database
client = pymongo.MongoClient("localhost:27017")
db = client.youtube_data

# CONNECTING WITH YOUTUBE API
api_key = "AIzaSyCSxPiXODQWEEzr1CHSjYZndi9rZbhUWAg"
youtube = build('youtube', 'v3', developerKey=api_key)

# CREATING COLLECTIONS IN MONGODB
collections1 = db.channel_details
collections2 = db.video_details
collections3 = db.comments_details

# MAIN PAGE
with st.sidebar:
    selected = option_menu(None, ["Project Description","Data Processing","Accessing Information"], 
                           icons=["house-door-fill","tools","card-text"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#C80101"},
                                   "icon": {"font-size": "30px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#C80101"}})

if selected == "Project Description":
    st.markdown("<h2 style='font-size: 20px; color: green'>Topic of the project : YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit</h2>", unsafe_allow_html=True)
    st.write("<hr>", unsafe_allow_html=True) 
    st.markdown("<h2 style='font-size: 20px; color: orange'>Problem Statement:</h2>", unsafe_allow_html=True)
    st.write("""
The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
  - Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
  - Option to store the data in a MongoDB database as a data lake.
  - Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
  - Option to select a channel name and migrate its data from the data lake to a SQL database as tables.
  - Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.
""")
    st.write("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 20px; color: yellow'>Approach:</h2>", unsafe_allow_html=True)
    st.write("""
1. Set up a Streamlit app: Streamlit is a great choice for building data visualization and analysis tools quickly and easily. You can use Streamlit to create a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.
2. Connect to the YouTube API: You'll need to use the YouTube API to retrieve channel and video data. You can use the Google API client library for Python to make requests to the API.
3. Store data in a MongoDB data lake: Once you retrieve the data from the YouTube API, you can store it in a MongoDB data lake. MongoDB is a great choice for a data lake because it can handle unstructured and semi-structured data easily.
4. Migrate data to a SQL data warehouse: After you've collected data for multiple channels, you can migrate it to a SQL data warehouse. You can use a SQL database such as MySQL or PostgreSQL for this.
5. Query the SQL data warehouse: You can use SQL queries to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input. You can use a Python SQL library such as SQLAlchemy to interact with the SQL database.
6. Display data in the Streamlit app: Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data.
Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing it in a MongoDB data lake, migrating it to a SQL data warehouse, querying the data warehouse with SQL, and displaying the data in the Streamlit app.
""")

    
# EXTRACT AND TRANSFORM PAGE
if selected == "Data Processing":
    st.write("### Enter YouTube Channel_ID below :")
    ch_id = st.text_input("").split(',')

    if ch_id and st.button("Extract Data"):
        ch_details = get_channel_details(ch_id)
        st.write(f'#### Extracted data from :green["{ch_details[0]["Channel_name"]}"] channel')
        st.table(ch_details)
        
    if st.button("Save to MongoDB"):
        if ch_id:
            with st.spinner('Saving the data...'):
                ch_details = get_channel_details(ch_id)
                v_ids = get_channel_videos(ch_id)
                vid_details = get_video_details(v_ids)

                comm_details = []
                for vid_id in v_ids:
                    comm_details.extend(get_comments_details(vid_id))

                collections1.insert_many(ch_details)
                collections2.insert_many(vid_details)
                collections3.insert_many(comm_details)
                st.success("Data saved to MongoDB successfully!")
        else:
            st.warning("Please enter a valid YouTube Channel ID before saving to MongoDB.")


# VIEW PAGE
if selected == "Accessing Information":
    st.write("## :orange[Pick a question to uncover trends]")
    questions = st.selectbox('List of questions:', [
        '1. What are the names of all the videos and their corresponding channels?',
        '2. Which channels have the most number of videos, and how many videos do they have?',
        '3. What are the top 10 most viewed videos and their respective channels?',
        '4. How many comments were made on each video, and what are their corresponding video names?',
        '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
        '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
        '7. What is the total number of views for each channel, and what are their corresponding channel names?',
        '8. What are the names of all the channels that have published videos in the year 2022?',
        '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
        '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])


    if questions == '1. What are the names of all the videos and their corresponding channels?':
        df = pd.DataFrame(db.video_details.find({}, {'_id': 0, 'Title': 1, 'Channel_name': 1}))
        st.write(df)

    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        pipeline = [
            {"$group": {"_id": "$Channel_name", "Total_Videos": {"$sum": 1}}},
            {"$sort": {"Total_Videos": -1}}
        ]
        df = pd.DataFrame(list(db.video_details.aggregate(pipeline)))
        st.write(df)
        st.write("### :green[Number of videos in each channel :]")
        fig = px.bar(df, x="_id", y="Total_Videos", orientation='v', color="_id")
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        pipeline = [
            {"$sort": {"Views": -1}},
            {"$limit": 10},
            {"$project": {"_id": 0, "Channel_name": 1, "Title": 1, "Views": 1}}
        ]
        df = pd.DataFrame(list(db.video_details.aggregate(pipeline)))
        st.write(df)
        st.write("### :green[Top 10 most viewed videos :]")
        fig = px.bar(df, x="Views", y="Title", orientation='h', color="Channel_name")
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        pipeline = [
            {"$group": {"_id": "$Video_id", "Total_Comments": {"$sum": 1}}},
            {"$lookup": {"from": "video_details", "localField": "_id", "foreignField": "Video_id", "as": "video"}},
            {"$unwind": "$video"},
            {"$project": {"_id": 0, "Video_Title": "$video.Title", "Total_Comments": 1}}
        ]
        df = pd.DataFrame(list(db.comments_details.aggregate(pipeline)))
        st.write(df)

    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        pipeline = [
            {"$sort": {"Likes": -1}},
            {"$limit": 10},
            {"$project": {"_id": 0, "Channel_name": 1, "Title": 1, "Likes": 1}}
        ]
        df = pd.DataFrame(list(db.video_details.aggregate(pipeline)))
        st.write(df)
        st.write("### :green[Top 10 most liked videos :]")
        fig = px.bar(df, x="Likes", y="Title", orientation='h', color="Channel_name")
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        pipeline = [
            {"$group": {"_id": "$Video_id", "Total_Likes": {"$sum": "$Likes"}, "Total_Dislikes": {"$sum": "$Dislikes"}}},
            {"$lookup": {"from": "video_details", "localField": "_id", "foreignField": "Video_id", "as": "video"}},
            {"$unwind": "$video"},
            {"$project": {"_id": 0, "Title": "$video.Title", "Total_Likes": 1, "Total_Dislikes": 1}}
        ]
        df = pd.DataFrame(list(db.comments_details.aggregate(pipeline)))
        st.write(df)

    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        pipeline = [
            {"$group": {"_id": "$Channel_name", "Total_Views": {"$sum": "$Views"}}},
            {"$project": {"_id": 0, "Channel_Name": "$_id", "Total_Views": 1}}
        ]
        df = pd.DataFrame(list(db.video_details.aggregate(pipeline)))
        st.write(df)
        st.write("### :green[Channels vs Views :]")
        fig = px.bar(df, x="Total_Views", y="Channel_Name", orientation='h', color="Channel_Name")
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        pipeline = [
            {"$match": {"Published_date": {"$regex": "^2022"}}},
            {"$group": {"_id": "$Channel_name"}},
            {"$project": {"_id": 0, "Channel_Name": "$_id"}}
        ]
        df = pd.DataFrame(list(db.video_details.aggregate(pipeline)))
        st.write(df)

    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        pipeline = [
            {"$group": {"_id": "$Channel_name", "Average_Duration": {"$avg": "$Duration"}}},
            {"$project": {"_id": 0, "Channel_Name": "$_id", "Average_Duration": {"$divide": ["$Average_Duration", 60]}}}
        ]
        df = pd.DataFrame(list(db.video_details.aggregate(pipeline)))
        st.write(df)
        st.write("### :green[Avg video duration for channels :]")
        fig = px.bar(df, x="Average_Duration", y="Channel_Name", orientation='h', color="Channel_Name")
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        pipeline = [
            {"$sort": {"Comments": -1}},
            {"$limit": 10},
            {"$project": {"_id": 0, "Channel_name": 1, "Title": 1, "Comments": 1}}
        ]
        df = pd.DataFrame(list(db.video_details.aggregate(pipeline)))
        st.write(df)
        st.write("### :green[Videos with most comments :]")
        fig = px.bar(df, x="Comments", y="Title", orientation='h', color="Channel_name")
        st.plotly_chart(fig, use_container_width=True)
