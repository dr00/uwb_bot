#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref

import sys

Base = declaritive_base()     


class TwitterBotDB:
    def __init__(self, db_filename)
        engine = create_engine('sqlite:///:{0}'.format(db_filename), echo=False)
        Base = declaritive_base()
        Base.metadata.create_all(engine)
        #TODO: COMPLETE DEFINITION
        
        
class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    id_str = Column(String)
    created_at = Column(DateTime)
    favorited = Column(Bool)
    in_reply_to_screen_name = Column(String)
    in_reply_to_status_id = Column(Integer)
    in_reply_to_status_id_str = Column(String)
    n_reply_to_user_id = Column(Integer)
    in_reply_to_user_id_str = Column(String)
    possibly_sensitive = Column(Bool)
    retweet_count = Column(Integer)
    retweeted = Column(Bool)
    source = Column(String)
    text = Column(String)
    truncated = Column(Bool)
    user = Column(Integer)
    coordinate_id = Column(Integer)
    category_id = Column(Integer)
    media_entity_id = Column(Integer, ForeignKey("tweet_media_entities.id"))
    url_entity_id = Column(Integer, ForeignKey("tweet_url_entities.id"))
    hashtag_entity_id = Column(Integer, ForeignKey("tweet_hashtag_entities.id"))

    #TODO: COMPLETE RELATIONSHIP DEFINITIONS
    tweet_media_entity = relationship('MediaEntity', secondary=tweet_media_entities,
                                      backref=backref('tweets', lazy='dynamic')

    def __init__(self, tweet_json):
        # loop through each key and assign
        pass
    
    def __repr__(self):
        r = "<User('{}','{}', '{}')>".format(self.id, self.text, self.created_at)
        return r


class UrlEntity(Base):
    __tablename__ = 'url_entities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text, nullable=False, unique=True)
    display_url = Column(Text)
    expanded_url = Column(Text)

    #TODO: COMPLETE RELATIONSHIP DEFINITIONS
    
    
class HashtagEntity(Base):
    __tablename__ = 'hashtag_entities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hashtag = Column(Text, nullable=False, unique=True)

    #TODO: COMPLETE RELATIONSHIP DEFINITIONS
    
    
class MediaEntity(Base):
    __tablename__ = "media_entities" 

    id = Column(Integer, primary_key=True)
    id_str = Column(String)
    media_url_https = Column(Text)
    url = Column(Text)
    display_url = Column(Text)
    expanded_url = Column(Text)
    type = Column(Text, server_default=text('photo'))

    #TODO: COMPLETE RELATIONSHIP DEFINITIONS
    
    
class CannedTweet(Base):
    __tablename__ = 'canned_tweets'

    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String, nullable=False)
    topic = Column(String)
    tone = Column(String)
    context = Column(String)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    id_str = Column(String)
    created_at = Column(DateTime)
    default_profile = Column(Boolean)
    default_profile_image = Column(Boolean)
    description = Column(Text)
    favourites_count = Column(Text)
    follow_request_sent = Column(Boolean)
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    geo_enabled = Column(Boolean)
    is_translator = Column(Boolean)
    lang = Column(Text)
    listed_count = Column(Integer)
    location = Column(Text)
    name = Column(Text)
    protected = Column(Boolean)
    screen_name = Column(Text)
    statuses_count = Column(Integer)
    time_zone = Column(Text)
    url = Column(Text)
    utc_offset = Column(Integer)
    verified = Column(Boolean)

    #TODO: COMPLETE RELATIONSHIP DEFINITIONS

## TABLE DEFINITIONS
tweet_hashtag_entities = Table('tweet_hashtag_entities', Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweets.id'))
    Column('hashtag_entity_id', Integer, ForeignKey('hashtag_entities.id'))


tweet_media_entities = Table('tweet_media_entities', Base.metadata, 
    Column('tweet_id', Integer, ForeignKey('tweets.id'))
    Column('media_entity_id', Integer, ForeignKey('media_entities.id'))


tweet_url_entities = Table('tweet_url_entities', Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweets.id'))
    Column('url_entity_id', Integer, ForeignKey('url_entities.id'))


users_bot_follows = Table('users_bot_follows', Base.metadata,
    Column('date_follows', DateTime, primary_key=True, 
           server_default=text('CURRENT_TIMESTAMP'))
    Column('user_id', Integer, ForeignKey('users.id'))


users_following_bot = Table('users_following_bot', Base.metadata,
    Column('date_following', DateTime, primary_key=True,
           server_default=text('CURRENT_TIMESTAMP'))
    Column('user_id', Integer, ForeignKey('users.id'))


users_targetuser_follows = Table('users_targetuser_follows', Base.metadata,
    Column('date_follows', DateTime, primary_key=True, 
           server_default=text('CURRENT_TIMESTAMP'))
    Column('targetuser_id', Integer, ForeignKey('users.id'))
    Column('follows_targetuser_id', Integer, ForeignKey('users.id'))


target_users = Table('target_users', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'))


tweet_usermention_entities = Table('tweet_url_entities', Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweets.id'))
    Column('user_id', Integer, ForeignKey('users.id'))
