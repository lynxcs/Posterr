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
TV_POSTER_DIR=os.environ.get('TV_POSTER_DIR', None)

# TODO: Determine all characters and how they are modified in radarr / sonarr
def normalize_name(name):
    name = name.translate({ord(c): None for c in '!?@#$:'})
    name = name.translate({ord(c): '+' for c in '/'})
    return name

@app.route('/upload', methods=['POST'])
def upload_poster():
    parameters = request.form
    url = parameters['url'] # Download URL of poster
    name = parameters['name'] # Name (Year)
    media_type = parameters['type'] # Movie or Show

    if "/login" in url:
        app.logger.critical("You have to be logged in to download!");
        return '', 500

    name = normalize_name(name)
    name = (name.split(")")[0]) + ")" # Only select first part of title

    app.logger.info("URL: " + url)
    app.logger.info("Name: " + name)
    app.logger.info("Type: " + media_type)

    # Determine if directories for current type are set
    download_directory = ""
    if media_type == "Movie":
        download_directory = MOVIE_POSTER_DIR
        if MOVIE_DIR is None:
            app.logger.critical("MOVIE_DIR isn't set!")
            return '', 500
        elif MOVIE_POSTER_DIR is None:
            app.logger.critical("MOVIE_POSTER_DIR isn't set!")
            return '', 500
    elif media_type == "Show":
        download_directory = TV_POSTER_DIR
        if TV_DIR is None:
            app.logger.critical("TV_DIR isn't set!")
            return '', 500
        elif TV_POSTER_DIR is None:
            app.logger.critical("TV_POSTER_DIR isn't set!")
            return '', 500

    download_directory = os.path.join(download_directory, name)
    if not os.path.isdir(download_directory):
        os.makedirs(download_directory, 0o777)

    app.logger.info("Path: " + download_directory)

    scraper = cloudscraper.create_scraper()
    r = scraper.get(url, stream=True)

    filename = normalize_name(r.headers['content-disposition'].split('"')[1])

    if "html" in r.headers['content-type'].split('/')[-1]:
        app.logger.critical("Failed to get poster!");
        return '', 500

    with open(os.open(os.path.join(download_directory, filename), os.O_CREAT | os.O_WRONLY, 0o777), 'wb') as f: # open the file to write as binary - replace 'wb' with 'w' for text files
        for chunk in r.iter_content(1024): # iterate on stream using 1KB packets
            f.write(chunk) # write the file

    directory_list = [name]
    if media_type == "Movie":
        poster_replacer.process_movies(MOVIE_POSTER_DIR, MOVIE_DIR, directory_list)
    elif media_type == "Show":
        poster_replacer.process_shows(TV_POSTER_DIR, TV_DIR, directory_list)
    else:
        app.logger.error("Downloading media of type '" + media_type + "' isn't supported yet!")
    
    return '', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("57272"))
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
