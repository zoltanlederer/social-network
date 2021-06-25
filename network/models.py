from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    sex = (
        ('Female', 'Female'),
        ('Male', 'Male'),
    )

    gender = models.CharField(max_length=300, choices = sex)
    avatarURL = models.URLField(max_length=500, default='https://none.com')
    

class Posts(models.Model):
    class Meta:
        verbose_name_plural = 'Posts'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=4096)
    total_likes = models.IntegerField(default=0)  
    created = models.DateTimeField(auto_now_add=True)

    # For API GET request
    def create_dict(self):
        return {
            "id": self.id,
            "post": self.post,
            "total_likes": self.total_likes,
            "created": self.created.strftime("%b %d %Y, %I:%M %p")
        }


class Likes(models.Model):
    class Meta:
        verbose_name_plural = 'Likes'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postid = models.ForeignKey(Posts, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.IntegerField()

