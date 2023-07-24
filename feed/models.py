from django.contrib.auth.models import AbstractUser
from django.db import models
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField

POST_IMAGE_PATH = 'post/images'
PROFILE_IMAGES_PATH = 'user/images'
DEFAULT_PROFILE_IMAGE_PATH = 'user/images/default_user.png'


class User(AbstractUser):
    """User model. Standard User model supplemented with fields bio and
    profile image."""
    bio = models.TextField(blank=True)
    profile_image = CloudinaryField(
        'profile_image',
        folder=PROFILE_IMAGES_PATH,
        default=DEFAULT_PROFILE_IMAGE_PATH)
    followers = models.ManyToManyField('self', related_name='following',
                                       symmetrical=False,
                                       blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    """Post model. Contains description, owner(user who created post),
    likes(list of users who liked this post), tags and posted(date and
    time when it were posted) fields."""
    description = models.TextField(max_length=400,
                                   help_text='Write a description',
                                   blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='owner')
    likes = models.ManyToManyField(User, related_name='liked',
                                   blank=True)
    tags = TaggableManager(blank=True)
    posted = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    """Image model. Relates to Post model. Representation of posts images."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = CloudinaryField('post_image', folder=POST_IMAGE_PATH)


class Comment(models.Model):
    """Comment model. Relates to Post and User model.
    Representation of comments for posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    text = models.TextField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='comments')
    likes = models.ManyToManyField(User, related_name='liked',
                                   blank=True)
    posted = models.DateTimeField(auto_now_add=True)
