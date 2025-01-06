from django.core.management import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import random
from app.app.models import Post, Comment



class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()

        for i in range(5):
            User.objects.create_user(username = fake.user_name(),
                                     email = fake.email(),
                                     password = 'random_password_321')

        users = list(User.objects.all())

        for i in range(10):
            Post.objects.create(title = fake.sentence(nb_words=5),
                                content = fake.paragraph(10),
                                author = random.choice(users))

        posts = list(Post.objects.all())

        for i in range(30):
            Comment.objects.create(author = random.choice(users),
                                   content = fake.paragraph(3),
                                   post = random.choice(posts))

    print("all done")