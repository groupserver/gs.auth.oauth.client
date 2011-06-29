# Partially borrowed from django_social_auth
import cgi
import urllib
import simplejson

FACEBOOK_SERVER = "graph.facebook.com"
FACEBOOK_AUTHORIZATION_URI = "https://%s/oauth/authorize" % FACEBOOK_SERVER
FACEBOOK_ACCESS_TOKEN_URI = "https://%s/oauth/access_token" % FACEBOOK_SERVER
FACEBOOK_CHECK_AUTH = "https://%s/me" % FACEBOOK_SERVER

def auth_url(redirect_uri, client_id, scope=('email',)):
    """ Return URL which will initiate oauth authentication.

    """
    params = {'redirect_uri': redirect_uri,
              'client_id': client_id,
              'scope': ','.join(scope)}
        
    return FACEBOOK_AUTHORIZATION_URI+'?'+urllib.urlencode(args)

class FacebookAuth:
    def __init__(self, redirect_uri, client_id, scope=('email',)):
        self.redirect_uri = redirect_uri
        self.client_id = client_id,
        self.scope = scope

    def complete_auth(self, request):
        """ Finish second stage of oauth2 dance.

        """
        self.access_token = None
        if 'code' in self.request:
            params = {'redirect_uri': self.redirect_uri,
                      'client_id': self.client_id,
                      'scope': ','.join(self.scope),
                      'code': self.request['code']}

            url = FACEBOOK_ACCESS_TOKEN_URI+'?'+urllib.urlencode(params)
            response = cgi.parse_qs(urllib.urlopen(url).read())
            self.access_token = response['access_token'][0]
    
    def data(self):
        """ Retrieve user data from service.
        
        """
        params = {'access_token': self.access_token}
        url = FACEBOOK_CHECK_AUTH+'?'+urllib.urlencode(params)
        return simplejson.load(urllib.urlopen(url))      

   
