from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.index, name="index"),
    url(r'^wish_items/create$', views.create, name="create"),
    url(r'^wish_items/(?P<wishlist_id>\d*)$', views.view, name="view"),
    url(r'^wish_items/creatWishlist', views.creatWishlist, name="creatWishlist"),
    url(r'^addToMyList/(?P<id>\d*)$', views.addToMyList, name="addToMyList"),
    # url(r'^viewUser/(?P<user_id>\d*)$', views.viewUser, name="viewUser"),
    url(r'^delete_item/(?P<wishlist_id>\d*)$', views.delete_item, name="delete_item")
]