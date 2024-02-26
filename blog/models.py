from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'Блог пользователя "{self.user.username}"'
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.blog.user.username} - {self.title}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subscriber} подписался на {self.blog.user}'