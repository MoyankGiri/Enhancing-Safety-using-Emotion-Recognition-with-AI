import sys
import spotipy
import spotipy.util as util

import random

client_id = "e497bebef80547fb928fb9cef8d51118"
client_secret = "891ef3573e864066bd309344f1d390fe"
redirect_uri = "https://127.0.0.1:8008/"

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
    mood = sys.argv[2]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
	
	#Step 1. Authenticating Spotipy

	def authenticate_spotify():
		print('...connecting to Spotify')
		sp = spotipy.Spotify(auth=token)
		return sp

    #Step 2. Creating a list of your favorite artists

	def aggregate_top_artists(sp):
		print('...getting your top artists')
		top_artists_name = []
		top_artists_uri = []

		ranges = ['short_term', 'medium_term', 'long_term']
		for r in ranges:
			top_artists_all_data = sp.current_user_top_artists(limit=50, time_range= r)
			top_artists_data = top_artists_all_data['items']
			for artist_data in top_artists_data:
				if artist_data["name"] not in top_artists_name:		
					top_artists_name.append(artist_data['name'])
					top_artists_uri.append(artist_data['uri'])

		followed_artists_all_data = sp.current_user_followed_artists(limit=50)
		followed_artists_data = (followed_artists_all_data['artists'])
		for artist_data in followed_artists_data["items"]:
			if artist_data["name"] not in top_artists_name:
				top_artists_name.append(artist_data['name'])
				top_artists_uri.append(artist_data['uri'])
		return top_artists_uri


    #Step 3. For each of the artists, get a set of tracks for each artist
    
	def aggregate_top_tracks(sp, top_artists_uri):
		print("...getting top tracks")
		top_tracks_uri = []
		for artist in top_artists_uri:
			top_tracks_all_data = sp.artist_top_tracks(artist)
			top_tracks_data = top_tracks_all_data['tracks']
			for track_data in top_tracks_data:
				top_tracks_uri.append(track_data['uri'])
		return top_tracks_uri

	# Step 4. From top tracks, select tracks that are within a certain mood range

	def select_tracks(sp, top_tracks_uri):
		
		print("...selecting tracks")
		selected_tracks_uri = []
		def group(seq, size):
			return (seq[pos:pos + size] for pos in range(0, len(seq), size))

		emo = {"Happy":1.0 , "Surprised":0.7,"Sad":0.05,"Angry":0.3,"Disgust":0.2,"Neutral":0.5,"Fear":0.8}
		random.shuffle(top_tracks_uri)
		for tracks in list(group(top_tracks_uri, 50)):
			tracks_all_data = sp.audio_features(tracks)
			for track_data in tracks_all_data:
				try:
					if mood=="Sad" :
						if (0 <= track_data["valence"] <= (emo["Sad"] + 0.15)
						and track_data["danceability"] <= (emo["Sad"]*8)
						and track_data["energy"] <= (emo["Sad"]*10)):
							selected_tracks_uri.append(track_data["uri"])					
					elif mood=="Disgust":						
						if (( emo["Disgust"] - 0.075) <= track_data["valence"] <= ( emo["Disgust"]+ 0.075)
						and track_data["danceability"] <= (emo["Disgust"]*4)
						and track_data["energy"] <= (emo["Disgust"]*5)):
							selected_tracks_uri.append(track_data["uri"])
					elif mood=="Angry":						
						if ((emo["Angry"] - 0.075) <= track_data["valence"] <= ( emo["Angry"]+ 0.075)
						and track_data["danceability"] <= (emo["Angry"]*3)
						and track_data["energy"] <= (emo["Angry"]*4)):
							selected_tracks_uri.append(track_data["uri"])
					elif mood=="Neutral":						
						if ((emo["Neutral"] - 0.05) <= track_data["valence"] <= (emo["Neutral"] + 0.05)
						and track_data["danceability"] <= (emo["Neutral"]*1.75)
						and track_data["energy"] <= (emo["Neutral"]*1.75)):
							selected_tracks_uri.append(track_data["uri"])
					elif mood=="Surprised":						
						if ((emo["Surprised"] - 0.075) <= track_data["valence"] <= (emo["Surprised"] + 0.075)
						and track_data["danceability"] >= (emo["Surprised"]/2.5)
						and track_data["energy"] >= (emo["Surprised"]/2)):
							selected_tracks_uri.append(track_data["uri"])
					elif mood=="Fear":						
						if ((emo["Fear"] - 0.075) <= track_data["valence"] <= (emo["Fear"] + 0.075)
						and track_data["danceability"] >= (emo["Fear"]/2)
						and track_data["energy"] >= (emo["Fear"]/1.75)):
							selected_tracks_uri.append(track_data["uri"])
					elif mood=="Happy":
						if ((emo["Happy"] - 0.15) <= track_data["valence"] <= 1
						and track_data["danceability"] >= (emo["Happy"]/1.75)
						and track_data["energy"] >= (emo["Happy"]/1.5)):
							selected_tracks_uri.append(track_data["uri"])
				except TypeError as te:
					continue
	
		return selected_tracks_uri			

	# Step 5. From these tracks, create a playlist for user

	def create_playlist(sp, selected_tracks_uri):

		print("...creating playlist")
		user_all_data = sp.current_user()
		user_id = user_all_data["id"]

		playlist_all_data = sp.user_playlist_create(user_id,"You feel : "+ mood )
		playlist_id = playlist_all_data["id"]
		#print(selected_tracks_uri)
		random.shuffle(selected_tracks_uri)
		sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks_uri[0:30])


	spotify_auth = authenticate_spotify()
	top_artists = aggregate_top_artists(spotify_auth)
	top_tracks = aggregate_top_tracks(spotify_auth, top_artists)
	selected_tracks = select_tracks(spotify_auth, top_tracks)
	create_playlist(spotify_auth, selected_tracks)



else:
    print("Can't get token for", username)

