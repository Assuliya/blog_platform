from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blog/main$', views.main, name='main'),
    url(r'^blog/display/(?P<search>\w+)$', views.display, name='display'),
    url(r'^blog/(?P<user_id>\d+)$', views.user, name='user'),
    url(r'^blog/login$', views.login, name='login'),
    url(r'^blog/edit$', views.edit, name='edit'),
    url(r'^blog/post/(?P<post_id>\d+)$', views.post, name='post'),

    url(r'^blog/login_process$', views.login_process, name='login_process'),
    url(r'^blog/register_process$', views.register_process, name='register_process'),
    url(r'^blog/update$', views.update, name='update'),
    url(r'^blog/update_pass$', views.update_pass, name='update_pass'),
    url(r'^blog/logout$', views.logout, name='logout'),
    url(r'^blog/delete$', views.delete, name='delete'),

    url(r'^blog/add_post$', views.add_post, name='add_post'),
    url(r'^blog/post/(?P<post_id>\d+)/add_comment$', views.add_comment, name='add_comment'),
    url(r'^blog/post/(?P<post_id>\d+)/add_like$', views.add_like, name='add_like'),

]
