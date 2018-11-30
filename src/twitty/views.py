from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import CreateView

from src.accounts.models import User
from src.twitty.forms import CreateTweetForm
from src.twitty.models import Tweet, Follow, Like, Retweet


@login_required(login_url='/login')
def home(request):
    tweets = Tweet.objects.order_by('-id')
    users = User.objects.exclude(username=request.user.username)
    who_to_follow = [user for user in users if Follow.objects.filter(follow=user, user=request.user).exists() is False]
    return render(request, 'home.html', {'tweets': tweets, 'users': who_to_follow})


# @login_required(login_url='/login')
# @require_POST
# def create_tweet(request):
#     form = CreateTweetForm(data=request.POST or None)
#     if form.is_valid():
#         model = form.save(commit=False)
#         model.user = request.user
#         model.save()
#         return redirect("/")
#     else:
#         print(form.errors)
#         return redirect("/")

class CreateTweetView(CreateView):
    form_class = CreateTweetForm
    http_method_names = ['post']

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user = self.request.user
        model.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, "Form is invalid")
        return reverse('twitty:home')

    def get_success_url(self):
        return reverse('twitty:home')


@login_required(login_url='/login')
def follow(request):
    f = request.GET.get('follow')
    follow_user = User.objects.get(pk=int(f))
    new_follow = Follow(user=request.user, follow=follow_user)
    new_follow.save()
    data = {
        'success': 1
    }
    return JsonResponse(data)


@login_required(login_url='/login')
def follow_user(request, id=None):
    fol = User.objects.get(id=id)
    if not Follow.objects.filter(follow=fol, user=request.user).exists():
        new_follow = Follow(follow=fol, user=request.user)
        new_follow.save()
        return redirect(to='/profile/' + str(new_follow.follow.username))
    else:
        return redirect(to='/')


@login_required(login_url='/login')
def unfollow_user(request, id=None):
    fol = User.objects.get(id=id)
    if Follow.objects.filter(follow=fol, user=request.user).exists():
        f = Follow.objects.get(follow=fol, user=request.user)
        f.delete()
        return redirect(to='/profile/' + str(f.follow.username))
    else:
        return redirect(to='/')


@login_required(login_url='/login')
def like(request):
    tweet = Tweet.objects.get(id=request.POST['tweet_id'])
    new_like = Like(user=request.user, tweet=tweet)
    new_like.save()
    return JsonResponse({'success': 1})


@login_required(login_url='/login')
def dislike(request):
    tweet = Tweet.objects.get(id=request.POST['tweet_id'])
    Like.objects.filter(user=request.user, tweet=tweet).delete()
    return JsonResponse({'success': 1})


@login_required(login_url='/login')
def retweet(request):
    tweet = Tweet.objects.get(id=request.POST['tweet_id'])
    new_retweet = Retweet(user=request.user, tweet=tweet, message=request.POST['retweet'])
    new_retweet.save()
    return redirect('/')
