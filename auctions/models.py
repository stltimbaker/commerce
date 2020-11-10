from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import time, date


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.description})"

class Listing(models.Model):
    itemName = models.CharField(max_length=64)
    itemShortDescription = models.CharField(max_length=24)
    itemLongDescription = models.TextField()
    setPrice = models.DecimalField(max_digits=7,decimal_places=2)
    listedBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="listings"
    )
    imageURL = models.URLField()
    isOpen = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}:{self.itemName} - {self.itemShortDescription} (by: {self.listedBy})"

class Bid(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    amount = models.DecimalField(max_digits=7,decimal_places=2)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

class Comment(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    comment = models.TextField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

class Watch(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watches"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="watches"
    )
    def __str__(self):
        return f"{self.user}:{self.listing}"
