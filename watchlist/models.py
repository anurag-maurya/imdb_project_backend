from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=100)
    
    def __str__(self) -> str:
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    
    def __str__(self):
        return self.title
    
    
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating)+" | "+self.watchlist.title
