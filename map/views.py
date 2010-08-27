from pprint import pprint
from utils.render_decorator import render
from django.core.cache import cache

ONE_MINUTE = 60

ONE_HOUR = ONE_MINUTE ** 2


@render('show_map.html')
def show_map(request):
    return locals()

import feedparser
FEED_URL = "http://www.tfl.gov.uk/tfl/syndication/feeds/traffic-camera-update-v1.xml"


def load_feed():
    # cache protected version of _load_feed()
    cache_key = 'traffic-camera-feed'
    cameras = cache.get(cache_key)
    if cameras is None:
        cameras = list(_load_feed())
        cache.set(cache_key, cameras, ONE_MINUTE * 2)
    return cameras

def _load_feed():
    fed = feedparser.parse(FEED_URL)
    
    for entry in fed['entries']:
        title = entry.title
        
        yield dict(title=title, 
                   lat=entry.geo_lat, 
                   lng=entry.geo_long, # because 'long' is a keyword in JS
                   link=entry.link,
                   id=entry.id)
    

@render('json')
def cameras_json(request):
    since = request.GET.get('since')
    if since:
        raise NotImplementedError("work harder!")
    
    cameras = []
    for camera in load_feed():
        cameras.append(camera)
    return dict(cameras=cameras)