from django.test import TestCase

from ..forms import SignUpForm, EditProfile, CreatePostForm


class TestForms(TestCase):

    def test_sign_up_form(self):
        """Test for sign up form.
        :return:
        """
        form = SignUpForm(data={
            'username': 'testuser',
            'password1': 'test_1234',
            'password2': 'test_1234',
            'email': 'test@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_edit_profile_form(self):
        """Test for edit profile form.
        :return:
        """
        form = EditProfile(data={
            'username': 'testuser',
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@example.com',
            'bio': 'test bio',
        })
        self.assertTrue(form.is_valid())

    def test_post_form(self):
        """Test for post creation form."""
        form = CreatePostForm(data={
            'description': "post description",
            'tags': 'tag1, tag2, tag3'
        })
        self.assertTrue(form.is_valid())
