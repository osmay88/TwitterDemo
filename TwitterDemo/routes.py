import httplib2
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import get_db
from .db import ClientInfo, get_client
from .service import get_consumer_oauth, TWITTER_AUTHORIZE_URL, hash_client_address

router = APIRouter()
templating = Jinja2Templates("templates")


@router.get("/")
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    client_addr = hash_client_address(request.client.host)
    try:
        oauth_token, oauth_token_secret = await get_consumer_oauth(request.url_for("authorize"))
    except httplib2.HttpLib2ErrorWithResponse as err:
        error_ctx = {
            "request": request,
            "error_code": err.response.status,
            "error_msg": err.content.decode()
        }
        return templating.TemplateResponse("error.html", error_ctx)
    except Exception as err:
        error_ctx = {
            "request": request,
            "error_code": "000",
            "error_msg": str(err)
        }
        return templating.TemplateResponse("error.html", error_ctx)
    context = {
        "request": request,
        "callback_url": "%s?oauth_token=%s" % (TWITTER_AUTHORIZE_URL, oauth_token),
        "auth_active": "active"
    }
    client = await get_client(db, client_addr)
    if not client:
        client = ClientInfo()
        client.id = client_addr
        client.client_oauth_token = oauth_token
        client.client_oauth_secret = oauth_token_secret
        db.add(client)
        await db.commit()
    return templating.TemplateResponse("home.html", context)


@router.get("/oauth/callback")
async def authorize(request: Request, db: Session = Depends(get_db)):
    client_addr = hash_client_address(request.client.host)
    return ""


@router.get("/dms")
async def render_dms(request: Request):
    context = {
        "request": request,
        "dm_active": "active"
    }
    return templating.TemplateResponse("dms.html", context)
