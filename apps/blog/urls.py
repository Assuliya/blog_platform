from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'blog/login$', views.login, name='login'),
    url(r'blog/register$', views.register, name='register'),
    url(r'user/(?P<user_id>\d+)/edit$', views.edit, name='edit'),
    url(r'user/dashboard$', views.dashboard, name='dashboard'),
    url(r'^blog/(?P<user_id>\d+)$', views.show, name='show'),
    url(r'user/deletion_page$', views.deletion_page, name='deletion_page'),

    url(r'^blog/login_process$', views.login_process, name='login_process'),
    url(r'^blog/register_process$', views.register_process, name='register_process'),
    url(r'user/update$', views.update, name='update'),
    url(r'user/update_pass$', views.update_pass, name='update_pass'),
    url(r'^blog/logout$', views.logout, name='logout'),
    url(r'^user/delete$', views.delete, name='delete'),

    url(r'^user/add_post$', views.add_post, name='add_post'),
    url(r'^user/(?P<post_id>\d+)/add_comment$', views.add_comment, name='add_comment')

]
