from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator

from .models import Group, Post, User
from posts.forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.ITEMS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, settings.ITEMS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    post_count = posts.count()
    paginator = Paginator(posts, settings.ITEMS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'post_count': post_count,
        'author': author
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts = Post.objects.filter(author__id=post.author_id)
    post_count = posts.count()
    context = {
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = User.objects.get(username=request.user.username)
        post.save()
        return redirect('posts:profile', username=request.user.username)

    posts_group = Group.objects.all()
    context = {
        'posts_group': posts_group,
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    author = post.author
    if author != user:
        return redirect('posts:post_id')

    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('posts:post_id')

    form = PostForm(instance=post)
    context = {
        'form': form,
        'post_id': post_id,
    }
    return render(request, 'posts/create_post.html', context)
