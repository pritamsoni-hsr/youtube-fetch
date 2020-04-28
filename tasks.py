import requests
from db import Videos
from decouple import config
from server import app

VIDEOS_PER_PAGE = 25

API_KEY = config('API_KEY', cast=str)

client = requests.session()
client.headers['Accept'] = 'application/json'


def raiseError(value):
    raise ValueError(value)


def yt_params(**kwargs):
    """
    opt = available_params.get(key, None)
    opt.type= required => raise warning
            = from avaialble options => use the provided if it 
                matches else use a default key
    """

    available_params = {
        'part': lambda x: x or 'snippet',
        'q': lambda x: x or raiseError('Value is required\n q=query'),
        'maxResults': lambda x: min(x, VIDEOS_PER_PAGE),
        'pageToken': lambda x: x or None,
        # 'channelId': str,
        # 'channelType': 'any|show',
        # 'location': str,
        # 'locationRadius': int,
        # 'topicId': str,
        # 'type': str,
        # 'videoCategoryId': str,
    }
    query_params = {}
    for i in kwargs:
        opt = available_params.get(i, None)
        if opt:
            query_params[i] = opt(kwargs[i])
            if not opt(kwargs[i]):
                del query_params[i]

    return query_params


def fetch_data(query='cricket', pageToken=None, **kwargs):
    params = yt_params(
        q=query, part='', maxResults=20, pageToken=pageToken,
    )
    url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&order=date&type=video&publishedAfter=2018-01-01'  # noqa

    response = client.get(url, params=params)

    if response.status_code != 200:
        return response.json()['error']['message'], False

    response = response.json()
    if len(response['items']) == 0:
        return 'End of results', False

    nextPageToken = response['nextPageToken']
    for vid in response['items']:
        snippet = vid['snippet']
        v = Videos(
            videoId=vid['id']['videoId'],
            title=snippet['title'],
            description=snippet['description'],
            thumbnails=snippet['thumbnails'],
            channelTitle=snippet['channelTitle'],
            publishedAt=snippet['publishedAt'],
        )
        with app.app_context():
            try:
                v.insert()
            except:
                print('-', end=' ')
    return nextPageToken, True


# def loop_infinite(query='cricket'):
#     paginationToken, _ = None, True
#     # paginationToken = config('TOKEN', cast=str, default=None)
#     while(_):
#         print(paginationToken)
#         paginationToken, _ = fetch_data(query=query, pageToken=paginationToken)
#     print(paginationToken)
# loop_infinite()
