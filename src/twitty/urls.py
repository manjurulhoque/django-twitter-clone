from django.contrib.auth.decorators import login_required
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from src.twitty.views import home, CreateTweetView, follow, follow_user, unfollow_user, like, dislike, retweet

app_name = "twitty"

urlpatterns = [
    path('', home, name='home'),
    path('tweets/create', CreateTweetView.as_view(), name='create'),
    path('follow', follow, name='follow'),
    path('follow_user/<int:id>', follow_user, name='follow_user'),
    path('unfollow_user/<int:id>', unfollow_user, name='unfollow_user'),
    path('like', like, name='like'),
    path('dislike', dislike, name='dislike'),
    path('retweet', retweet, name='retweet'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
