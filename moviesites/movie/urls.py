from django.conf.urls import url

from . import views

app_name = 'movie'
urlpatterns = [
	url(r'^movie/$', views.IndexView.as_view(), name='index'),
	url(r'^movie/post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
	url(r'^tags/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tags')

]