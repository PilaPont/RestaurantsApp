from .views import (
    # restaurant_listview,
    # restaurant_createview,
    RestaurantListView,
    RestaurantDetailView,
    RestaurantCreateView,
    RestaurantUpdateView
)

from django.urls import path, re_path

urlpatterns = [

    re_path(r'^$', RestaurantListView.as_view(), name='list'),
    re_path(r'^create/$', RestaurantCreateView.as_view(), name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$', RestaurantUpdateView.as_view(), name='detail'),
    # re_path(r'^(?P<slug>[\w-]+)/edit/$', RestaurantUpdateView.as_view(), name='edit'),
]
