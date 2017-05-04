# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import *

# Create your views here.

from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).order_by('published_at')
    return render(request, 'blog_app/post_list.html', { 'posts' : posts })

def post_detail(request, p_id):
    post = get_object_or_404(Post, pk=p_id)
    return render(request, 'blog_app/post_detail.html', { 'post' : post })

@login_required
def post_new(request):
    form = PostForm()
    return render(request, 'blog_app/post_new.html', { 'form' : form })

@login_required
def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.published_at = timezone.now()
        post.save()
        return redirect('post_detail', p_id=post.pk)

@login_required
def post_edit(request, p_id):
    post = get_object_or_404(Post, pk=p_id)
    form = PostForm(instance=post)
    return render(request, 'blog_app/post_edit.html', { 'form' : form, 'post' : post })

@login_required
def post_update(request, p_id):
    old_post = get_object_or_404(Post, pk=p_id)
    form = PostForm(request.POST, instance=old_post)
    if form.is_valid():
        post = form.save(commit=False)
        # prveious data from the record will still be the same, hence we can directly save it
        post.save()
        return redirect('post_detail', p_id=post.pk)

@login_required
def post_destroy(request, p_id):
    post = get_object_or_404(Post, pk=p_id)
    post.delete()
    return redirect('post_list')

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True)
    return render(request, 'blog_app/post_list.html', { 'posts' : posts })

@login_required
def post_publish(request, p_id):
    post = get_object_or_404(Post, pk=p_id)
    post.publish()
    return redirect('post_detail', p_id=post.pk)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    form = UserRegistrationForm()
    return render(request, 'registration/register.html', { 'form' : form })
