"""pipicky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from restaurants.views import TemplateView
from restaurants.views import (
    # restaurant_listview,
    RestaurantListView,
    RestaurantDetailView,
    restaurant_createview,
    # RestaurantCreateView
)
from django.contrib.auth.views import LoginView, LogoutView
from profiles.views import ProfileFollowToggle, RegisterView, \
    activate_user_view
from menus.views import HomeView

"""class based view related to line 53 in views.py"""
# from restaurants.views import HomeView, AboutView, ContactView
#
# """instead of above line you can import TemplateView, use TemplateView
# instead of any page view in path and just write Template_name= page.html,
# inside parenthesis in as_view() """
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', TemplateView.as_view(template_name='home.html')),
#     path('about/', TemplateView.as_view(template_name='about.html')),
#     path('contact/', TemplateView.as_view(template_name='contact.html')),
# ]


"""build new view using models.py"""

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^register/$', RegisterView.as_view(), name='register'),
    re_path(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    re_path(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
    re_path(r'^restaurants/', include(('restaurants.urls', 'restaurants'), namespace='restaurants')),
    re_path(r'^items/', include(('menus.urls', 'menus'), namespace='menus')),
    re_path(r'^u/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    # re_path(r'^restaurants/$', RestaurantListView.as_view(), name='restaurants'),
    # re_path(r'^restaurants/create/$', RestaurantCreateView.as_view(), name='restaurant_create'),
    # re_path(r'^restaurants/create/$', restaurant_createview),
    # re_path(r'^restaurants/(?P<slug>\w+)/$', RestaurantListView.as_view()),
    # re_path(r'^restaurants/(?P<slug>[\w-]+)/$', RestaurantDetailView.as_view(), name='restaurant_detail'),
    re_path(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    re_path(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
]
