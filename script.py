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
    data        = { 'grant_type': 'password', 'username': username, 'password': password }
    headers     = { 'User-Agent': user_agent }

    response = requests.post(url, auth=client_auth, data=data, headers=headers)

    if response.status_code != 200:
        print('ERROR: response did not return 200 OK')
        print(response)
        exit()

    json_response = response.json()
    access_token  = json_response['access_token']
    token_type    = json_response['token_type']

    authorization = token_type + ' ' + access_token

    # ---- Get user's saved posts ----------------------------------------------
    # TODO: Refactor initial request into loop

    url      = 'https://oauth.reddit.com/user/' + username + '/saved'
    headers  = { 'Authorization': authorization, 'User-Agent': user_agent }
    response = requests.get(url, headers=headers)

    json_response = response.json()
    all_posts     = json_response['data']['children']
    after         = json_response['data']['after']

    print('Retrieving saved posts for ' + username + '...')

    while after is not None:
        params   = { 'after': after }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print('ERROR: response did not return 200 OK')
            print(response)
            exit()

        json_response = response.json()
        posts         = json_response['data']['children']
        after         = json_response['data']['after']

        all_posts     = all_posts + posts

    print(' ...found ' + str(len(all_posts)) + '.')

    # ---- Filter posts --------------------------------------------------------
    # TODO: Filter by image size

    print('Filtering for images...')

    filtered_posts = filter(lambda post: post['data']['subreddit'] == subreddit, all_posts)
    target_urls = {}

    for post in filtered_posts:
        title   = post['data']['title']
        url     = post['data']['url']

        if is_url_image(url):
            target_urls[title] = url

    print(' ...found ' + str(len(target_urls)) + '.')

    # ---- Download image posts ------------------------------------------------
    # TODO: Normalize file names

    print('Downloading images...')

    for title, url in target_urls.iteritems():
        try:
            file_extension = get_file_extension(url)
            file_name      = title + '.' + file_extension
            print(' -> ' + url)
            download_image(url, 'output/' + file_name)
        except:
            continue

    print(' ...done.')

    # TODO: Unsave post (optional)

# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    download_saved_images()
