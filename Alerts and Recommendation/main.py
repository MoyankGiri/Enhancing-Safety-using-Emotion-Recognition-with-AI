from flask import Flask, flash, redirect, render_template, request, session, abort
 
import sys
import spotipy
import spotipy.util as util

import random

from spotify_functions import authenticate_spotify, aggregate_top_artists, aggregate_top_tracks, select_tracks, create_playlist

client_id = "e497bebef80547fb928fb9cef8d51118"
client_secret = "891ef3573e864066bd309344f1d390fe"
redirect_uri = "https://127.0.0.1:8008/"

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

username = "iok0nh3zbhf7hiehmdxmpi9kl"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)




app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('input.html')


@app.route("/<emotion>", methods=['POST'])
#@app.route('/<emotion>')
#@app.route('/', methods=['POST'])
def moodtape(emotion):
	#mood = request.form['text']
	#username = request.form['username']
	#mood = float(mood)
	#token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
	mood = emotion
	#client_id = "e497bebef80547fb928fb9cef8d51118"
	#client_secret = "891ef3573e864066bd309344f1d390fe"	
	#redirect_uri = "https://127.0.0.1:8008/"

	#scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

	#username = "iok0nh3zbhf7hiehmdxmpi9kl"
	#token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
	spotify_auth = authenticate_spotify(token)
	top_artists = aggregate_top_artists(spotify_auth)
	top_tracks = aggregate_top_tracks(spotify_auth, top_artists)
	selected_tracks = select_tracks(spotify_auth, top_tracks, mood)
	playlist = create_playlist(spotify_auth, selected_tracks, mood)
	print(playlist)
	#return render_template('playlist.html', playlist=playlist)
	return playlist


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001)
