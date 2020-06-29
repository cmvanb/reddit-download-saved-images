# -----------------------------------------------------------------------------
# Download user's saved images
# -----------------------------------------------------------------------------
def download_saved_images():
    import configparser
    import requests
    import requests.auth

    # ---- Config -------------------------------------------------------------

    config = configparser.RawConfigParser()
    config.read('input/credentials.ini')

    username   = config['DEFAULT']['username']
    password   = config['DEFAULT']['password']
    app_token  = config['DEFAULT']['app_token']
    app_secret = config['DEFAULT']['app_secret']

    user_agent = 'DownloadImages script'

    # ---- Get access token ---------------------------------------------------

    url         = 'https://www.reddit.com/api/v1/access_token'
    client_auth = requests.auth.HTTPBasicAuth(app_token, app_secret)
    payload     = { 'grant_type': 'password', 'username': username, 'password': password }
    headers     = { 'User-Agent': user_agent }

    response = requests.post(url, auth=client_auth, data=payload, headers=headers)

    data         = response.json()
    access_token = data['access_token']
    token_type   = data['token_type']

    authorization = token_type + ' ' + access_token

    # ---- Get user data ------------------------------------------------------

    url      = 'https://oauth.reddit.com/api/v1/me'
    headers  = { 'Authorization': authorization, 'User-Agent': user_agent }
    response = requests.get(url, headers=headers)

    data = response.json()
    print(data)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys

    #if not sys.argv[1]:
    #    print 'ERROR: Missing command line argument: recipeId'
    #    sys.exit(1)

    download_saved_images()
