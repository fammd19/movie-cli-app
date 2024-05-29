from env import session, clear
from models import Movie, Actor, Genre, MovieGenre, Cast, User, Fave

logged_user = None


def heading(text):
    print("*"*30)
    print(text)
    print("*"*30)

def handle_yes_no(message):
    returned_val = True
    while True:
        print(message)
        choice = input()

        if choice.lower() == "yes" or choice.lower() == "y":
            returned_val = True
            break
        elif choice.lower() == "no" or choice.lower() == "n":
            returned_val = False
            clear()
            break
        else:
            print(Fore.RED + "Invalid input" + Style.RESET_ALL)
    return returned_val

def main_menu():
    heading("MAIN MENU")

    print("all   - display all movies")
    print("genre - search movies by genre")
    print("actor - search movies by actor")
    print('faves - display all faves')
    print('exit  - terminate the program')

    print("\nPlease enter you menu choice:")
    return input()


def login(username):
    user = session.query(User).filter(User.name == username).first()

    if not user:
        user = User(name = username)
        session.add(user)
        session.commit()
        print("You have successfully registered for the app!")

    else:
        print(f"Welcome back, {user.name}")

    global logged_user
    logged_user = user


def faves():
    clear()

    heading("WATCH LIST")

    if logged_user.movies:
        for fave_movie in logged_user.movies:
            print(fave_movie)

    else:
        print("No movies in the watch list")

    input("Press enter to continue")

    

def greet():
    clear()
    print("Welcome to the Movie CLI App")
    print("Please enter your username")
    username = input()

    login(username)


def add_to_fave(movie):
    choice = handle_yes_no("Would you like to add this to your watch list (yes/no)?")
    if choice:
        new_fave = Fave(movie_id = movie.id, user_id = logged_user.id)
        session.add(new_fave)
        session.commit()
        print("\nYou have successfully added this to your watch list")

def display_movies(movies, heading_msg):
    loop = True

    while loop:
        heading(heading_msg)
        
        if len(movies)>0:
            for movie in movies:
                print(movie)
        else: 
            print("No movie...")

        print("-"*30)
        print("\nPlease enter the movie ID to view more details (type 'back' to go back):")
        id_input = input()

        if id_input.lower() != "back":
            movie_id = int(id_input)

            movie = [ m for m in movies if m.id == movie_id ]

            if len(movie)>0:
                movie = movie[0]
                clear()

                print(f"{movie.title.upper()}")
                print(f"Genres:")
                print(f"{movie.genres}")
                print(f"Cast:")
                for actor in movie.actors:
                    cast = session.query(Cast).filter(Cast.actor_id == actor.id, Cast.movie_id == movie.id).first()
                    print(cast)
                print(f"Plot:")
                print(f"{movie.plot}")

                add_to_fave(movie)

            else: 
                print("No movie found")
        
        else:
            clear()
            loop = False
            return False
                    
def all():
    movies = session.query(Movie).all()

    return display_movies(movies,"ALL MOVIES")


def genre():
    print("\nPlease enter a genre:")
    genre_input = input()
    genre = session.query(Genre).filter(Genre.name.like(genre_input)).first()

    if genre:
        display_movies(genre.movies, f"MOVIES UNDER {genre.name}")
    
    else:
        print("No genre found")


def actor():
    print("\nPlease enter an actor's name:")
    actor_input = input()
    actor = session.query(Actor).filter(Actor.name.like(actor_input)).first()

    if genre:
        display_movies(actor.movies, f"FILMS FOR {actor.name.upper()}")
    
    else:
        print("No genre found")

def start():
    greet()
    loop = True
    while loop:
        choice = main_menu()
        while True:
            if choice.lower() == 'all':
                all()
                break
            elif choice.lower() == 'genre':
                clear()
                genre()
                break
            elif choice.lower() == 'actor':
                clear()
                actor()
                break
            elif choice.lower() == 'faves':
                clear()
                faves()
                break
            elif choice.lower() == 'exit' or choice.lower() == 'quit':
                loop = False
                break
            else:
                print("Invalid input. Please try again!")

    print("Thank you for using the Movies DB App. Goodbye!")

if __name__ == "__main__":
    start()