from pprint import pprint

import sys
import json
import urllib2

class GopherBot:
    BASE_URL = 'http://api.twitter.com'
    USER_LOOKUP_URL = '{}/{}'.format(BASE_URL, '1/users/lookup.json?user_id=')
    
    def __init__(self):
        pass
    
    def get_users(self, user_ids):
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

    
    def save_to_file(json_obj, filename, mode):
        with open(filename, mode) as f:
            f.write(json_obj)
