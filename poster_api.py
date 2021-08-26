# Webserver which responds to queries
# Used by the chrome extension
from genericpath import isdir
import os, argparse, requests
from flask import request, Flask

import poster_replacer

app = Flask(__name__)

MOVIE_DIR=os.environ.get('MOVIE_DIR', None) # Directory where folders with movies are kept
MOVIE_POSTER_DIR=os.environ.get('MOVIE_POSTER_DIR', None) # Directory where to store backup's of posters
TV_DIR="" # Not used yet
TV_POSTER_DIR="" # Not used yet

@app.route('/upload', methods=['POST'])
def upload_poster():
    if MOVIE_DIR is None:
        print("MOVIE_DIR isn't set!")
        return '', 500
    elif MOVIE_POSTER_DIR is None:
        print("MOVIE_POSTER_DIR isn't set!")
        return '', 500
    parameters = request.form
    url = parameters['url'] # Download URL of poster
    name = parameters['name'] # Name (Year)
    media_type = parameters['type'] # Movie or Show

    # TODO: Determine all characters and how they are modified in radarr / sonarr
    name = name.translate({ord(c): None for c in '!?@#$:-'})
    name = name.translate({ord(c): '+' for c in '/'})

    print("URL: " + url)
    print("Name: " + name)
    print("Type: " + media_type)

    download_directory = MOVIE_POSTER_DIR if media_type == "Movie" else TV_POSTER_DIR
    download_directory = os.path.join(download_directory, name)
    if not os.path.isdir(download_directory):
        os.makedirs(download_directory)

    print("Path: " + download_directory)
    
    download_file = os.path.join(download_directory, "poster")
    r = requests.get(url, stream=True)
    ext = r.headers['content-type'].split('/')[-1] # converts response headers mime type to an extension (may not work with everything)
    with open("%s.%s" % (download_file, ext), 'wb') as f: # open the file to write as binary - replace 'wb' with 'w' for text files
        for chunk in r.iter_content(1024): # iterate on stream using 1KB packets
            f.write(chunk) # write the file

    if media_type == "Movie":
        directory_list = [name]
        poster_replacer.process_movies(MOVIE_POSTER_DIR, MOVIE_DIR, directory_list)
    else:
        print("Downloading media of type '" + media_type + "' isn't supported yet!")
    
    return '', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("57272"))
