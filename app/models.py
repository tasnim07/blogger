from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, related_name='posts',
                               on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, related_name='like',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='like',
                             on_delete=models.CASCADE)
