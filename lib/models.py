from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column (Integer(), primary_key=True)
    title = Column (String())
    plot = Column (String())

    movie_genres = relationship("MovieGenre", back_populates="movie")
    genres = association_proxy("movie_genres", "genre", creator=lambda g: MovieGenre(genre=g))

    casts = relationship("Cast", back_populates="movie")
    actors = association_proxy("casts", "actor", creator=lambda a: Cast(actor=a))

    faves = relationship("Fave", back_populates="movie")
    users = association_proxy("faves", "user", creator=lambda u: Fave(user=u))

    def __repr__(self):
        return f"{self.id}: {self.title}"

class Genre(Base):
    __tablename__ = "genres"
    id = Column (Integer(), primary_key=True)
    name = Column (String())

    movie_genres = relationship("MovieGenre", back_populates="genre")
    movies = association_proxy("movie_genres", "movie", creator=lambda m: MovieGenre(movie=m))

    def __repr__(self):
        return f"{self.name}"

class Actor(Base):
    __tablename__ = "actors"
    id = Column (Integer(), primary_key=True)
    name = Column (String())

    casts = relationship("Cast", back_populates="actor")
    movies = association_proxy("casts", "movie", creator=lambda m: Cast(movie=m))

    def __repr__(self):
        return f"{self.id}: {self.name}"

class MovieGenre(Base):
    __tablename__ = "movie_genres"

    id = Column (Integer(), primary_key=True)
    movie_id = Column (Integer(), ForeignKey("movies.id"))
    genre_id = Column (Integer(), ForeignKey("genres.id"))

    movie = relationship("Movie", back_populates="movie_genres")
    genre = relationship("Genre", back_populates="movie_genres")

class Cast(Base):
    __tablename__ = "casts"

    id = Column (Integer(), primary_key=True)
    movie_id = Column (Integer(), ForeignKey("movies.id"))
    actor_id = Column (Integer(), ForeignKey("actors.id"))
    role = Column (String())

    movie = relationship("Movie", back_populates="casts")
    actor = relationship("Actor", back_populates="casts")

    def __repr__(self):
        return f"{self.actor.name}: {self.role}"

class User(Base):
    __tablename__ = "users"
    id = Column (Integer(), primary_key=True)
    name = Column (String())

    faves = relationship("Fave", back_populates="user")
    movies = association_proxy("faves", "movie", creator=lambda m: Fave(movie=m))
    
    def __repr__(self):
        return f"{self.id}: {self.name}"

class Fave(Base):
    __tablename__ = "faves"

    id = Column (Integer(), primary_key=True)
    user_id = Column (Integer(), ForeignKey("users.id"))
    movie_id = Column (Integer(), ForeignKey("movies.id"))

    movie = relationship("Movie", back_populates="faves")
    user = relationship("User", back_populates="faves")

    def __repr__(self):
        return f"{self.movie.id}. {self.movie.title}"