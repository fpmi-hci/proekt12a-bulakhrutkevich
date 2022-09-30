from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse

from autoslug import AutoSlugField


# Create your models here.
class UserAccount(AbstractUser):
    # for Deactivate Account
    # we should use is_active attribute

    def __str__(self):
        return self.username


class FriendListManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_mutual_friends(self, user1, user2):
        friends1 = self.get_queryset().get(user=user1).friends.all()
        friends2 = self.get_queryset().get(user=user2).friends.all()
        return friends1.intersection(friends2).difference(UserAccount.objects.filter(pk__in=(user1.id, user2.id)))


class FriendRequestManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def clean(self):
        self.get_queryset().filter(is_active=False).delete()


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                     related_name='friends')

    objects = FriendListManger()

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                                  , related_name='sent')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                                , related_name='received')

    is_active = models.BooleanField(default=True, blank=True, null=True)

    objects = FriendRequestManger()

    def accept(self):
        sender = FriendList.objects.get(user=self.from_user)
        receiver = FriendList.objects.get(user=self.to_user)
        if sender and receiver:
            sender.add_friend(receiver)
            receiver.add_friend(sender)
            self.is_active = False
            self.save()

    def decline(self):
        self.is_active = False
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.user.username} comment : on {self.post.user.username} post'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user.username} like : on {self.post.user.username} post'


class Unlike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE, related_name='unlikes')

    def __str__(self):
        return f'{self.user.username} unlike : on {self.post.user.username} post'


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    slug = AutoSlugField(unique=True, populate_from='user.username')

    def __str__(self):
        return self.text

    def get_absolute_path(self):
        return reverse('posts:view', args=[self.slug])


class PostManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def add_like(self, user, post):
        # if there unlike then delete it before make like
        unlike = Unlike.objects.get(user=user, post=post)
        if unlike:
            unlike.delete()
        like, _ = Like.objects.get_or_create(user=user, post=post)

    def add_unlike(self, user, post):
        # if there like then delete it before make unlike
        like = Unlike.objects.get(user=user, post=post)
        if like:
            like.delete()
        unlike, _ = Unlike.objects.get_or_create(user=user, post=post)


class Story(models.Model):
    image = models.ImageField(upload_to='stories/')
    text = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    def get_url(self):
        return self.image.url


class Profile(models.Model):
    name = models.CharField(max_length=50, blank=True)
    slug = AutoSlugField(unique=True, populate_from='name', always_update=True)
    location = models.CharField(max_length=50, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='users_images/')

    def __str__(self):
        return self.name

    def get_absolute_path(self):
        return reverse('user_profile:view', args=[self.slug])
