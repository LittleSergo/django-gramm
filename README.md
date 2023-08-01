# DjangoGramm

DjangoGramm is my pet project. It is a simple django application that repeats the idea of Instagram. 
Users can sign up, create posts, see posts in feed, like and comment them, and follow each other.

## Authentication

The application provides the authentication with email confirmation. Users must activate their 
accounts via email verification, or they will not be able to log in. After confirming the e-mail, 
after which he can freely log in, the user will be redirected to the profile page. 

## Profile page, editing and following

There, users can add a profile picture and edit profile information, and can see who is following 
it and who the user is following. If user go to another users page, he can follow this profile and 
unfollow as well.

## Feed

Feed is divided onto 2 sections, first one is the main feed section where all posts are located.
Second is the following section where user can watch on the posts that following users posted.

## Post

Post is a single unit of feed. Posts consist of image or images, description, likes (users 
can like posts and unlike as well), tags and comments section.

### Comments

Users can write comments to each post, and like them the same way as posts. At the first view 
user can see only 3 comments maximum, but he can expand it and see them all, and collapse sa well.

### Creating post

If user is logged in, he can find the 'Create post' button, if he clicks on, he will be redirected
to the post creation page. There user can choose the photos for new post, or one photo, add description,
tags and finally create the post.

## Fake data

You can actually add fake data into this app. It's simple just write command in the command line:

```commandline
python manage.py fake_data
```

And that command will add two users, with two posts each, where will be two photos.
