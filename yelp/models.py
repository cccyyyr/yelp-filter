from django.db import models


class Category(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'yelp'
