from django.db import models


class Category(models.Model):
    '''
    unused. I initially was hoping to store the category information in the database and realized that there's no need.
    I stored it in a csv file instead.
    '''
    title = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'yelp'
