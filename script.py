# -----------------------------------------------------------------------------
# Globals
# -----------------------------------------------------------------------------

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']

# -----------------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------------

def index_of(value, list):
    try:
        return list.index(value)
    except ValueError:
        return -1

def contains(value, list):
    return index_of(value, list) != -1

def is_url_image(url):
    try:
        file_extension = url.rpartition('.')[-1]
        return contains(file_extension, IMAGE_EXTENSIONS)
    except:
        return False

# -----------------------------------------------------------------------------
# Download user's saved images
# -----------------------------------------------------------------------------
def download_saved_images():
    import configparser
    import requests
    import requests.auth
    import io
    import json

    # ---- Config -------------------------------------------------------------

    config = configparser.RawConfigParser()
    config.read('input/credentials.ini')

    username   = config['DEFAULT']['username']
    password   = config['DEFAULT']['password']
    app_token  = config['DEFAULT']['app_token']
    app_secret = config['DEFAULT']['app_secret']

    config.read('input/filters.ini')
    subreddit  = config['DEFAULT']['subreddit']

    user_agent = 'DownloadImages script'

    # ---- Get access token ---------------------------------------------------

    url         = 'https://www.reddit.com/api/v1/access_token'
    client_auth = requests.auth.HTTPBasicAuth(app_token, app_secret)
    payload     = { 'grant_type': 'password', 'username': username, 'password': password }
    headers     = { 'User-Agent': user_agent }

    response = requests.post(url, auth=client_auth, data=payload, headers=headers)

    if response.status_code != 200:
        print('ERROR: response did not return 200 OK')
        print(response)
        exit()

    json_response = response.json()
    access_token  = json_response['access_token']
    token_type    = json_response['token_type']

    authorization = token_type + ' ' + access_token

    # ---- Get user's saved posts ---------------------------------------------

    url      = 'https://oauth.reddit.com/user/' + username + '/saved'
    headers  = { 'Authorization': authorization, 'User-Agent': user_agent }
    response = requests.get(url, headers=headers)

    json_response = response.json()
    posts         = json_response['data']['children']

    # ---- Filter posts -------------------------------------------------------

    filtered_posts = filter(lambda post: post['data']['subreddit'] == subreddit, posts)

    for post in filtered_posts:
        url = post['data']['url']
        if is_url_image(url):
            print(url + ' is an image!')
            # TODO: download image

    # output_file   = 'output/saved_posts.json'
    # json_unicode  = unicode(json.dumps(json_response))

    # with io.open(output_file, 'w', encoding='utf-8') as f:
    #     f.write(json_unicode)

# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys

    #if not sys.argv[1]:
    #    print 'ERROR: Missing command line argument: recipeId'
    #    sys.exit(1)

    download_saved_images()
