from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),  # <-- Add a comma here
    # View to create a new post
    path('new_post/', views.new_post, name='new_post'),

    # View to display all posts
    path('all_posts/', views.all_posts, name='all_posts'),

    # View to display a user's profile page
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),

    # View to handle following/unfollowing a user
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),

    # View to display posts from users that the current user follows
    path('following_posts/', views.following_posts, name='following_posts'),

    # View to edit a post
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),

    # View to handle liking/unliking a post
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('unlike_post/<int:post_id>/', views.unlike_post, name='unlike_post'),
]
