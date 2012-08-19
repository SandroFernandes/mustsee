from django.conf.urls import patterns, url

urlpatterns = patterns(
    'mustsee.views',
    url(r'^$', 'attraction_list', name='list'),
    url(r'^promote/(?P<attraction_id>\d+)$', 'promote',
        name='promote'
    ),
)
