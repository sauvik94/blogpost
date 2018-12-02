from django.db import models


class Post(models.Model):
    email = models.CharField(max_length=150)
    title = models.CharField(max_length=200,blank=True, null=True)
    story = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(null=False, default=False)

    def __str__(self):
        return 'Title : ' + self.title
