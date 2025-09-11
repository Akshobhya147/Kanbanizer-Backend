from fastapi import APIRouter,Request
from fastapi.responses import Response
import os
from dotenv import load_dotenv
from jwt_handler import create_token
from fastapi.responses import JSONResponse

load_dotenv()

signoutrouter=APIRouter()

@signoutrouter.post("/",tags=["signout"])
async def signout():
    # here, we assume that a user would only be able to sign out if they are already signed in.
    # And, so, we are not going to verify the token recieved in the cookie.

    our_token=create_token("0","anon@email.com",-200) 
    # it doesn't matter what userID and email we use to create the token,
    # since, this is going to generate an expired token (, notice negative time_delta value),
    # we'll send this expired token in the cookie and redirect to home page (update: via front-end), so that when, the front-end
    # tries to send authorization request next time, using the expired token, the server, i.e., us, will redirect it to signin.

    # response=RedirectResponse(url=os.getenv("APP_FRONT_END"),status_code=301)
    # Redirect response doesn't work because fetch (in front-end) follows the server, then, the redirect response
    # assuming it is an end-point. But, the redirected url is actually an HTML page. As a result, the pre-flight request fails to 
    # that page (, since, it is not an endpoint) and the browser throws a CORS error.
    # This worked in signin because (my guess) actually, the google's auth system redirected to backend and fetch wasn't used. So, the redirect to myspace happened organically.
    # Instead, following:
    response=JSONResponse(content={"status":"success","info":"signed out successfully."},status_code=200)
    response.delete_cookie("session_token")
    response.headers["Cache-Control"]="no-store"
    return response

