from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Post, PostForm, Like, Follow
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required




def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('all_posts')  # Redirect to the page where all posts are displayed
    else:
        form = PostForm()

    return render(request, 'network/new_post.html', {'form': form})


def all_posts(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'network/all_posts.html', {'posts': posts})



@login_required
def following_posts(request):
    # Get the users that the current user is following
    following_users = Follow.objects.filter(follower=request.user).values('following')

    # Get posts from the following users
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')

    return render(request, 'network/following_posts.html', {'posts': posts})


@login_required
def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    # Check if the current user is the profile user
    is_own_profile = profile_user == request.user

    # Fetch posts for the profile user
    posts = Post.objects.filter(user=profile_user).order_by('-timestamp')

    # Get follower and following counts
    follower_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    # Check if the current user is following the profile user
    is_following = False
    if not is_own_profile:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, 'network/user_profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_own_profile': is_own_profile,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following,
    })

@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    Follow.objects.create(follower=request.user, following=followed_user)
    return redirect('user_profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=followed_user).delete()
    return redirect('user_profile', user_id=user_id)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        post.content = new_content
        post.edited = True
        post.save()
        return JsonResponse({'success': True})

    return render(request, 'network/edit_post.html', {'post': post})


@require_POST
def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()

        post_likes_count = post.likes.count()

        return JsonResponse({'likes_count': post_likes_count})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in like_post view: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


@login_required
def unlike_post(request, post_id):
    # Implement logic to handle unliking a post
    # ...
    return redirect('all_posts')