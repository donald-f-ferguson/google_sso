"""Google Login Example
"""

import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
import json

from fastapi.staticfiles import StaticFiles

from data_service import MySQLDataService

import env

app = FastAPI()
my_sql_data_service = MySQLDataService()


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
OAUTH_URL = os.environ["OAUTH_URL"]

app.mount("/static", StaticFiles(directory="static"), name="static")

sso = GoogleSSO(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=OAUTH_URL + "/auth/callback",
    allow_insecure_http=True,
)


@app.get("/ping", response_class=HTMLResponse)
def ping():
    """

    :return:
    """

    rsp = """
     <!DOCTYPE html>
            <html>
            <head>
                <title>User Info</title>
            </head>
            <body>
               Pong.
            </body>
            </html>
    """
    return rsp

@app.get("/", response_class=HTMLResponse)
async def home_page():
    print("Current directory = " + os.getcwd())
    print("Files = " + str(os.listdir("./")))

    result = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 100px;
            }
            .container {
                width: 300px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            .logo {
                margin-bottom: 20px;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #4285f4;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
        <p>
        This is the sample web application for <a href="https://donald-f-ferguson.github.io/E6156-Cloud-Computing-F23/">
        E6156 - Topics in SW Engineering, section 001, Fall 2023.</a> 
        </p>
        <p>The application simply demonstrates single sign-on
        via Google for Columbia University students.
        </p>
        <p>
        The application does not capture or maintain any information about users. The application does not
        share any information.
        </p>
        <form action="{OAUTH_URL}/auth/login">
            <div class="logo">
                <img src="{OAUTH_URL}/static/e6156-logo.jpg" 
                    height="100px" alt="Google Logo">
            </div>
            <h2>Sign in with your Google Account</h2>
            <button type="submit" class="button">Login with Google</button>
            </form>
        </div>
    </body>
    </html>
    """

    result = result.replace("{OAUTH_URL}", OAUTH_URL)
    return result

@app.get("/auth/login")
async def auth_init():
    """Initialize auth and redirect"""
    with sso:
        return await sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@app.get("/auth/callback", response_class=HTMLResponse)
async def auth_callback(request: Request):
    """Verify login"""
    print("Request = ", request)
    print("URL = ", request.url)

    try:
        with sso:
            user = await sso.verify_and_process(request)
            data = user

            student = my_sql_data_service.get_student_info(user.email)
            print("Student = \n", json.dumps(student, indent=2, default=str))
            coupon = student.get("student_coupon_code", None)
            coupon_value = student.get("Value", None)

            # if user.email == "dff9@columbia.edu":
            #    raise Exception("Not cool dude.")

            html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>User Info</title>
                </head>
                <body>
                    <h1>User Information</h1>
                    <img src="{user.picture}" alt="User Picture" width="96" height="96"><br>
                    <p>ID: {user.id}</p>
                    <p>Email: {user.email}</p>
                    <p>First Name: {user.first_name}</p>
                    <p>Last Name: {user.last_name}</p>
                    <p>Display Name: {user.display_name}</p>
                    <p>Identity Provider: {user.provider}</p>
                    <h1>Google Coupon Information</h1>
                    <p>Google Coupon: {coupon}<br>
                    <p>Coupon Value: ${coupon_value}
                </body>
                </html>
                """

            return HTMLResponse(content=html_content)
    except Exception as e:
        print("Exception e = ", e)
        return RedirectResponse("/static/error.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
