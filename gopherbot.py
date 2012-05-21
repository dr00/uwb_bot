#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Author: Dom Roselli (droselli)
# Course: CSS 490 - Spring 2012
from twitter.api import Twitter, TwitterError, TwitterHTTPError
from twitter.oauth import OAuth, write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

import os
import sys
import json
import urllib2

CONSUMER_KEY = 'uS6hO2sV6tDKIOeVjhnFnQ'
CONSUMER_SECRET = 'MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk'
DEFAULT_LASTID = 0
DEFAULT_LASTIDFILE = '{}{}.twitter_lastid'.format(os.environ['HOME'], os.sep)
DEFAULT_OAUTHFILE = '{}{}.twitter_oauth'.format(os.environ['HOME'], os.sep)
DEFAULT_USERNAME = 'AnOrangeEater'

class GopherBot:
    BASE_URL = 'http://api.twitter.com'
    USER_LOOKUP_URL = '{}/{}'.format(BASE_URL, '1/users/lookup.json?user_id=')
    
    def __init__(self, username, lastid_filename, oauth_filename):
        # Get the lastid and oauth tokens used to call the Twitter API
        self.lastid_filename = lastid_filename
        self.lastid = self.get_lastid(lastid_filename)        
        self.username = username
        
        t, ts = self.get_oauth_tokens(oauth_filename)
        self.oauth_token = t
        self.oauth_token_secret = ts
        
        self.twitter_auth = None
        if self.is_valid_oauth(self.oauth_token, self.oauth_token_secret):
            self.twitter_auth = OAuth(self.oauth_token, 
                                      self.oauth_token_secret,
                                      CONSUMER_KEY,
                                      CONSUMER_SECRET)
        else:
            print('Could not authenticate invalid oauth tokens')


    
    def get_users(self, user_ids):
        """
        Gets and returns the user json objects from Twitter.
        """
        lookup_url = self.USER_LOOKUP_URL
        params = ','.join([str(id) for id in user_ids])
        url = '{0}{1}'.format(lookup_url, urllib2.quote(params))
        yield self.get_json_obj(url)
            

    def get_json_obj(self, url):
        """
        Gets the JSON object at the specified url.
        Returns and empty list if the call failed.
        """
        json_list = []
        try:
            f = urllib2.urlopen(url)
            response = f.read()
            json_list = json.loads(response)
        except urllib2.URLError as e:
            print(e)
        except ValueError as e:
            print(e)

        return json_list

    
    def save_to_file(self, json_obj, filename, mode):
        """
        Save the json object to a text file for later
        """
        with open(filename, mode) as f:
            f.write(json_obj)
    
    
    def get_lastid(self, lastid_filename):
        """
        Gets the lastid value from the lastid_filename (if exists)
        Otherwise, returns the default lastid
        """
        lastid = ''
        try:
            with open(lastid_filename, 'r') as f:
                lastid = f.readline()
        except IOError:
            lastid = DEFAULT_LASTID

        if not isinstance(lastid, (int, long)):
            lastid = DEFAULT_LASTID

        return lastid
        

    def get_oauth_tokens(self, oauth_filename):
        """
        Gets the oauth_token and oauth_token_secret from the oauth_filename.
        Returns empty strings for both if the we cannot find them or the user
        doesn't want to create new ones.
        """
        try:
            with open(oauth_filename, 'r') as f:
                t, ts = read_token_file(oauth_filename)
        except IOError:
            print 'OAuth file {} not found'.format(oauth_filename)
            request = 'Do you want to initiate a new oauth dance (y or n)? '
            response = raw_input(request)

            if len(response) > 0 and response[0].upper() == 'Y':
                t, ts = oauth_dance('Autoecho Tool', CONSUMER_KEY,
                                    CONSUMER_SECRET, oauth_filename)
            else:
                t = ts = ''

        return t, ts

   
    def get_tweets(self, username, lastid):
        """
        Gets the tweets of username starting at lastid using the Twitter Search API
        """
        tweets = None
        try:
            ts = self.get_twitter_search()
            tweets = ts.search(q=username, since_id=lastid)
        except TwitterHttpError, e:
            errormsg = 'Call to Twitter Search API Failed!\n'
            print(errormsg)

        return tweets


    def get_twitter_search(self):
        """
        Returns Twitter object used for searching.
        """
        return Twitter(domain='search.twitter.com')
    

    def get_twitter_api(self, oauth_token=None, oauth_token_secret=None):
        """
        Returns a Twitter object to be used for various Twitter API calls.
        """
       
        twitter_api = None
        if oauth_token and oauth_token_secret:
            twitter_api = Twitter(auth=self.twitter_auth, secure=True,
                              api_version='1', domain='api.twitter.com')
        else:
            if self.is_valid_oauth(oauth_token, oauth_token_secret):
                my_auth = OAuth(oauth_token, oauth_token_secret,
                                    CONSUMER_KEY, CONSUMER_SECRET)
        
                twitter_api = Twitter(secure=True, api_version='1',
                                      domain='api.twitter.com')

        return twitter_api  
   

    def is_valid_oauth(self, oauth_token, oauth_token_secret):
        """
        Returns True if the oauth tokens passed in are valid and False if not.
        """
        if oauth_token == '' or oauth_token_secret == '':
            return False
        else:
            return True


    def get_tweets(self, username, lastid):
        """
        Gets the tweets of username starting at lastid using the Twitter Search API
        """
        tweets = None
        try:
            ts = self.get_twitter_search()
            tweets = ts.search(q=username, since_id=lastid)
        except TwitterHttpError, e:
            errormsg = 'Call to Twitter Search API failed!\n'
            print(errormsg)

        return tweets
        
    
    def get_followers(self, screen_name):
        """
        Gets the tweets of username starting at lastid using the Twitter Search API
        """
        followers = None
        
        try:
            api = self.get_twitter_api()
            return api.followers.ids(screen_name=screen_name)
        except TwitterHttpError, e:
            errormsg = 'Call to Twitter followers/ids failed!\n'
            print(errormsg)


    def save_lastid(self, lastid, lastid_filename):
        """
        Saves the lastid value to the lastid_filename.
        """
        try:
            with open(lastid_filename, 'w') as f:
                f.write(lastid)
        except IOError:
            errormsg = ('\nCould not write lastid {0}'
                        'to {1}\n'.format(lastid, lastid_filename))
            print(errormsg)

