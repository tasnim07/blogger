from django.conf.urls import url
from app import views


urlpatterns = [
    url(r'^login', views.user_login, name='login'),
    url(r'^register', views.user_registration, name='register'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^home', views.home, name='app-home'),
    url(r'^create', views.create, name='post-create'),
    url(r'^post/(?P<pk>\d+)/like', views.like_post, name='post-like'),
    url(r'^post/(?P<pk>\d+)/unlike', views.unlike_post, name='post-unlike'),
    url(r'^post/(?P<pk>\d+)/delete', views.delete, name='post-delete')
]
