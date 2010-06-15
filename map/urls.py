from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    # Example:
    url(r'^$', views.show_map, name="show-map"),
    url(r'^cameras.json$', views.cameras_json, name="cameras_json"),
)