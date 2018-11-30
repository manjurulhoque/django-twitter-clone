from django import template

from src.twitty.models import Like, Retweet

register = template.Library()


@register.simple_tag(name='is_liked')
def is_liked(user, tweet):
    return Like.objects.filter(user=user, tweet=tweet).exists()


@register.simple_tag(name='is_retweeted')
def is_retweeted(user, tweet):
    return Retweet.objects.filter(user=user, tweet=tweet).exists()
