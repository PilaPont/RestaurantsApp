from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from .validator import validate_category
from django.conf import settings
from django.urls import reverse
from django.db.models import Q


User = settings.AUTH_USER_MODEL


class RestaurantLocationQuerySet(models.query.QuerySet):
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query)|
                Q(location__icontains=query)|
                Q(location__iexact=query)|
                Q(category__icontains=query)|
                Q(category__iexact=query)|
                Q(item__name__icontains=query)|
                Q(item__contents__icontains=query)
                ).distinct()
        return self


class RestaurantLocationManager(models.Manager):
    def get_queryset(self):
        return RestaurantLocationQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class RestaurantLocation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, null=True, blank=True)
    category = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)
    objects = RestaurantLocationManager()

    def __str__(self):
        return self.name

    """Instead of using success url in Detail class,use reverse and absolute url"""

    def get_absolute_url(self):
        return reverse('restaurants:detail', kwargs={'slug': self.slug})

    @property
    def title(self):
        return self.name


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    print('Saving...', instance.timestamp)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

#
# def rl_post_save_receiver(sender, instance, created, *args, **kwargs):
#     print('Saved', instance.timestamp)
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#         instance.save()


pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)
# post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)
