import praw
from tokens import app_key, app_secret, access_token, refresh_token
from settings import scopes, user_agent, redirect_url

r = praw.Reddit(user_agent=user_agent)

r.set_oauth_app_info(client_id=app_key,
                      client_secret=app_secret,
                     redirect_uri=redirect_url)
# Setup Access Token
#url = r.get_authorize_url('uniqueKey', scopes, True)
#import webbrowser
#webbrowser.open(url)

# Use Acces Token to get Refresh Token
#access_information = r.get_access_information(access_token)
#print(access_information)