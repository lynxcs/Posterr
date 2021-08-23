# Domas Kalinauskas 2021
# This script scans a "poster" directory, and a "media" directory, (re)placing posters for consistency!
# Heavily W.I.P, doesn't work yet!
# Example usage: python poster_replacer.py -i INPUT_DIR -o OUTPUT_DIR

# Input folder directory structure:
# ALL FOLDERS SHOULD HAVE RELEASE DATE (e.g Tenet (2020) ), this is used to determine which part of filename to ignore, and is crucial!
# Movie posters -> FOLDER OF MOVIES -> single jpg file
# Tv Show posters -> FOLDER OF TV SHOWS -> Season xx (e.g Season 01) TODO
import os, hashlib, argparse, pathlib, shutil

# Terminal colors
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Stack overflow by maxschlepzig
# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
# Used to check poster hash and see if current poster matches poster in folder
def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

# Movie defining class
class Movie:
    def __init__(self, folderName):
        self.fullName = folderName
        self.name = folderName[:-7]
        self.year = folderName[-5:][:-1]

# Find poster in media movie directory
def findPosterMovie(movie, directory):
    if not os.path.isdir(directory):
        print(tcolors.FAIL + "Movie " + movie.fullName + " doesn't exist in media!")
        return os.error
    file_list = os.listdir(directory)
    for file in file_list:
        if "poster" in file:
            return os.path.join(directory, file)
    # Didn't find a file
    return os.error

# Process the images in the posters movie directory
def processPosterMovie(movie, directory):
    file_list = os.listdir(directory)
    for file in file_list:
        if movie.fullName in file or movie.name in file:
            extension = os.path.splitext(file)[1]
            oldFile = os.path.join(directory, file)
            newFile = os.path.join(directory, "poster" + extension)
            os.rename(oldFile, newFile)
            print ("Found poster for " + movie.fullName + " renaming...")
            return newFile
        elif "poster" in file:
            #print ("Found poster for " + movie.fullName)
            return os.path.join(directory, file)
        else:
            print ("Ignoring " + file + " in " + movie.fullName)
    # Didn't find a file
    print(tcolors.FAIL + movie.fullName + " doesn't have a poster!" + tcolors.ENDC)
    return os.error

def process_movies(input_dir, output_dir):
    print("Processing movies")
    directory_list = os.listdir(input_dir)
    for directory in directory_list:
        movie = Movie(directory)
        poster = processPosterMovie(movie, os.path.join(input_dir, directory))

        # If poster exists in directory, continue on checking movie folder
        if poster != os.error:
            posterHash = sha256sum(poster).strip()
            oldPoster = findPosterMovie(movie, os.path.join(output_dir, directory))

            # There isn't a poster in the movies media directory
            if oldPoster == os.error:
                if os.path.isdir(os.path.join(output_dir, directory)):
                    print(tcolors.OKCYAN + movie.fullName + " doesn't have a poster! Copying..." + tcolors.ENDC)
                    print(poster + " -> " + os.path.join(output_dir, directory, os.path.basename(poster)))
                    shutil.copyfile(poster, os.path.join(output_dir, directory, os.path.basename(poster)))
                    print()
                else:
                    continue
            else:
                oldPosterHash = sha256sum(oldPoster).strip()
                # If poster in the movies media directory doesn't match that in the poster directory, replace it
                if posterHash != oldPosterHash:
                    print(tcolors.OKGREEN + "Replacing poster for " + movie.fullName + tcolors.ENDC)
                    shutil.copyfile(poster, os.path.join(output_dir, directory, os.path.basename(poster)))
                # More stuff here
                    

def process_shows(input_dir, output_dir):
    print(tcolors.FAIL + "Processing shows isn't implemented yet!" + tcolors.ENDC)
    #print("Processing shows")
    #directory_list = os.listdir(input_dir)
    #for directory in directory_list:
    #    print("Checking directory: " + directory)


# Tries to infer the type of directory (movie or tv show)
# Returns "movie", "show" or "none" depending on type inferred
def infer_type(directory):
    path = pathlib.PurePath(directory).name.lower()
    # Movie folder (skipping first letter as to trigger with both capital and lowercase m)
    if "movie" in path:
        print("Directory inferred as movie")
        return "movie"
    elif "show" in path or "tv" in path:
        print ("Directory inferred as show")
        return "show"
    else: # Can't determine type
        print (tcolors.FAIL + "Can't determine folder type!" + tcolors.ENDC)
        return "none"
        

def run():
    # Parse arguments
    parser = argparse.ArgumentParser("poster_replacer")
    parser.add_argument("input_dir", help="The input directory containing posters", type=str)
    parser.add_argument("output_dir", help="The input directory containing posters", type=str)
    args = parser.parse_args()

    folder_type = infer_type(args.input_dir)
    if folder_type == "none":
        print("Can't determine input folder type!")
        exit(-1)

    if not os.path.isdir(args.input_dir):
        print("Input directory doesn't exist!")
        exit(-1)

    # Uncomment this later
    #if not os.path.isdir(args.output_dir):
    #    print("Output directory doesn't exist!")
    #    exit(-1)

    if folder_type == "movie":
        process_movies(args.input_dir, args.output_dir)
    else:
        process_shows(args.input_dir, args.output_dir)

if __name__ == "__main__":
    run()