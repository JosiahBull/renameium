#!/usr/bin/env python3

import config as config
import psycopg2 as Db

class Movie:
    def __init__(self, movieId, title, path, createdAt):
        self.movieId = movieId
        self.title = title
        self.path = path
        self.createdAt = createdAt


class Show:
    def __init__(self, showId, seasonNumber, episodeNumber, title, path, createdAt):
        self.showId = showId
        self.seasonNumber = seasonNumber
        self.episodeNumber = episodeNumber
        self.title = title
        self.path = path
        self.createdAt = createdAt

def connect():
    """ Connect to the PostgreSQL database server """
    # read connection parameters
    params = config.config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = Db.connect(**params)

    return conn

def get_movies():
    """ Query all movies from the table, returning a list of Movie objects """

    conn = None
    try:
        conn = connect()
        curr = conn.cursor()
        curr.execute("SELECT f.\"movieId\", m.title, f.\"createdAt\", f.path FROM file as f JOIN movie as m on f.\"movieId\"=m.id WHERE f.\"movieId\" IS NOT NULL AND m.state ='processed' ORDER BY f.\"createdAt\";")
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
        curr.execute("SELECT tv.\"tvShowId\", tv.\"seasonNumber\", tv.\"episodeNumber\", s.title, f.\"createdAt\", f.path FROM tv_episode as tv JOIN tv_show as s ON tv.\"tvShowId\"=s.id JOIN file AS f ON f.\"tvEpisodeId\"=tv.id WHERE f.\"tvEpisodeId\" IS NOT NULL AND tv.state='processed' ORDER BY f.\"createdAt\";")
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

