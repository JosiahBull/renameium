#!/usr/bin/env python3

import config as config
import psycopg2 as Db

class Movie:
    def __init__(self, movieId, title, createdAt, path, fileId):
        self.movieId = movieId
        self.title = title
        self.createdAt = createdAt
        self.path = path
        self.fileId = fileId

class Show:
    def __init__(self, showId, seasonNumber, episodeNumber, title, createdAt, path, fileId):
        self.showId = showId
        self.seasonNumber = seasonNumber
        self.episodeNumber = episodeNumber
        self.title = title
        self.createdAt = createdAt
        self.path = path
        self.fileId = fileId

def connect():
    """ Connect to the PostgreSQL database server """
    # read connection parameters
    params = config.database_config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = Db.connect(**params)

    return conn

def check_init():
    """ Check if the database is initialized, returns True if it is, False otherwise """

    conn = None
    try:
        conn = connect()
        curr = conn.cursor()

        # check if the file table has the renameium_state column
        curr.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'file' AND column_name = 'renameium_state';")

        count = curr.rowcount

        curr.close()

        return count == 1
    except (Exception, Db.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

#TODO: these should throw errors up the chain correctly, so that we don't continue assuming these are good
def init():
    """ Attempt to initalise the database for use by renameium, this involves modifying and creating several tables. """

    conn = None
    try:
        conn = connect()
        curr = conn.cursor()

        # alter the movie and tv_show tables to add renameium_state column with default value of false
        curr.execute("ALTER TABLE file ADD COLUMN renameium_state boolean DEFAULT false;")

        # XXX: store any other state we need to by creating the relevant tables.

        curr.close()
    except (Exception, Db.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def set_renameium_state(fileId, new_path):
    """ Set the renameium_state column to true for the given file """
    conn = None
    try:
        conn = connect()
        curr = conn.cursor()
        curr.execute("UPDATE file SET renameium_state = true, path=%s WHERE id = %s;", (new_path, fileId,))
        curr.close()
    except (Exception, Db.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def get_movies():
    """ Query all movies from the table, returning a list of Movie objects """

    conn = None
    try:
        conn = connect()
        curr = conn.cursor()
        curr.execute("""
            SELECT f.\"movieId\", m.title, f.\"createdAt\", f.path, f.id
            FROM file as f JOIN movie as m on f.\"movieId\"=m.id
            WHERE f.\"movieId\" IS NOT NULL
            AND m.state ='processed'
            AND f.renameium_state=false
            ORDER BY f.\"createdAt\";""")
        rows = curr.fetchall()
        curr.close()
        rows = list(map(lambda x: Movie(*x), rows))
        return rows
    except (Exception, Db.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def get_shows():
    """" Query all shows from the table, returning a list of Show objects """

    conn = None
    try:
        conn = connect()
        curr = conn.cursor()
        curr.execute("""
            SELECT tv.\"tvShowId\", tv.\"seasonNumber\", tv.\"episodeNumber\", s.title, f.\"createdAt\", f.path, f.id
            FROM tv_episode as tv
            JOIN tv_show as s ON tv.\"tvShowId\"=s.id
            JOIN file AS f ON f.\"tvEpisodeId\"=tv.id
            WHERE f.\"tvEpisodeId\" IS NOT NULL
            AND tv.state='processed'
            AND f.renameium_state=false
            ORDER BY f.\"createdAt\";
        """)
        rows = curr.fetchall()
        curr.close()
        rows = list(map(lambda x: Show(*x), rows))
        return rows
    except (Exception, Db.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')