import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import FollowerRelation, Post, User, Like

class NewPostForm(forms.Form):
    content = forms.CharField(max_length=500, widget=forms.Textarea(), label='')

def index(request):
    posts = Post.objects.all().order_by('-creation_date')
    form = NewPostForm()
    paginator = create_post_paginator(posts)
    page_number = request.GET.get('page')
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NewPostForm(request.POST)
            if form.is_valid():
                post_content = form.cleaned_data['content']
                create_post(request,post_content)
    return render(request, 'network/index.html', {
        'posts': paginator.get_page(page_number),
        'form': form,
    })

def user(request, user_id):
    page_user = User.objects.get(id=user_id)
    posts = page_user.posts.order_by('-creation_date')
    followed = FollowerRelation.objects.filter(user=request.user, followed_user=page_user).exists()
    return render(request, 'network/user.html', {
        'page_user': page_user,
        'posts': posts,
        'followed': followed,
    })

def following(request):
    if request.user.is_authenticated:
        follower_relations = request.user.followed_users.all()
        posts = []
        for relation in follower_relations:
            posts += relation.followed_user.posts.all()
        posts = sorted(posts, key=lambda post: post.creation_date, reverse=True)
        paginator = create_post_paginator(posts)
        page_number = request.GET.get('page')
        return render(request, 'network/following.html', {
            'posts': paginator.get_page(page_number)
        })
    else:
        return HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.method == 'POST':
        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'network/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'network/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'network/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'network/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'network/register.html')

def follow(request, page_user_id):
    followerRelation = FollowerRelation(user=request.user, followed_user=User.objects.get(id=page_user_id))
    followerRelation.save()
    return HttpResponseRedirect(reverse('user', args=(page_user_id,)))

def unfollow(request, page_user_id):
    followerRelation = FollowerRelation.objects.get(user=request.user, followed_user=page_user_id)
    followerRelation.delete()
    return HttpResponseRedirect(reverse('user', args=(page_user_id,)))

def create_post(request, post_content):
    if request.method == 'POST':
        new_post = Post(user=request.user, content=post_content, creation_date=timezone.now())
        new_post.save()
        return HttpResponseRedirect(reverse('index'))

def create_post_paginator(posts):
    paginator = Paginator(posts, 10)
    return paginator

@csrf_exempt
def edit_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required.'}, status=400)
    data = json.loads(request.body)
    id = data.get('id')
    content = data.get('content')
    if not content or not id:
        return JsonResponse({'error': 'Incorrect JSON response data received'})
    post = Post.objects.get(id=id)
    post.content = content
    post.save()
    return JsonResponse({'message': 'Post edited successfully'})

@csrf_exempt
def like_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required.'}, status=400)
    data = json.loads(request.body)
    id = data.get('id')
    if not id:
        return JsonResponse({'error': 'Incorrect JSON response data received'})
    post = Post.objects.get(id=id)
    user_likes_on_post = Like.objects.filter(user=request.user, post=post)
    if user_likes_on_post.exists():
        user_likes_on_post.delete()
        return JsonResponse({'message': 'Post unliked successfully'})
    else:
        like = Like(user=request.user, post=post)
        like.save()
        return JsonResponse({'message': 'Post liked successfully'})
    
def post_likes(request, post_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET request required.'}, status=400)
    post = Post.objects.get(id=post_id)
    return JsonResponse({'likes': f'{post.post_likes.count()}', 'user_liked': Like.objects.filter(user=request.user, post=post).exists()})
    




