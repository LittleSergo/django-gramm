import pytz

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist

from .forms import SignUpForm, EditProfile, CreatePostForm
from .models import User, Post, Image, Comment
from .tokens import account_activation_token


def activate_email(request, user, email):
    """Send an email with account confirmation link.
    :param request:
    :param user:
    :param email:
    :return:
    """
    mail_subject = "Activate your account."
    message = render_to_string("template_activate_account.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    email.send()


def signup_user(request):
    """Sign up user and send a confirmation email.
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'feed/signup_user.html',
                      {'form': SignUpForm()})
    # Create a new user
    if request.POST['password1'] == request.POST['password2']:
        try:
            user = User.objects.create_user(
                request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password1'])
            user.is_active = False
            user.save()
            activate_email(request, user, request.POST['email'])
            messages.success(request,
                             "You have been registered successfully."
                             "Please confirm your email before login.")
            return redirect('feed:login')
        except IntegrityError:
            messages.error(request,
                           f"That username has already been taken. "
                           "Please choose a new username.")
            return render(request, 'feed/signup_user.html', {
                'form': SignUpForm()
            })
    messages.error(request, "Passwords did not match!")
    return render(request, 'feed/signup_user.html', {
        'form': SignUpForm()
    })


def signup_redirect(request):
    messages.error(request, "That email has already been registered.")
    return redirect('feed:login')


def activate_user(request, uidb64, token):
    """Activate user by uid64 and token in link.
    :param request:
    :param uidb64:
    :param token:
    :return:
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except ObjectDoesNotExist:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return redirect('feed:user_edit_profile', user.id)


def login_user(request):
    """Login user page.
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'feed/login.html',
                      {'form': AuthenticationForm()})

    user = authenticate(request, username=request.POST['username'],
                        password=request.POST['password'])

    if user is None:
        messages.error(request, 'Username and password did not match.')
        return render(request, 'feed/login.html', {
            'form': AuthenticationForm()
        })

    if not user.is_active:
        messages.error(request, "Looks like your account isn't active."
                       "Please check your mailbox and confirm your"
                       "email to activate your account.")
        return render(request, 'feed/login.html', {
            'form': AuthenticationForm()
        })

    messages.success(request, f"Successfully logged in as {user.username}.")
    login(request, user)
    return redirect('feed:feed')


@login_required
def logout_user(request):
    """Log out user functionality.
    :param request:
    :return:
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Successfully logged out.')
        return redirect('feed:login')


@login_required
def user_profile(request, user_id):
    """Representation of user's profile page.
    :param request:
    :param user_id:
    :return:
    """
    user = get_object_or_404(User, pk=user_id)
    followed = False
    if request.user in user.followers.all():
        followed = True
    return render(request, 'feed/user_profile.html', {
        'user': user,
        'followed': followed,
    })


@login_required
def user_edit_profile(request, user_id):
    """Representation of user's editing profile page.
    :param request:
    :param user_id:
    :return:
    """
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'GET':
        if user != request.user:
            return redirect('feed:user_profile', user_id)
        form = EditProfile(instance=user)
        return render(request, 'feed/user_edit_profile.html', {
            'form': form,
        })
    form = EditProfile(request.POST, request.FILES, instance=user)
    form.save()
    return redirect('feed:user_profile', user.id)


@login_required
def feed(request):
    """Representation of feed page. There user can see all posts.
    :param request:
    :return:
    """
    posts = Post.objects.order_by('-posted')[:25]
    following_users = [following for following
                       in request.user.following.all()]
    following_posts = Post.objects.filter(owner__in=following_users).order_by(
        '-posted')[:25]
    return render(request, 'feed/feed.html', {
        'posts': posts,
        'following_posts': following_posts,
    })


@login_required
def create_post(request):
    """Create post page. There user can create new post.
    :param request:
    :return:
    """
    if request.method == 'POST':
        post = Post.objects.create(description=request.POST['description'],
                                   owner=request.user)
        tags = request.POST['tags'].replace(' ', '').split(',')
        post.tags.add(*tags)
        post.save()
        for image in request.FILES.getlist('images'):
            Image.objects.create(post=post, image=image)
        return redirect('feed:feed')
    return render(request, 'feed/create_post.html', {
        'form': CreatePostForm(),
    })


@login_required
def like(request, post_id):
    """Functionality for liking posts. User can like post and
    unlike as well.
    :param request:
    :param post_id: the ID of the post to be liked.
    :return:
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return JsonResponse({'likes_count': post.likes.count(), 'liked': False})
    post.likes.add(request.user)
    return JsonResponse({'likes_count': post.likes.count(), 'liked': True})


@login_required
def follow(request, user_id):
    """Functionality for following users. User can follow and
    unfollow other user.
    :param request:
    :param user_id:
    :return:
    """
    user = get_object_or_404(User, pk=user_id)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
        return JsonResponse({'followers': user.followers.count(), 'followed': False})
    user.followers.add(request.user)
    return JsonResponse({'followers': user.followers.count(), 'followed': True})


@login_required
def followers(request, user_id):
    """Representation of page with list of followers.
    :param request:
    :param user_id:
    :return:
    """
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'feed/followers.html', {
        'user': user,
    })


@login_required
def following(request, user_id):
    """Representation of page with list of following.
    :param request:
    :param user_id:
    :return:
    """
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'feed/following.html', {
        'user': user,
    })


@login_required
def make_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    Comment.objects.create(text=request.POST['feed-comment'],
                           owner=request.user,
                           post=post)
    comments = {'post_id': post_id, 'comments': [{
        'owner': comment.owner.username, 'text': comment.text,
        'posted': comment.posted.astimezone(pytz.timezone(
            'Europe/Kiev')).strftime('%d.%m.%y %H:%M'),
        'id': comment.id,
        'liked': request.user in comment.likes.all(),
        'likes_count': comment.likes.count()
    } for comment in post.comments.order_by('posted')]}
    return JsonResponse(comments, safe=False)


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        return JsonResponse({'likes_count': comment.likes.count(),
                             'liked': False})
    comment.likes.add(request.user)
    return JsonResponse({'likes_count': comment.likes.count(),
                         'liked': True})
