# Posterr
## Poster manager for plex / emby / jellyfin

### Introduction
This application manages posters from a poster directory, (re)placing posters in corresponding media directory. The purpose of this application is to speed up poster management, renaming, etc. Very useful to also re-add posters when Radarr or Sonarr removes them.

The application also comes with a chrome extension that adds a button to [theposterdb](https://theposterdb.com) which interacts with a flask server

Currently, everything is still in development, and only movie poster management is working, with support for TV shows and collections coming soon.

### Installation & usage
#### **Chrome extension**
To install the chrome extension:
* Download & extract the repository
* Go to [chrome://extensions](chrome://extensions)
* Turn on developer mode
* Press "Load unpacked" and navigate to the "extension" folder in the repository

To use the chrome extension:
* Press on the extension icon to set the base url for the poster API server
* Go to any theposterdb poster page (e.g "https://theposterdb.com/poster/4793")
* Press the yellow button "Upload to Posterr" (*Currently only works for movies!*)

**NOTE** This extension doesn't work without the poster API!
#### **Poster API**
To install the poster API on docker:
* Docker url is: domaskal/posterr:latest
* Two environment variables need to be defined: MOVIE_DIR and MOVIE_POSTER_DIR
* Mount volumes to the same directories as MOVIE_DIR and MOVIE_POSTER_DIR

To install the poster API another way:
* Launch with `python3 poster_api.py`, don't forget to define MOVIE_DIR and MOVIE_POSTER_DIR

*Environment Variables:*
* MOVIE_DIR - Directory where all the media is stored (directory structure: "MOVIE_DIR/Title (Year)")
* MOVIE_POSTER_DIR - Directory where the posters should be stored

#### **Poster replacer**
The poster replacer script usage is very simple:
* `python3 poster_replacer.py INPUT_DIR OUTPUT_DIR`
where INPUT_DIR is the poster location and OUTPUT_DIR is the media location
**NOTE** The media type is inferred automatically by the name, but a single run of the script can only work on a single type of media (Movie or Show), not both.

### Screenshots
Here's how the extension icon looks:
<br>
![Extension photo](images/sc-extension.png?raw=true "Extension")
<br>
And this is how the modification made to the ThePosterDB website looks:
<br>
![ThePosterDB addition](images/sc-theposterdb.png?raw=true "ThePosterDB addition")

### Getting help
If you need help troubleshooting, create an issue and I'll try to help you fix it.