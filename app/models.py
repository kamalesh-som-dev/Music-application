from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext

Base = declarative_base()
    
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    
    playlists = relationship("Playlist", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Song(Base):
    __tablename__ = "songs"

    song_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String, index=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    album_id = Column(Integer, ForeignKey('albums.album_id'))
    genre_id = Column(Integer, ForeignKey('genres.genre_id'))
    recommendation_count = Column(Integer, default=0)

class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    artist_name = Column(String, index=True)
    songs = relationship("Song", backref="artist")
    
class Album(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    album_title = Column(String, index=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    songs = relationship("Song", backref="album")

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    genre_name = Column(String, index=True)
    songs = relationship("Song", backref="genre")

class Playlist(Base):
    __tablename__ = "playlists"

    playlist_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    playlist_name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    song_ids = Column(ARRAY(Integer))

    user = relationship("User", back_populates="playlists")

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    song_id = Column(Integer, ForeignKey('songs.song_id'))
    rating = Column(Float)  

    user = relationship("User", back_populates="ratings")

class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('users.user_id'))
    receiver_id = Column(Integer)
    recommendation_type = Column(String)
    recommendation_type_id = Column(Integer)

def create_tables(engine):
    Base.metadata.create_all(bind=engine)
    