# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Wishlist
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:        
        context = { 'user': User.objects.get(id=request.session['user_id']),
                    'wishlists': Wishlist.objects.getAllMyList(request.session['user_id']),
                    'mine': Wishlist.objects.getMyItem(request.session['user_id']),
                    'otherlists': Wishlist.objects.getOtherList(request.session['user_id']) }
        return render(request,'wishlist/index.html', context )

def create(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:        
        return render(request,'wishlist/create.html')

def creatWishlist(request):
    if request.method == "POST":
        wishlist = Wishlist.objects.validate(request.POST)     
        if wishlist:
            for error in wishlist:
                messages.add_message(request, messages.INFO, error)
            print "in if"
            return redirect('/wishlist/wish_items/create')
        else:
            postData = { 'user': request.session['user_id'],
                        'item': request.POST['item'] }
            wish = Wishlist.objects.addWishlist(postData)
            if not isinstance(wish, Wishlist):
                messages.add_message(request, messages.ERROR, wish)       
                print 'in not isinstance' 
                return redirect('/wishlist/dashboard') 
            print 'taking me to dashboard'
            return redirect('/wishlist/dashboard')   

def addToMyList(request, id):        
    try:
        if request.method == "GET":    
            # add to favorite
            Wishlist.objects.addMyList(request.session['user_id'], id)
            return redirect('/wishlist/dashboard')
    except:
        print 'Cannot add to list'
        return redirect('/wishlist/dashboard')

def removeMyList(request, wishlist_id):
    try:
        if request.method == "GET":
            Wishlist.objects.removeFromList(request.session['user_id'], wishlist_id)
            return redirect('/wishlist/dashboard')
    except:
        print 'Cannot remove from fav list'
        return redirect('/wishlist/dashboard')

def view(request, wishlist_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:        
        context = { 'wished_by': Wishlist.objects.getAllwished_by(wishlist_id),
                    'items': Wishlist.objects.get(id=wishlist_id) }
        return render(request, 'wishlist/view.html', context) 

def delete_item(request, wishlist_id):
    Wishlist.objects.get(id=wishlist_id).delete()
    return redirect('/wishlist/dashboard')