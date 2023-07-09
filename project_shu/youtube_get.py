from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd

from json_rw import *

DEVELOPER_KEY='AIzaSyA1wwM8c35Vpy2darfuHo6-OCBHCw0K3D8'
CHANNEL_NAME="에슈비_서울대학교 방송 SUB"
YOUTUBE_API_SERVICE_NAME='youtube'
YOUTUBE_API_VERSION='v3'

youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

def getPlayLists(channel) :
    search_response=youtube.search().list(
        q=channel,
        order='relevance',
        part='snippet',
        maxResults=50,
        ).execute()

    channel_id=search_response['items'][0]['id']['channelId']

    playlists=youtube.playlists().list(
        channelId=channel_id,
        part='snippet',
        maxResults=20).execute()

    ids=[]
    titles=[]
    for i in playlists['items']:
        ids.append(i['id'])
        titles.append(i['snippet']['title'])
        
    df=pd.DataFrame([ids,titles]).T
    df.columns=['PlayLists','Titles']
    return df

    
#영상 list
def getVideos(dtcu) :
    playlist_videos=youtube.playlistItems().list(
        playlistId=dtcu,
        part='snippet',
        maxResults=50)
    playlistitems_list_response=playlist_videos.execute()

    video_names=[]
    video_ids=[]
    date=[]

    for v in playlistitems_list_response['items']:
        video_names.append(v['snippet']['title'])
        video_ids.append(v['snippet']['resourceId']['videoId'])
        date.append(v['snippet']['publishedAt'])
        
    vdf=pd.DataFrame([date,video_names,video_ids]).T
    vdf.columns=['Date','Title','IDS']
    return vdf

#Title, description, thumbnail
def getTDTD(videoID) :
    request=youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=videoID)
    response = request.execute()
    try:
        return response['items'][0]['snippet']['localized']['title'],response['items'][0]['snippet']['localized']['description'],response['items'][0]['snippet']['thumbnails'][list(response['items'][0]['snippet']['thumbnails'].keys())[-1]]['url'],response['items'][0]['snippet']['publishedAt']
    except:
        return None,None,None, None

def getNewVideos(channel, path="./json_data") :
    video_list = []
    pls = getPlayLists(channel)
    for pl_id in pls['PlayLists'] :
        for v_id in getVideos(pl_id)['IDS']:
            title, des, thum , date = getTDTD(v_id)
            if not title : continue
            video = {"id":v_id, "title":title,"description":des,"thumbnail":thum, "date":date}
            if video in video_list : continue
            video_list.append(video)


    file_name = "videos_" + channel
    try:
        videos = getJSON(path, file_name)
        new_videos = [i for i in video_list if i not in videos]
        videos += new_videos
        writeJSON(path, file_name, videos)
        return new_videos
    except:
        writeJSON(path, file_name, video_list)
        return video_list
