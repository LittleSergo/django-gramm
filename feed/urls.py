from django.urls import path, include

from . import views

app_name = 'feed'

auth_urlpatterns = [
    path('signup', views.signup_user, name='signup'),
    path('activate/<uidb64>/<token>', views.activate_user, name='activate_user'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
]

user_urlpatterns = [
    path('<user_id>', views.user_profile, name='user_profile'),
    path('<user_id>/edit', views.user_edit_profile, name='user_edit_profile'),
    path('<user_id>/follow', views.follow, name='follow'),
    path('<user_id>/followers', views.followers, name='followers'),
    path('<user_id>/following', views.following, name='following'),
]

post_urlpatterns = [
    path('create', views.create_post, name='create_post'),
    path('<post_id>/like', views.like, name='like'),
    path('<post_id>/make_comment', views.make_comment, name='make_comment'),
]

comment_urlpatterns = [
    path('<comment_id>/like', views.like_comment, name='like_comment'),
]

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('users/', include(user_urlpatterns)),
    path('auth/', include(auth_urlpatterns)),
    path('posts/', include(post_urlpatterns)),
    path('comments/', include(comment_urlpatterns)),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
]
