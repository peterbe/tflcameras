from django.conf import settings
import django.views.static
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'', include('map.urls', namespace="map", app_name="map")),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:

    # When not in debug mode (i.e. development mode)
    # nothing django.views.static.serve should not be used at all.
    # If it is used it means that nginx config isn't good enough.

    urlpatterns += patterns('',

        # CSS, Javascript and IMages
        (r'^img/(?P<path>.*)$', django.views.static.serve,
         {'document_root': settings.MEDIA_ROOT + '/img',
           'show_indexes': settings.DEBUG}),
        (r'^css/(?P<path>.*)$', django.views.static.serve,
          {'document_root': settings.MEDIA_ROOT + '/css',
           'show_indexes': settings.DEBUG}),
        (r'^js/(?P<path>.*)$', django.views.static.serve,
          {'document_root': settings.MEDIA_ROOT + '/js',
           'show_indexes': settings.DEBUG}),
    
    )
