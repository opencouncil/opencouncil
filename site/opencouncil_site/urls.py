from django.conf.urls.defaults import patterns, include
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^api/locksmith/', include('locksmith.mongoauth.urls')),
    (r'^api/', include('billy.web.api.urls')),
    (r'^admin/', include('billy.web.admin.urls')),
    (r'^djadmin/', include(admin.site.urls)),
    #(r'^', include('billy.web.public.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', 'django.views.defaults.page_not_found'),
        (r'^500/$', 'django.views.defaults.server_error'),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT,
          'show_indexes': True}))
