from targetuser_ids import targetuser_ids
from pprint import pprint
from twitterbotdb import TwitterBotDB, User, Tweet, TargetUser
from gopherbot import GopherBot

import sys
import os

_MAX_USERS_REQ = 100
_MAX_TRIES = 5
_ECHO = True
_DEFAULT_LASTIDFILE = '{}{}.twitter_lastid'.format(os.environ['HOME'], os.sep)
_DEFAULT_OAUTHFILE = '{}{}.twitter_oauth'.format(os.environ['HOME'], os.sep)
_DEFAULT_USERNAME = 'AnOrangeEater'


def init_users(db, gopher, ids, limit_per_call, max_tries):
    if not targetuser_ids:
        raise RuntimeError('No targetusers to intitialize.')
        
    if max_tries < 1:
        raise RuntimeError('max_tries is less than 1. Nothing to try.')
    
    tries_left = max_tries
    limit = limit_per_call
    targets = ids
    s = db.session
    g = gopher
    
    if sys.flags.debug:
        print('max_tries:     {}'.format(max_tries))
        print('targets:       {}'.format(len(targets)))

    # somtimes I don't get all data requested from twitter, so use retry logic
    # max_tries + 1 for the insertion to the database on the last iteration   
    # initialize targetuser data
    #TODO: Fix. How to do this using ORM without return trips to db?        
    known = [u[0] for u in s.query(User.id)]
    missing = [t for t in targets if t not in known]

    if sys.flags.debug:
        print('known:         {}'.format(len(known)))
        print('missing:       {}'.format(len(missing)))

    # Make sure we have the target users in the User table before 
    # inserting the target user ids into the targetusers table
    print('missing {} ids'.format(len(missing)))
    tries_left += 1
    remaining = len(missing) / limit + (1 if len(missing) % limit else 0)
    if sys.flags.debug:
        print('tries_left:    {}'.format(tries_left))
        print('remaining:     {}'.format(remaining))

    while tries_left:        
        while remaining:
            for u in g.get_users(missing[:limit-1]):
                #g.save_to_file(u, 'targetusers.json', 'a')
                db.user_insert_all(u)
                known = [u[0] for u in s.query(User.id)]
                missing = [t for t in targets if t not in known]
                if sys.flags.debug:
                    print('tries_left:     {}'.format(tries_left))
                    print('now known:      {}'.format(len(known)))
                    print('still missing:  {}'.format(len(missing)))
            remaining -= 1
    
        tries_left -= 1

    if not tries_left and remaining:
        print(tries_left)
        raise RuntimeError('ran out of tries.')


"""
def init_followers(db, gopher, names, limit_per_call, max_tries):
    limit = limit_per_call
    for name in names:
        ids = gopher.get_followers(name)
        if ids:
            init_users(tdb, gopher, ids, limit, max_tries)
            known = [f for f in s.query(TargetUserFollower)]
            missing = [t for t in targetuser_ids if t not in known]
                if missing:
                    db.targetuser_insert_all(missing)

"""
if __name__ == '__main__':
    #status = main()
    status = -1
    sys.exit(status)
else:
    db_name = 'sqlite:///db/twitterbotdb.sqlite'
    print('Initializing database engine: {} ...'.format(db_name))        
    tdb = TwitterBotDB(db_name, _ECHO)
    s = tdb.session
    print('Session ready!')
    
    username = '@{0}'.format(_DEFAULT_USERNAME)
    lastid_filename = _DEFAULT_LASTIDFILE
    oauth_filename = _DEFAULT_OAUTHFILE 
    g = GopherBot(username, lastid_filename, oauth_filename)
    
    init_users(tdb, g, targetuser_ids, _MAX_USERS_REQ, _MAX_TRIES)
    
    known = [tu[0] for tu in s.query(TargetUser.id)]
    missing = [t for t in targetuser_ids if t not in known]
    if missing:
        tdb.targetuser_insert_all(missing)
    
    names = [n[0] for n in s.query(User.screen_name).join(TargetUser)]
    #init_followers(tdb, g, names, _MAX_USERS_REQ, _MAX_TRIES)
        

