# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']

# ------------------------------------------------------------------------------
# Utility
# ------------------------------------------------------------------------------

def index_of(value, list):
    try:
        return list.index(value)
    except ValueError:
        return -1

def contains(value, list):
    return index_of(value, list) != -1

def get_file_extension(url):
    return url.rpartition('.')[-1]

def is_url_image(url):
    try:
        file_extension = get_file_extension(url)
        return contains(file_extension, IMAGE_EXTENSIONS)
    except:
        return False

def download_image(url, path):
    import requests
    import io

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with io.open(path, 'wb') as f:
            for chunk in response:
                f.write(chunk)

# ------------------------------------------------------------------------------
# Download user's saved images
# ------------------------------------------------------------------------------
def download_saved_images():
    import configparser
    import requests
    import requests.auth

    # ---- Config --------------------------------------------------------------

    config = configparser.RawConfigParser()
    config.read('input/credentials.ini')

    username   = config['DEFAULT']['username']
    password   = config['DEFAULT']['password']
    app_token  = config['DEFAULT']['app_token']
    app_secret = config['DEFAULT']['app_secret']

    config.read('input/filters.ini')
    subreddit  = config['DEFAULT']['subreddit']

    user_agent = 'DownloadImages script'

    # ---- Get access token ----------------------------------------------------

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

    # ---- Get user's saved posts ----------------------------------------------
    # TODO: Currently, this only retrieves the most recent 25 saved posts.
    # The script should retrieve all saved image posts, optionally filter them
    # (e.g. by image size, subreddit), download the images, and then optionally
    # unsave the posts.
    # https://www.reddit.com/dev/api

    url      = 'https://oauth.reddit.com/user/' + username + '/saved'
    headers  = { 'Authorization': authorization, 'User-Agent': user_agent }
    response = requests.get(url, headers=headers)

    json_response = response.json()
    posts         = json_response['data']['children']

    # ---- Filter posts --------------------------------------------------------

    filtered_posts = filter(lambda post: post['data']['subreddit'] == subreddit, posts)
    target_urls = {}

    for post in filtered_posts:
        title = post['data']['title']
        url   = post['data']['url']
        if is_url_image(url):
            print(url + ' is an image!')
            target_urls[title] = url

    # ---- Download image posts ------------------------------------------------

    for title, url in target_urls.iteritems():
        try:
            file_extension = get_file_extension(url)
            file_name      = title + '.' + file_extension
            download_image(url, 'output/' + file_name)
        except:
            continue

# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    download_saved_images()
