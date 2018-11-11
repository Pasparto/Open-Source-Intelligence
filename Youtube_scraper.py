from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import sys



def youtube_search(options):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	DEVELOPER_KEY = 'Enter here API key'
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
	search_response = youtube.search().list(q=options.q,
	part="id,snippet",
	maxResults=options.max_results).execute()
	videos = []
	channels = []
	playlists = []
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
		elif search_result["id"]["kind"] == "youtube#channel":
			channels.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["channelId"]))
		elif search_result["id"]["kind"] == "youtube#playlist":
			playlists.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["playlistId"]))

	f = open("/var/www/cgi-bin/History/Youtube_scrapper.html",'w')
	f.write("<div id='youtube' class='hid'>\n<h1>Associated Youtube Videos</h1>\n")
		
	f.write("<h3>Videos:</h3><br>\n")
	for video in videos:
		f.write("<li>" + video + "</li>\n")

	f.write("<h3>Channels:</h3><br>")
	for channel in channels:
		f.write("<li>" + channel + "</li>\n")


	f.write("<h3>Playlists:</h3><br>\n")
	for playlist in playlists:
		f.write("<li>" + playlist + "</li>\n")