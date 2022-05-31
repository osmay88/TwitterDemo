import os
import oauth2 as oauth
import hashlib
import httplib2
from urllib import parse
from typing import Tuple

from TwitterDemo import get_db

TWITTER_API_URL = "https://api.twitter.com"
TWITTER_REQUEST_TOKEN_URL = "%s/oauth/request_token" % TWITTER_API_URL
TWITTER_ACCESS_TOKEN_URL = "%s/oauth/access_token" % TWITTER_API_URL
TWITTER_AUTHORIZE_URL = "%s/oauth/authorize" % TWITTER_API_URL
TWITTER_SHOW_USER_URL = "%s/1.1/users/show.json" % TWITTER_API_URL

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")

if not TWITTER_CONSUMER_KEY or not TWITTER_CONSUMER_SECRET:
    raise "Twitter credentials are missing"


def hash_client_address(addr: str):
    hasher = hashlib.sha256(addr.encode())
    return hasher.hexdigest()


async def store_client_credentials(id: str, client_oaut: str, client_oauth_secret: str):
    db = get_db()


async def get_consumer_oauth(callback_url: str) -> Tuple[str, str]:
    consumer = oauth.Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    client = oauth.Client(consumer)
    payload = {
        "oauth_callback": callback_url
    }
    resp: httplib2.Response = None
    content: bytes = None
    resp, content = client.request(TWITTER_REQUEST_TOKEN_URL, "POST", body=parse.urlencode(payload))
    if resp.status != 200:
        raise httplib2.HttpLib2ErrorWithResponse("Error obtaining redirect url", resp, content)
    request_token = dict(parse.parse_qsl(content.decode()))
    oauth_token = request_token.get("oauth_token")
    oauth_token_secret = request_token.get("oauth_token_secret")

    if not oauth_token or not oauth_token_secret:
        raise Exception("Missing oauth_token or oauth_token_secret in handshake")

    return oauth_token, oauth_token_secret