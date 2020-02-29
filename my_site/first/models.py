from django.db import models
# Create your models here.


class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.search

    class Meta:
        verbose_name_plural = "Searches"


class Product(models.Model):
    name = models.CharField(max_length=500)
    prize = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to="static/images/")

    def __str__(self):
        return '{}'.format(self.name)
