import base64
import hashlib
import hmac
import os
from fastapi import APIRouter, Request

router = APIRouter()


TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")


@router.post("/api/webhook")
def webhook(request: Request):
    pass


@router.get("/api/webhook")
def authenticate(request: Request):
    crc_token = request.query_params.get('crc_token')
    if not crc_token:
        raise ValueError("Missing crc token in request")

    sha256_hash_digest = hmac.new(TWITTER_CONSUMER_SECRET.encode(),
                                  msg=crc_token.encode(),
                                  digestmod=hashlib.sha256).digest()
    return {
        'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode()
    }