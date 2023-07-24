from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .. import views


class TestUrls(SimpleTestCase):
    """Tests for urls. Check for binding of functions with urls."""
    def test_signup_url_resolves(self):
        """Check for sign up url.
        :return:
        """
        url = reverse('feed:signup')
        self.assertEquals(resolve(url).func, views.signup_user)

    def test_activate_user_url_resolves(self):
        """Check for activate user url.
        :return:
        """
        url = reverse('feed:activate_user', args=['Ai', '02130'])
        self.assertEquals(resolve(url).func, views.activate_user)

    def test_login_url_resolves(self):
        """Check for login url.
        :return:
        """
        url = reverse('feed:login')
        self.assertEquals(resolve(url).func, views.login_user)

    def test_logout_url_resolves(self):
        """Check for logout url.
        :return:
        """
        url = reverse('feed:logout')
        self.assertEquals(resolve(url).func, views.logout_user)

    def test_user_profile_url_resolves(self):
        """Check for user's profile url.
        :return:
        """
        url = reverse('feed:user_profile', args=[1])
        self.assertEquals(resolve(url).func, views.user_profile)

    def test_user_edit_profile_url_resolves(self):
        """Check for edit user profile url.
        :return:
        """
        url = reverse('feed:user_edit_profile', args=[1])
        self.assertEquals(resolve(url).func, views.user_edit_profile)

    def test_follow_url_resolves(self):
        """Check for follow url."""
        url = reverse('feed:follow', args=[1])
        self.assertEquals(resolve(url).func, views.follow)

    def test_followers_url_resolves(self):
        """Check for followers url."""
        url = reverse('feed:followers', args=[1])
        self.assertEquals(resolve(url).func, views.followers)

    def test_following_url_resolves(self):
        """Check for following url."""
        url = reverse('feed:following', args=[1])
        self.assertEquals(resolve(url).func, views.following)

    def test_feed_url_resolves(self):
        """Check for feed url.
        :return:
        """
        url = reverse('feed:feed')
        self.assertEquals(resolve(url).func, views.feed)

    def test_create_post_url_resolves(self):
        """Check for create post url.
        :return:
        """
        url = reverse('feed:create_post')
        self.assertEquals(resolve(url).func, views.create_post)

    def test_like_url_resolves(self):
        """Check for like url.
        :return:
        """
        url = reverse('feed:like', args=[1])
        self.assertEquals(resolve(url).func, views.like)

    def test_make_comment_url_resolves(self):
        """Check for make comment url."""
        url = reverse('feed:make_comment', args=[1])
        self.assertEquals(resolve(url).func, views.make_comment)

    def test_like_comment_url_resolves(self):
        """Check for like comment url."""
        url = reverse('feed:like_comment', args=[1])
        self.assertEquals(resolve(url).func, views.like_comment)

    def test_signup_redirect_url_resolves(self):
        """Check for signup redirect url."""
        url = reverse('feed:signup_redirect')
        self.assertEquals(resolve(url).func, views.signup_redirect)
