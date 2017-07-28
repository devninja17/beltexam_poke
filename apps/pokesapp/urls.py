from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index),
    url('^main$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^pokes$', views.dashboard),
    url('^pokes/(?P<user_id>\d+)$', views.got_poked)
]