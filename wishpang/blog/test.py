from email import contentmanager
from multiprocessing import AuthenticationError
import factory, factory.fuzzy
from faker import Faker
from django.contrib.auth.models import User
from blog.models import Post, Comment
from django.contrib.auth.hashers import make_password
fake=Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=User

    username=factory.Faker('name')
    password=factory.LazyFunction(lambda: make_password('password'))


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Post

    title=factory.Faker('sentence')
    contents=factory.Faker('sentence')
    auth=factory.fuzzy.FuzzyChoice(User.objects.all())

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Comment
    post=factory.fuzzy.FuzzyChoice(Post.objects.all())
    contents=factory.Faker('sentence')
    auth=factory.fuzzy.FuzzyChoice(User.objects.all())

class likeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Post
    post=Post.objects.all().first()
    auth=User.objects.all().order_by('?').first()
    if post.liker.filter(id=auth.id).exists():
                post.liker.remove(auth)
    else:
        post.liker.add(auth)
    
# user=UserFactory.create_batch(10)


# posts=PostFactory.create_batch(10)

# for post in posts:
#     print(post)

for _ in range(10):
    likeFactory.create_batch(1)


# comments=CommentFactory.create_batch(100)

# for comment in comments:
#     print(comment.contents)