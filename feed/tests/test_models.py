from django.test import TestCase

from ..models import User, Post, Image, Comment


class ModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', bio='test bio')
        self.post = Post.objects.create(
            description='post description',
            owner=self.user,
        )

    def test_user_model(self):
        """Get created User object and check data."""
        user = User.objects.get(username='testuser')
        self.assertEquals(user.bio, 'test bio')

    def test_post_model(self):
        """Get Post object and check data."""
        post = Post.objects.get(owner=self.user)
        self.assertEquals(post.description, 'post description')

    def test_add_tags_to_post(self):
        """Add tags to the post and check it."""
        self.post.tags.add('tag1', 'tag2', 'tag3')
        self.post.save()
        post = Post.objects.get(owner=self.user)
        self.assertIn('tag2', [tag.name for tag in post.tags.all()])

    def test_image_model(self):
        """Create and get an Image object and check it."""
        Image.objects.create(
            post=self.post,
            image='post/images/fake_image.jpg',
        )
        image = Image.objects.get(post=self.post)
        self.assertEquals(image.image.url,
                          'https://res.cloudinary.com/dscyxplsu/'
                          'image/upload/v1/post/images/fake_image.jpg')

    def test_comment_model(self):
        """Create and get a Comment object and check it."""
        Comment.objects.create(
            post=self.post,
            text='test comment',
            owner=self.user
        )
        comment = Comment.objects.get(post=self.post)
        comments = self.post.comments.all()
        self.assertEquals(comment.text, 'test comment')
        self.assertTrue(comment in comments)
