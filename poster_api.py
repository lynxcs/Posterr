# Webserver which responds to queries
# Used by the chrome extension
from genericpath import isdir
import os, argparse, requests
from flask import request, Flask
import logging

import cloudscraper

import poster_replacer

app = Flask(__name__)

MOVIE_DIR=os.environ.get('MOVIE_DIR', None)
MOVIE_POSTER_DIR=os.environ.get('MOVIE_POSTER_DIR', None)
TV_DIR=os.environ.get('TV_DIR', None)
TV_POSTER_DIR=os.environ.get('TV_POSTER_DIR')

@app.route('/upload', methods=['POST'])
def upload_poster():
    parameters = request.form
    url = parameters['url'] # Download URL of poster
    name = parameters['name'] # Name (Year)
    media_type = parameters['type'] # Movie or Show

    # TODO: Determine all characters and how they are modified in radarr / sonarr
    name = name.translate({ord(c): None for c in '!?@#$:-'})
    name = name.translate({ord(c): '+' for c in '/'})

    if "/login" in url:
        app.logger.critical("You have to be logged in to download!");
        return '', 500

    app.logger.info("URL: " + url)
    app.logger.info("Name: " + name)
    app.logger.info("Type: " + media_type)

    # Determine if directories for current type are set
    if media_type == "Movie":
        if MOVIE_DIR is None:
            app.logger.critical("MOVIE_DIR isn't set!")
            return '', 500
        elif MOVIE_POSTER_DIR is None:
            app.logger.critical("MOVIE_POSTER_DIR isn't set!")
            return '', 500
    elif media_type == "Show":
        if TV_DIR is None:
            app.logger.critical("TV_DIR isn't set!")
            return '', 500
        elif TV_POSTER_DIR is None:
            app.logger.critical("TV_POSTER_DIR isn't set!")
            return '', 500

    download_directory = MOVIE_POSTER_DIR if media_type == "Movie" else TV_POSTER_DIR
    download_directory = os.path.join(download_directory, name)
    if not os.path.isdir(download_directory):
        os.makedirs(download_directory)

    app.logger.info("Path: " + download_directory)

    scraper = cloudscraper.create_scraper()
    r = scraper.get(url, stream=True)
    ext = r.headers['content-type'].split('/')[-1] # converts response headers mime type to an extension (may not work with everything)
    if "html" in ext:
        app.logger.critical("Failed to get poster!");
        return '', 500

    download_file = os.path.join(download_directory, "poster")
    with open("%s.%s" % (download_file, ext), 'wb') as f: # open the file to write as binary - replace 'wb' with 'w' for text files
        for chunk in r.iter_content(1024): # iterate on stream using 1KB packets
            f.write(chunk) # write the file

    directory_list = [name]
    if media_type == "Movie":
        poster_replacer.process_movies(MOVIE_POSTER_DIR, MOVIE_DIR, directory_list)
    elif media_type == "Show":
        poster_replacer.process_movies(TV_POSTER_DIR, TV_DIR, directory_list)
    else:
        app.logger.error("Downloading media of type '" + media_type + "' isn't supported yet!")
    
    return '', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("57272"))

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
