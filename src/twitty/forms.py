from django import forms

from src.twitty.models import Tweet


class CreateTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['tweet', 'image']
