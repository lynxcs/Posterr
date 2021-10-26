# Posterr
## Poster manager for plex / emby / jellyfin

### Introduction
This application manages posters from a poster directory, (re)placing posters in corresponding media directory. The purpose of this application is to speed up poster management. Very useful to automatically re-add posters when Radarr or Sonarr removes them.

~~The application also comes with a chrome extension that adds a button to [theposterdb](https://theposterdb.com) which interacts with a flask server~~  
**The chrome extension was removed, due to TPDb complaining that it violates their ToS.**

Currently, movie and TV Show poster management is working, with support for collections coming soon.
### Installation & usage
#### **Poster API**
To install the poster API on docker:
* Docker url is: domaskal/posterr:latest
* Four environment variables need to be defined: MOVIE_DIR, MOVIE_POSTER_DIR, TV_DIR, TV_POSTER_DIR
* Mount volumes to the same directories as MOVIE_DIR, MOVIE_POSTER_DIR, TV_DIR, TV_POSTER_DIR

*Environment Variables:*
* MOVIE_DIR - Directory where all the movie media is stored (directory structure: "MOVIE_DIR/Title (Year)")
* MOVIE_POSTER_DIR - Directory where the movie posters should be stored
* TV_DIR - Directory where all the TV media is stored (directory structure: "TV_DIR/Title (Year)")
* TV_POSTER_DIR - Directory where the TV posters should be stored

#### **Poster replacer**
The poster replacer script usage is very simple:
* `python3 poster_replacer.py INPUT_DIR OUTPUT_DIR`
where INPUT_DIR is the poster location and OUTPUT_DIR is the media location
**NOTE** The media type is inferred automatically by the name, but a single run of the script can only work on a single type of media (Movie or Show), not both.

### Getting help
If you need help troubleshooting, create an issue and I'll try to help you fix it.