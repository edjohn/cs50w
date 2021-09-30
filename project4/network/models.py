from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} said {self.content} on {self.creation_date}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return f"{self.user} liked {self.post}"

class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_users")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__():
        return f""