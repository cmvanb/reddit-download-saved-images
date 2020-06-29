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

    # ---- Get access token ---------------------------------------------------

    url = 'https://www.reddit.com/api/v1/access_token'

    client_auth = requests.auth.HTTPBasicAuth(app_token, app_secret)

    req = requests.get(url)

    data = req.text

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
