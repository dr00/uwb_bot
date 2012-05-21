from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, exists
from sqlalchemy import func

from datetime import datetime, timedelta
from email.utils import parsedate_tz

import sys
import json

_DB = 'sqlite:///twitterbotdb.sqlite'

Base = declarative_base()

class TwitterBotDB:

    def __init__(self, db=_DB, echo=False):
        # initialize the db engine, session, and metadata
        self.Base = Base
        self.engine = create_engine(db, echo=echo)
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


    ###########################################################################
    ##                       TWITTERBOTDB USER API                           ##
    ###########################################################################
    def user_select_by_id(self, id):
        """Get the User object by it's Twitter id.
        """
        try:
            id = long(id)
            return self.session.query(User).filter_by(id=id).first()
        except ValueError:
            raise ValueError('id is not an integer')
    

    def user_select_by_screen_name(self, screen_name):
        """Get the User object by the by it's Twitter screen_name.
        """
        if id.startswith('@'):
            id = id[1:]
            
        return self.session.query(User).\
                   filter(func.lower(User.screen_name)==func.lower(screen_name)).\
                   first()


    def user_select_by_ids_all(self, ids):
        """Get a list of User objects by their Twitter id's.
        """
        if type(ids) is not type([]):
            raise TypeError('ids should be of type list')
        
        if ids:
            try:
                ids = [long(id) for id in ids]                
                return self.session.query(User).filter(User.id.in_(ids)).all()
            except ValueError:                
                raise ValueError('ids list contains non-integer values')
        else:
            raise RuntimeError('No users to select. ids list is empty')

    
    def user_select_by_screen_names_all(self, screen_names):    
        if type(screen_names) is not type([]):
            raise TypeError('screen_names should be of type list')

        if screen_names:
            return self.session.query(User).\
                    filter(func.lower(User.screen_name).\
                    in_(func.lower(screen_names))).\
                    all()


    def user_insert(self, user_json):
        """Insert the User object as described by the json object.
        """
        if type(user_json) is not type({}):
            raise TypeError('user_json should be of type dict')

        # Don't insert duplicate User.id!
        #TODO: Fix. This sucks, but I can't tell how to do this via SQL yet
        uid = user_json['id']
        exists = [id for id in self.session.query(User.id).where(User.id==uid)]

        user = None
        if uid not in exists:
            user = User(user_json)
        
        if user:           
            self.session.add(user)
            self.session.commit()
            self.session.flush()
        else:
            raise RuntimeError('No user to insert. Is user_json empty?')
            self.session.rollback()


    def user_insert_all(self, user_json):
        """Insert the User objects as described by the list of json objects.
        """

        if type(user_json) is not type([]):
            raise TypeError('user_json should be of type list')

        # Don't insert duplicate User.id!
        #TODO: Fix. This sucks, but I can't tell how to do this via SQL yet
        existing = [id for id in self.session.query(User.id)]
        users = [User(u) for u in user_json if u['id'] not in existing]
        
        if users:
            self.session.add_all(users)
            self.session.commit()
            self.session.flush()
        else:        
            raise RuntimeError('No users to insert. Is user_json empty?')
            self.session.rollback()

    
    def targetuser_insert_all(self, targetusers):
        if type(targetusers) is not type([]):
            raise TypeError('targetusers should be of type list')

        existing = [tu[0] for tu in self.session.query(TargetUser.id)]
        tu = [TargetUser(id) for id in targetusers if id not in existing]

        if tu:
            self.session.add_all(tu)
            self.session.commit()
            self.session.flush()
        else:
            raise RuntimeError('No targetusers to insert.')
            self.session.rollback()
        

    ###########################################################################
    ##                       TWITTERBOTDB TWEET API                          ##
    ###########################################################################
    '''
    def tweet_select_by_user_id(self, id):
        """Get the User's Tweet objects by it's Twitter User id.
        """
        try:
            id = long(id)
            return self.session.query(Tweet).filter(Tweet.users.id(id=id).first()
        except ValueError:
            raise ValueError('id is not an integer')
            

    def tweet_select_by_screen_name(self, screen_name):
        """Get the User's Tweet objects by it's Twitter screen_name.
        """
        if id.startswith('@'):
            id = id[1:]
            
        return self.session.query(Tweet).\
                   filter(lower(Tweet.users.screen_name)==lower(screen_name)).\
                   first()
   '''


            



######################
## GLOBALS
######################
def to_datetime(datestring):
    """Converts the datetime string to a datetime python object.
    """
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])


class TargetUser(Base):
    __tablename__ = 'targetusers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    user = relationship('User')
    
    def __init__(self, id):
        self.id = id
 
    def __repr__(self):
        u = self.user
        id = u.id
        name = u.name.encode('utf-8', 'ignore')
        created_at = u.created_at
        r = "<User('{}','{}', '{}')>".format(id, name, created_at)
        return r


class User(Base):
    __tablename__ = 'users'
    
    # attributes definitions
    id = Column(Integer, primary_key=True)
    id_str = Column(String, nullable=False, default='0')
    created_at = Column(DateTime, nullable=False)
    default_profile = Column(Boolean)
    default_profile_image = Column(Boolean)
    description = Column(String)
    favourites_count = Column(Integer, nullable=False, default='0')
    follow_request_sent = Column(Boolean)
    followers_count = Column(Integer, nullable=False, default='0')
    friends_count = Column(Integer, nullable=False, default='0')
    geo_enabled = Column(Boolean)
    is_translator = Column(Boolean)
    lang = Column(String)
    listed_count = Column(Integer)
    location = Column(String)
    name = Column(String)
    protected = Column(Boolean)
    screen_name = Column(String)
    statuses_count = Column(Integer)
    time_zone = Column(String)
    url = Column(String)
    utc_offset = Column(Integer)
    verified = Column(Boolean)
    
    # relationship definitions
    tweets = relationship('Tweet', backref=backref('user', lazy='joined'))

    def __init__(self, user_json):
        self.created_at = to_datetime(user_json['created_at'])
        self.id = user_json['id']
        self.id_str = user_json['id_str']
        self.default_profile = user_json['default_profile']
        self.default_profile_image = user_json['default_profile_image']
        self.description = user_json['description']
        self.favourites_count = user_json['favourites_count']
        self.follow_request_sent = user_json['follow_request_sent']
        self.followers_count = user_json['followers_count']
        self.friends_count = user_json['friends_count']
        self.geo_enabled = user_json['geo_enabled']
        self.is_translator = user_json['is_translator']
        self.lang = user_json['lang']
        self.listed_count = user_json['listed_count']
        self.location = user_json['location']
        self.name = user_json['name']
        self.protected = user_json['protected']
        self.screen_name = user_json['screen_name']
        self.statuses_count = user_json['statuses_count']
        self.time_zone = user_json['time_zone']
        self.url = user_json['url']
        self.utc_offset = user_json['utc_offset']
        self.verified = user_json['verified']        

    def __repr__(self):
        id = self.id
        name = self.name.encode('utf-8', 'ignore')
        created_at = self.created_at
        r = "<User('{}','{}', '{}')>".format(id, name, created_at)
        return r


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    id_str = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    favorited = Column(Boolean)
    in_reply_to_screen_name = Column(String)
    in_reply_to_status_id = Column(Integer)
    in_reply_to_status_id_str = Column(String)
    in_reply_to_user_id = Column(Integer)
    in_reply_to_user_id_str = Column(String)
    possibly_sensitive = Column(Boolean)
    retweet_count = Column(Integer, nullable=False, default='0')
    retweeted = Column(Boolean)
    source = Column(String)
    text = Column(String, nullable=False)
    truncated = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))

    #coordinate_id = Column(Integer)
    #category_id = Column(Integer)
    #entities
    #coordinates
    #media_entity_id = Column(Integer, ForeignKey("tweet_media_entities.id"))
    #url_entity_id = Column(Integer, ForeignKey("tweet_url_entities.id"))
    #hashtag_entity_id = Column(Integer, ForeignKey("tweet_hashtag_entities.id"))

    #TODO: COMPLETE RELATIONSHIP DEFINITIONS
    #tweet_media_entity = relationship('MediaEntity', secondary=tweet_media_entities,
    #                                  backref=backref('tweets', lazy='dynamic')
    
    
    def __init__(self, tweet_json):
        self.id = tweet_json['id']
        self.id_str = tweet_json['id_str']
        self.created_at = to_datetime(tweet_json['created_at'])
        self.favorited = tweet_json['favorited']
        self.in_reply_to_screen_name = tweet_json['in_reply_to_screen_name']
        self.in_reply_to_status_id = tweet_json['in_reply_to_status_id']
        self.in_reply_to_status_id_str = tweet_json['in_reply_to_status_id_str']
        self.in_reply_to_user_id = tweet_json['in_reply_to_user_id']
        self.in_reply_to_user_id_str = tweet_json['in_reply_to_user_id_str']
        self.retweet_count = tweet_json['retweet_count']
        self.retweeted = tweet_json['retweeted']
        self.source = tweet_json['source']
        self.text = tweet_json['text']
        self.truncated = tweet_json['truncated']

        # SPECIAL
        self.user_id = tweet_json['user']['id']

    
    def __repr__(self):
        id = self.id
        text = self.text.encode('utf-8', 'ignore')
        created_at = self.created_at
        r = u"<Tweet('{}','{}', '{}')>".format(id, text, created_at)
        return r
        

