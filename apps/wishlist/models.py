# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from ..login.models import User
import datetime

class WishManager(models.Manager):
    def addWishlist(self, postData):
        user = User.objects.get(id=postData['user'])
        try:
            existing_wishlist = Wishlist.objects.get(item=postData['item'])
            error = "The same Wishlist already exists!"
            return error
        except:            
            return Wishlist.objects.create(item=postData['item'], user=user)        

    def getAllMyList(self, user_id):               
        return Wishlist.objects.filter(wished_by=User.objects.get(id=user_id)) | Wishlist.objects.filter(user=user_id)

    def getMyItem(self, user_id):
        return Wishlist.objects.filter(user=user_id)        

    def getOtherList(self, user_id):
        otherlist = []
        wishlist = Wishlist.objects.all().exclude(user=User.objects.get(id=user_id)).order_by('created_at')
        for wish in wishlist:
            if len(wish.wished_by.filter(id=user_id)) == 0:
                otherlist.append(wish)
        return otherlist
    
    def getAllwished_by(self, wishlist_id):
        return User.objects.filter(wishlists__id=wishlist_id)

    def validate(self, postData):
        errorMessages = []
        if len(postData['item']) < 3:
            errorMessages.append('Item name has to be more than 3 characters')
        if len(postData['item']) == 0:
            errorMessages.append('Item name cannot be empty!')
        return errorMessages

    def addMyList(self, user_id, wishlist_id):
        this_user = User.objects.get(id=user_id)
        this_wishlist = Wishlist.objects.get(id=wishlist_id)
        errors = []

        if len(User.objects.filter(id=user_id)) == 0:
            errors.append('This is not a user')
        try:
            existing_wishlist = Wishlist.objects.get(user=this_user)
            error = "The same wishlist already exists!"
            return error
        except:
            return this_user.wishlists.add(this_wishlist)
    
    def removeFromList(self, user_id, wishlist_id):
        this_user = User.objects.get(id=user_id)
        this_wishlist = this_user.wishlists.all().get(id=wishlist_id)
        errors = []

        if len(User.objects.filter(id=user_id)) == 0:
            errors.append('This is not a user')
        try:
            existing_list = Wishlist.objects.get(user=this_user)
            error = "The same list already exists!"
            return error
        except:
            return this_user.wishlists.remove(this_wishlist)
        

class Wishlist(models.Model):
    item = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="wish_item")
    wished_by = models.ManyToManyField(User, related_name="wishlists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()