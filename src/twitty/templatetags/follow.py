from django import template

from src.twitty.models import Follow

register = template.Library()


@register.simple_tag(name='following')
def following(user):
    return Follow.objects.filter(user=user).count()


@register.simple_tag(name='follower')
def follower(user):
    return Follow.objects.filter(follow=user).count()


@register.simple_tag(name='is_follow_by_me')
def is_follow_by_me(follow, user):
    return Follow.objects.filter(follow=follow, user=user).exists()
