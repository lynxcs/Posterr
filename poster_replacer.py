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

class TV:
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
            os.replace(oldFile, newFile)
            print ("Found poster for " + movie.fullName + " renaming...")
            return newFile
        elif "poster" in file:
            return os.path.join(directory, file)
        else:
            print ("Ignoring " + file + " in " + movie.fullName)
    # Didn't find a file
    print(tcolors.FAIL + movie.fullName + " doesn't have a poster!" + tcolors.ENDC)
    return os.error

def process_movies(input_dir, output_dir, directory_list):
    for directory in directory_list:
        print ("Processing directory " + directory)
        movie = Movie(directory)
        poster = processPosterMovie(movie, os.path.join(input_dir, directory))

        # If poster exists in directory, continue on checking movie folder
        if poster != os.error:
            posterHash = sha256sum(poster).strip()
            oldPoster = findPosterMovie(movie, os.path.join(output_dir, directory))

            # There isn't a poster in the movies media directory
            if oldPoster == os.error:
                if not os.path.isdir(os.path.join(output_dir, directory)):
                    os.makedirs(os.path.join(output_dir, directory))
                print(tcolors.OKCYAN + movie.fullName + " doesn't have a poster! Copying..." + tcolors.ENDC)
                shutil.copyfile(poster, os.path.join(output_dir, directory, os.path.basename(poster)))
            else:
                oldPosterHash = sha256sum(oldPoster).strip()
                # If poster in the movies media directory doesn't match that in the poster directory, replace it
                if posterHash != oldPosterHash:
                    print(tcolors.OKGREEN + "Replacing poster for " + movie.fullName + tcolors.ENDC)
                    os.remove(oldPoster) # Remove old poster, as it might have a different extension and thus not be replaced by the copyfile
                    shutil.copyfile(poster, os.path.join(output_dir, directory, os.path.basename(poster)))
            print()

def findPostersTV(tv, directory, season):
    if not os.path.isdir(directory):
        print(tcolors.FAIL + "TV Show " + tv.fullName + " doesn't exist in media!")
        return os.error
    if season == -1:
        file_list = os.listdir(directory)
        for file in file_list:
            if "show" in file:
                return os.path.join(directory, file)
    else:
        if season < 10:
            season_text = "0" + str(season)
        else:
            season_text = str(season)

        if not os.path.isdir(os.path.join(directory, "Season " + season_text)):
            print(tcolors.FAIL + "TV Show " + tv.fullName + " Season " + season_text + " doesn't exist in media!")
            return os.error
        file_list = os.listdir(os.path.join(directory, "Season " + season_text))
        for file in file_list:
            file_ext = os.path.splitext(file)[1]
            if "Season" in file and ("jpeg" in file_ext or "png" in file_ext or "jpg" in file_ext):
                return os.path.join(directory, "Season " + season_text, file)
    # Didn't find a file
    return os.error
# Process the images in the posters tv directory
def processPosterTV(tv, directory):
    file_list = os.listdir(directory)
    poster_list = []
    for file in file_list:
        if "Season" not in file and (tv.fullName in file or tv.name in file):
            # TV Show poster
            extension = os.path.splitext(file)[1]
            oldFile = os.path.join(directory, file)
            newFile = os.path.join(directory, "show" + extension)
            os.replace(oldFile, newFile)
            print ("Found poster for " + tv.fullName + " renaming...")
            poster_list.append(newFile)
        elif "show" in file:
            # TV Show poster (already renamed)
            poster_list.append(os.path.join(directory, file))
        elif "Season" in file:
            if tv.fullName in file or tv.name in file:
                # Rename file
                season, extension = os.path.splitext(file.split()[-1])
                oldFile = os.path.join(directory, file)
                if (int(season) < 10):
                    newFile = os.path.join(directory, "Season0" + season + extension)
                else:
                    newFile = os.path.join(directory, "Season" + season + extension)

                os.replace(oldFile, newFile)
                print ("Found Season " + season  + " poster for " + tv.fullName + " renaming...")
                poster_list.append(newFile)
            else:
                poster_list.append(os.path.join(directory, file))
        else:
            print ("Ignoring " + file + " in " + tv.fullName)
    # Didn't find a file
    if len(poster_list) == 0:
        print(tcolors.FAIL + tv.fullName + " doesn't have a poster!" + tcolors.ENDC)
        return os.error

    print(tv.fullName + " has " + str(len(poster_list) - 1) + " seasons!")
    return poster_list

def process_shows(input_dir, output_dir, directory_list):
    # print(tcolors.FAIL + "Processing shows isn't implemented yet!" + tcolors.ENDC)
    for directory in directory_list:
        print ("Processing directory " + directory)
        tv = TV(directory)
        poster_list = processPosterTV(tv, os.path.join(input_dir, directory))
        #old_poster = findPosterTV(tv, os.path.join(output_dir, directory))
        # If poster exists in directory, continue on checking movie folder
        if poster_list != os.error:
            if not os.path.isdir(os.path.join(output_dir, directory)):
                os.makedirs(os.path.join(output_dir, directory))

            for poster in poster_list:
                if "show" in poster:
                    old_poster = findPostersTV(tv, os.path.join(output_dir, directory), -1)
                    if old_poster == os.error:
                        print(tcolors.OKCYAN + tv.fullName + " doesn't have a show poster! Copying..." + tcolors.ENDC)
                        shutil.copyfile(poster, os.path.join(output_dir, directory, os.path.basename(poster)))
                    else:
                        posterHash = sha256sum(poster).strip()
                        oldPosterHash = sha256sum(old_poster).strip()
                        # If poster in the movies media directory doesn't match that in the poster directory, replace it
                        if posterHash != oldPosterHash:
                            print(tcolors.OKGREEN + "Replacing poster for " + tv.fullName + tcolors.ENDC)
                            os.remove(old_poster) # Remove old poster, as it might have a different extension and thus not be replaced by the copyfile
                            shutil.copyfile(poster, os.path.join(output_dir, directory, os.path.basename(poster)))
                elif "Season" in poster:
                    season = os.path.splitext(poster)[0][-2:]
                    old_poster = findPostersTV(tv, os.path.join(output_dir, directory), int(season))
                    if old_poster == os.error:
                        if not os.path.isdir(os.path.join(output_dir, directory, "Season " + season)):
                            os.makedirs(os.path.join(output_dir, directory, "Season " + season))

                        print(tcolors.OKCYAN + tv.fullName + " doesn't have a season " + season + " poster! Copying..." + tcolors.ENDC)
                        shutil.copyfile(poster, os.path.join(output_dir, directory, "Season " + season, os.path.basename(poster)))
                    else:
                        posterHash = sha256sum(poster).strip()
                        oldPosterHash = sha256sum(old_poster).strip()
                        # If poster in the movies media directory doesn't match that in the poster directory, replace it
                        if posterHash != oldPosterHash:
                            print(tcolors.OKGREEN + "Replacing poster for " + tv.fullName + tcolors.ENDC)
                            os.remove(old_poster) # Remove old poster, as it might have a different extension and thus not be replaced by the copyfile
                            shutil.copyfile(poster, os.path.join(output_dir, directory, "Season " + season, os.path.basename(poster)))
        print()

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

    folder_type = infer_type(args.output_dir)
    if folder_type == "none":
        print("Can't determine input folder type!")
        exit(-1)

    if not os.path.isdir(args.input_dir):
        print("Input directory doesn't exist!")
        exit(-1)

    if not os.path.isdir(args.output_dir):
        print("Output directory doesn't exist!")
        exit(-1)

    directory_list = os.listdir(args.input_dir)
    if folder_type == "movie":
        process_movies(args.input_dir, args.output_dir, directory_list)
    else:
        process_shows(args.input_dir, args.output_dir, directory_list)

if __name__ == "__main__":
    run()
