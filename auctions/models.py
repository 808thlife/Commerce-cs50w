from django.contrib.auth.models import AbstractUser
from django.db import models
import time 

class User(AbstractUser):
    username = models.CharField(max_length=32, unique = True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ()

class Category(models.Model):
    categoryName = models.CharField(max_length=50)
    
    def __str__(self):
        return self.categoryName 
    
     
class Listing(models.Model):
    title = models.CharField(max_length= 64)
    description = models.CharField(max_length= 128)
    img = models.ImageField(upload_to = 'auctions/media/images')
    isActive = models.BooleanField(default= True, blank=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user")
    categories = models.ForeignKey(Category, on_delete = models.CASCADE, blank= True, null = True, related_name = "category", default = "None")
    price = models.IntegerField(default = 0)
    watchlist = models.ManyToManyField(User, blank = True, null = True, related_name = "userTo")

    def __str__(self):
        return self.title   
    
class Bid(models.Model):
    bid_offer = models.IntegerField()
    listing_offer = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "listings", null = True)
    bid_owner= models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.bid_offer}$ on {self.listing_offer} by {self.bid_owner}"


class Comments(models.Model):
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE,)

    def __str__(self):
        return f'Comment by {self.writer} on the listing {self.listing.title}'