import faker
from django.core.management.base import BaseCommand
from django.db import transaction
from django.shortcuts import get_object_or_404

from ...models import User, Post, Image

FAKE_IMAGE_PATH = 'post/images/fake_image.jpg'

fake = faker.Faker()
generators = {}
user_ids = []


def generators_sort():
    """Sort generators dictionary by dependencies."""
    visited = set()
    stack = {}
    global generators

    def dfs(node):
        if node in visited:
            return
        visited.add(node)

        if node in generators:
            for dependency in generators[node][0]:
                dfs(dependency)

            stack[node] = generators[node]

    for node in generators:
        dfs(node)

    generators = stack


def register(deps: list = None):
    """Register function in generators dictionary and call
    sorting function.
    :param deps:
    :return:
    """
    if deps is None:
        deps = []

    def decorator(func):
        generators[func.__name__] = (deps, func)

        generators_sort()
        return func
    return decorator


@register(deps=['create_fake_user'])
def create_fake_post():
    """Create fake post.
    :return:
    """
    with transaction.atomic():
        for user_id in user_ids:
            user = get_object_or_404(User, pk=user_id)
            for _ in range(2):
                post = Post.objects.create(
                    owner=user,
                    description=fake.paragraph(nb_sentences=2),
                )
                post.tags.add(*fake.words(nb=3))
                post.save()
                for _ in range(2):
                    Image.objects.create(post=post,
                                         image=FAKE_IMAGE_PATH)


@register()
def create_fake_user():
    """Create 2 fake users.
    :return:
    """
    with transaction.atomic():
        for _ in range(2):
            user_data = fake.profile()
            first_name, last_name = user_data['name'].split(maxsplit=1)
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['mail'],
                first_name=first_name,
                last_name=last_name,
                bio=fake.paragraph(nb_sentences=4)
            )
            user_ids.append(user.id)


class Command(BaseCommand):
    """CLI command for adding fake users with fake posts."""
    help = 'Add 2 fake users with fake posts.'

    def handle(self, *args, **options):
        for name, (deps, func) in generators.items():
            func()
        self.stdout.write(
            self.style.SUCCESS('Successfully created.'))
