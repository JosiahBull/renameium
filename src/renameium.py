#!/usr/bin/env python3

import logging
import os
from time import sleep
import database
from config import general_config
import shutil



def main():
    """ Main function for renameium """
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(levelname)s %(message)s')

    config = general_config()
    os.makedirs(os.path.dirname(config.get('log_file')), exist_ok=True)

    logging.info("starting renameium...")

    if not database.check_init():
        logging.info("database not initialized, initializing...")
        database.init()
        logging.info("database initialized.")
    else:
        logging.info("database already initialized.")

    while True:
        logging.info("scanning for new movie additions")
        movies = database.get_movies()

        for movie in movies:
            # rename the movie
            new_name = (config.get('movie_rename_format')
                .replace('{{title}}', movie.title)
                .replace('{{year}}', 'n/a')
            )
            # move the movie to the new location
            old_path = movie.path
            # create new path by changing last filename to new name, with the file extension added to the end
            new_path = old_path.replace(old_path.split('/')[-1], new_name) + '.' + old_path.split('/')[-1].split('.')[-1]

            logging.info("moving movie: '%s' to: '%s'" % (old_path, new_path))

            # move the movie
            # shutil.move(old_path, new_path)

            # update the database
            # database.set_renameium_state(movie.fileId, new_path)

        logging.info("scanning for new show additions")
        shows = database.get_shows()

        for show in shows:
            # rename the show
            new_name = (config.get('show_rename_format')
                .replace('{{title}}', show.title)
                # .replace('\{\{year\}\}', show.year) #TODO: integrate with imbd for this information
                .replace('{{season}}', "{:02d}".format(int(show.seasonNumber)))
                .replace('{{episode}}', "{:02d}".format(int(show.episodeNumber)))
            )
            # move the show to the new location
            old_path = show.path
            # create new path by changing last filename to new name, with the file extension added to the end
            new_path = old_path.replace(old_path.split('/')[-1], new_name) + '.' + old_path.split('/')[-1].split('.')[-1]

            logging.info("moving show: '%s' to: '%s'" % (old_path, new_path))

            # move the show
            # shutil.move(old_path, new_path)

            # database.set_renameium_state(show.fileId, new_path)

        sleep(int(config.get('refresh_period')) * 1000)


main()