import os
import datetime
import psycopg2

from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIES_TABLE = """
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        title TEXT,
        release_timestamp REAL
    );
    """

CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY
    );
    """

CREATE_WATCHED_TABLE = """
    CREATE TABLE IF NOT EXISTS watched (
        user_username TEXT,
        movie_id INTEGER,
        FOREIGN KEY(user_username) REFERENCES users(username),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    );
    """
    
INSERT_MOVIES = """
    INSERT INTO movies (title, release_timestamp)
    VALUES (%s, %s);
    """
    
DELETE_MOVIES = """
    DELETE FROM movies 
    WHERE title = %s;
    """

SELECT_ALL_MOVIES = """
    SELECT * 
    FROM movies;
    """

SELECT_UPCOMING_MOVIES = """
    SELECT * 
    FROM movies 
    WHERE release_timestamp > %s;
    """

INSERT_USER = """
    INSERT INTO users (username)
    VALUES(%s);
    """
    
INSERT_WACTHED_MOVIE = """
    INSERT INTO watched (user_username, movie_id) 
    VALUES (%s, %s);
    """

SELECTED_WATCHED_MOVIES = """
    SELECT movies.* 
    FROM users 
    JOIN watched ON users.username = watched.user_username
    JOIN movies ON watched.movie_id = movies.id
    WHERE users.username = %s;
    """
    
SEARCH_MOVIE = """
    SELECT *
    FROM movies
    WHERE title LIKE %s;
    """

connection =  psycopg2.connect(os.environ["DATABASE_URL"])

def create_table() -> None: 
    with connection:
        with connection.cursor() as cursor:        
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
        
def add_movie(title: str, release_timestamp: float) -> None:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))
        
def get_movies(upcoming: bool=False) -> list:
    with connection:
        with connection.cursor() as cursor:            
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()
        
def watch_movies(
    username: str,
    movie_id: str
    ) -> None:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WACTHED_MOVIE, (username, movie_id))
        # cursor = connection.cursor()    
        # movies = get_movies()
        # movie_titles = []
        
        # for movie in movies:
        #     movie_titles.append(movie[0])
        # if title in movie_titles:
        #     cursor.execute(SET_MOVIE_WATCHED, (title,))
        #     print("The movie sucessfully added.")
        # else:
        #     print("Warning : No movie with the title in database.")
        #     print("Please input the movie in advance.")

def get_watched_movies(username) -> list:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECTED_WATCHED_MOVIES, (username,))
            return cursor.fetchall()
    
def search_movies(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIE, (f"%{search_term}",))
            return cursor.fetchall()

def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))