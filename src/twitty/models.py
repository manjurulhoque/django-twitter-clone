from django.db import models

# Create your models here.
from src.accounts.models import User


class Tweet(models.Model):
    tweet = models.CharField(max_length=140, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name='tweets')
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to='tweets',
                              verbose_name="tweets")


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_user')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='liked_tweet')


class Retweet(models.Model):
    message = models.CharField(max_length=256, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='retweet_user')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='retweet_tweet')
