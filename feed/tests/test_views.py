from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
import re

from ..models import User, Post, Comment
from ..forms import EditProfile, CreatePostForm


class SignUpViewTest(TestCase):
    """Test sign up page."""
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('feed:signup')

    def test_signup_GET(self):
        """Get sign up page."""
        response = self.client.get(self.signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed/signup_user.html')
        self.assertContains(response, 'Sign Up')

    def test_signup_POST(self):
        """Post sign up and register user."""
        self.assertEquals(len(mail.outbox), 0)

        response = self.client.post(self.signup_url, {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject,
                          'Activate your account.')
        user = User.objects.get(username='test')
        self.assertNotEqual(user.is_active, True)

    def test_wrong_password_signup_POST(self):
        """Check for wrong password input."""
        response = self.client.post(self.signup_url, {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword1',
            'email': 'test@example.com',
        })
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Passwords did not match!")
        self.assertEquals(len(mail.outbox), 0)

    def test_wrong_username_signup_POST(self):
        """Check uniqueness of username"""
        User.objects.create_user(username='test')
        response = self.client.post(self.signup_url, {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
        })
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,
                            "That username has already been taken. "
                            "Please choose a new username.")
        self.assertEquals(len(mail.outbox), 0)

    def test_signup_redirect(self):
        response = self.client.get(reverse('feed:signup_redirect'))
        self.assertRedirects(response, reverse('feed:login'))


class ActivateUserViewTest(TestCase):
    """Test account activation."""
    def setUp(self):
        self.client = Client()

    def test_activate_user(self):
        """Test account activation through email confirmation."""
        self.client.post(reverse('feed:signup'), {
            'username': 'test',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
        })
        user = User.objects.get(username='test')
        self.assertEquals(user.is_active, False)
        activate_link = re.search("(?P<url>https?://[^\s]+)",
                                  mail.outbox[0].body).group('url')
        response = self.client.get(activate_link)
        user = User.objects.get(username='test')
        self.assertEquals(user.is_active, True)
        self.assertEquals(response.status_code, 302)


class LoginLogoutUserViewTest(TestCase):
    """Test login page, and logout functionality."""
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('feed:login')
        self.user = User.objects.create_user(username='test',
                                             password='testpassword')

    def test_login_user_GET(self):
        """Get login page."""
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_user_POST(self):
        """Test login user and redirecting."""
        response = self.client.post(self.login_url, {
            'username': 'test',
            'password': 'testpassword'
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('feed:feed'))

    def test_wrong_login_user_POST(self):
        """Check wrong data input."""
        response = self.client.post(self.login_url, {
            'username': 'test',
            'password': 'testpassword1'
        })
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Username and password '
                                      'did not match.')

    def test_logout_user(self):
        """Test logout functionality."""
        self.client.login(username='test', password='testpassword')
        response = self.client.post(reverse('feed:logout'))
        self.assertRedirects(response, reverse('feed:login'))


class UserProfileViewTest(TestCase):
    """Test user's profile page."""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test',
                                             email='test@example.com',
                                             password='testpassword',
                                             bio='test bio')
        self.user_profile_url = reverse('feed:user_profile',
                                        args=[self.user.id])
        self.user_edit_profile_url = reverse('feed:user_edit_profile',
                                             args=[self.user.id])

    def test_user_profile_not_logged_in(self):
        """Test redirecting if user isn't logged in."""
        response = self.client.get(self.user_profile_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             f'/auth/login?next=/users/{self.user.id}')

    def test_user_profile_logged_in(self):
        """Get user's profile page."""
        self.client.login(username='test', password='testpassword')
        response = self.client.get(self.user_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Edit')

    def test_impossibility_to_edit_someone_else_profile(self):
        """Check impossibility to edit someone else's profile."""
        self.client.login(username='test', password='testpassword')
        user_2 = User.objects.create_user(username='test2')
        response = self.client.get(reverse('feed:user_profile',
                                           args=[user_2.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(b'Edit' not in response.content)
        response = self.client.get(reverse('feed:user_edit_profile',
                                           args=[user_2.id]))
        self.assertRedirects(response, reverse('feed:user_profile',
                                               args=[user_2.id]))

    def test_edit_user_profile_GET(self):
        """Get edit user profile page."""
        self.client.login(username='test', password='testpassword')
        response = self.client.get(self.user_edit_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Username:')

    def test_edit_user_profile_POST(self):
        """Check editing profile data."""
        self.client.login(username='test', password='testpassword')
        form = EditProfile(instance=self.user)
        form.initial['bio'] = 'changed bio'
        response = self.client.post(self.user_edit_profile_url,
                                    form.initial)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.user_profile_url)
        user = User.objects.get(username='test')
        self.assertEquals(user.bio, 'changed bio')

    def test_follow(self):
        """Check subscribe post functionality."""
        self.client.login(username='test', password='testpassword')
        test_user_2 = User.objects.create_user(username='test_user_2')
        url = reverse('feed:follow', args=[test_user_2.id])
        # Check follow
        self.client.get(url)
        self.assertTrue(self.user in test_user_2.followers.all())
        # Check unfollow
        self.client.get(url)
        self.assertFalse(self.user in test_user_2.followers.all())

    def test_followers(self):
        """Check followers view."""
        self.client.login(username='test', password='testpassword')
        response = self.client.get(reverse('feed:followers',
                                           args=[self.user.id]))
        self.assertContains(response, 'Followers', status_code=200)

    def test_following(self):
        """Check followers view."""
        self.client.login(username='test', password='testpassword')
        response = self.client.get(reverse('feed:following',
                                           args=[self.user.id]))
        self.assertContains(response, 'Following', status_code=200)


class FeedViewTest(TestCase):
    """Test for feed, create post and like pages."""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test',
                                             password='testpassword')
        self.feed_url = reverse('feed:feed')
        self.create_post_url = reverse('feed:create_post')

    def test_get_feed_not_logged_in(self):
        """Check redirect if user isn't logged in."""
        response = self.client.get(self.feed_url)
        self.assertRedirects(response,
                             '/auth/login?next=/feed/',
                             status_code=302)

    def test_get_feed(self):
        """Check feed response with 1 created post."""
        self.client.login(username='test', password='testpassword')
        Post.objects.create(description='post description',
                            owner=self.user)
        response = self.client.get(self.feed_url)
        self.assertContains(response, 'post description',
                            status_code=200)

    def test_get_create_post_not_logged_in(self):
        """Check redirect if user isn't logged in."""
        response = self.client.get(self.create_post_url)
        self.assertRedirects(response,
                             '/auth/login?next=/posts/create',
                             status_code=302)

    def test_get_create_post(self):
        """Get create post page and check it."""
        self.client.login(username='test', password='testpassword')
        response = self.client.get(self.create_post_url)
        self.assertContains(response, 'Create post',
                            status_code=200)

    def test_post_create_post(self):
        """Create post via create post page."""
        self.client.login(username='test', password='testpassword')
        form = CreatePostForm(initial={
            'description': 'post description',
            'tags': 'tag1, tag2, tag3'
        })
        response = self.client.post(self.create_post_url,
                                    data=form.initial)
        self.assertRedirects(response, reverse('feed:feed'),
                             status_code=302)
        post = Post.objects.get(owner=self.user)
        self.assertEquals(post.description, 'post description')

    def test_like_post(self):
        """Check for like post.
        :return:
        """
        self.client.login(username='test', password='testpassword')
        post = Post.objects.create(description='post description',
                                   owner=self.user)
        response = self.client.get(reverse('feed:like',
                                           args=[post.id]))
        self.assertJSONEqual(response.content,
                             {'likes_count': 1, 'liked': True})
        post = Post.objects.get(owner=self.user)
        self.assertEquals(post.likes.count(), 1)

    def test_unlike_post(self):
        """Check unlike post.
        :return:
        """
        self.client.login(username='test', password='testpassword')
        post = Post.objects.create(description='post description',
                                   owner=self.user)
        post.likes.add(self.user)
        self.client.get(reverse('feed:like', args=[post.id]))
        post = Post.objects.get(owner=self.user)
        self.assertEquals(post.likes.count(), 0)


class CommentTests(TestCase):
    """Tests for make comment and like comment."""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test',
                                             password='testpassword')
        self.client.login(username='test', password='testpassword')
        self.post = Post.objects.create(description='post description',
                                        owner=self.user)
        self.comment = Comment.objects.create(
            owner=self.user,
            text='test comment',
            post=self.post
        )

    def test_make_comment(self):
        """Create a comment and check it."""
        response = self.client.get(reverse('feed:feed'))
        self.assertContains(response, b'test comment')

    def test_like_comment(self):
        """Like comment check."""
        self.client.get(reverse('feed:like_comment', args=[self.comment.id]))
        self.assertEquals(1, self.comment.likes.count())
        self.assertTrue(self.user in self.comment.likes.all())

    def test_unlike_comment(self):
        """Unlike comment check."""
        self.comment.likes.add(self.user)
        self.client.get(reverse('feed:like_comment', args=[self.comment.id]))
        self.assertEquals(0, self.comment.likes.count())
        self.assertFalse(self.user in self.comment.likes.all())
