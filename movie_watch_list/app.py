from platform import release
import database
import datetime

menu = """
\n
Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movie.
4) Watch a movie.
5) View watched movies.
6) Add new user.
7) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"

print(welcome)
database.create_table()


def prompt_add_movie():
    title = input("Please input the name of the movie : ")
    release_date = input("Please input the release date of the movie : ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()
    
    database.add_movie(title, timestamp)
    
def print_movie_list(heading, movies):
    print(f"-- {heading} movies --")
    for _id, title, release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime("%d %b %Y")
        print(f"{_id}: {title} (on {human_date})")
    print("---- \n")
    
def print_watched_movie_list(username, movies):
    print(f"-- {username}'s Watched Movies --")
    for movie in movies:
        print(f"{movie[1]}")
    print("----- \n")
    
def prompt_watch_movie():
    username = input("Username : ")
    movie_id = input("Movie ID : ")
    database.watch_movies(username, movie_id)

def prompt_show_watched_movies():
    username = input("Username : ")
    movies = database.get_watched_movies(username)
    if movies:
        print_watched_movie_list("Wached", movies)
    else:
        print("That user has watched no movies yet!")
    
def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)

while (user_input := input(menu)) != "7":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = database.get_movies(True)
        print_movie_list("Upcoming", movies)
    elif user_input == "3":
        movies = database.get_movies()
        print_movie_list("All", movies)
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        prompt_show_watched_movies()
    elif user_input == "6":
        prompt_add_user()
    else:
        print("Invalid input, please try again!")