# Partially borrowed from django_social_auth
import cgi
import urllib
import simplejson
import base64
import logging
log = logging.getLogger("gs.auth.oauth.client")

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

    return FACEBOOK_AUTHORIZATION_URI+'?'+urllib.urlencode(params)


def encode_parameters(params):
    return base64.urlsafe_b64encode(urllib.urlencode(params))


def decode_parameters(s):
    return base64.urlsafe_b64decode(s)


class FacebookAuth:
    def __init__(self, redirect_uri, client_id, client_secret, scope=('email',)):
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope

    def complete_auth(self, request):
        """ Finish second stage of oauth2 dance.

        """
        self.access_token = None
        if 'code' in request:
            params = {'redirect_uri': self.redirect_uri,
                      'client_id': self.client_id,
                      'client_secret': self.client_secret,
                      'code': request['code']}

            url = FACEBOOK_ACCESS_TOKEN_URI+'?'+urllib.urlencode(params)
            response = cgi.parse_qs(urllib.urlopen(url).read())
            try:
                self.access_token = response['access_token'][0]
                log.info('Received access token from facebook')
            except KeyError:
                log.error('Did not receive access token from facebook, instead: %s' % response)

    def data(self):
        """ Retrieve user data from service."""
        params = {'access_token': self.access_token}
        url = FACEBOOK_CHECK_AUTH+'?'+urllib.urlencode(params)
        userdata = simplejson.load(urllib.urlopen(url))
        log.info('Received user data from facebook: %s' % userdata)
        return userdata
