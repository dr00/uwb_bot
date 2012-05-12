#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from pprint import pprint

import urllib2
import json
import sys

IP_ADDR = '192.168.0.1'
REFERER = 'uwb.edu'

class GoogleNewsResults:
    """
    Wraps the JSON results from the Google News API into a class.
    """
    
    """
    Dnyamically create the attributes for this class using setattr
    Protects us from changes in the results (and less code!)
    
    JSON reference: https://developers.google.com/news-search/v1/jsondevguide#json_reference
    Example:
    google = GoogleNews(IP_ADDR, REFERER)
    json_results = google.get_topic_topheadlines()
    
    results = [GoogleNewsResults(r) for r in json_results]
    result0 = results[0]
    
    # print the headline title
    print(result0.title)
    
    # print the headline unescaped url
    print(result0.unescapedUrl)
        
    # print the title of all the headline's related stories
    for rs in result0.relatedStories:
        print(rs.title)
        
    """
    def __init__(self, json_result):
        for k, v in json_result.items():
            
            if k == 'relatedStories':
                self.relatedStories = [GoogleNewsRelatedStory(rs) for rs in json_result[k]]
                continue

            # Don't process image (who cares) or any other dictionary type, 
            # other than 'relatedStories' (above)
            if k == 'image' or type(json_result[k]) == type({}):
                continue
                
            setattr(self, k, v)


class GoogleNewsRelatedStory:
    """
    Wraps the JSON results of the related news story from the results of a query.
    """
    def __init__(self, rs):
        for k, v in rs.items():
            setattr(self, k, v)    

class GoogleNews:
    """
    Provides access to the Google News API
    """
    def __init__(self, ipaddr, referer):
        self.ipaddr = ipaddr
        self.referer = referer
        self.url = ('https://ajax.googleapis.com/ajax/services/search/news?' +
                    'v=1.0&userip={0}'.format(ipaddr))

    def get_topic_topheadlines(self):
        """
        Gets the top headlines.
        """
        params = {'topic': 'h'}
        return self._call_api(self.url, params)
        
    def get_topic_world(self):
        """
        Gets the world news topics.
        """
        params = {'topic': 'w'}
        return self._call_api(self.url, params)
    
    def get_topic_scitech(self):
        """
        Gets the science and technology news topics.
        """
        params = {'topic': 't'}
        return self._call_api(self.url, params)
        
    def get_topic_politics(self):
        """
        Gets the political news topics.
        """
        params = {'topic': 'p'}   
        return self._call_api(self.url, params)
        
    def get_topic_entertainment(self):
        """
        Gets the entertainment news topics.
        """
        params = {'topic': 'e'}
        return self._call_api(self.url, params)
                    
    def get_topic_nation(self):
        """
        Gets the national news topics.
        """
        params = {'topic': 'n'}
        return self._call_api(self.url, params)
            
    def get_topic_elections(self):
        """
        Gets the election news topics.
        """
        params = {'topic': 'el'}
        return self._call_api(self.url, params)
        
    def get_adhoc_query(self, query):
        params = {'q': urllib2.quote(query)}   
        return self._call_api(self.url, params)
        
    def _call_api(self, url, params):
        """
        Calls the Google News API and returns the results as a list of 
        JSON data used to create GoogleNewsResults objects
        """
        print(type(params))
        paramlist = ["{}={}".format(k,v) for k, v in params.items()]
        queryurl = '{0}&{1}'.format(url, '&'.join(paramlist))
        if sys.flags.debug:
            pprint(queryurl)

        try:
            request = urllib2.Request(queryurl, None, {'Referer': REFERER})
            r = urllib2.urlopen(request)
            response = r.read()

            # Process the JSON string.
            return json.loads(response)['responseData']['results']
        # TODO: Better error handline
        except Error as e:        
            pprint(e)

if __name__ != '__main__':
    if sys.flags.debug:
        google = GoogleNews(IP_ADDR, REFERER)
        json_results = google.get_topic_topheadlines()
        
        results = [GoogleNewsResults(r) for r in json_results]
        obamaresults = google.get_adhoc_query('barrack obama')
    
    

