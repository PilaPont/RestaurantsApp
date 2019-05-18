from django.db.models import Q
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation

# Create your views here.
"""function based view"""
# def home_old(request):
#     # response
#     html_var = 'f strings'
#     html_ = f"""<!doctype html>
#     <html lang="en">
#     <head>
#     </head>
#     <body>
#     <h1>Hello World!</h1>
#     <p>
#         This is {html_var} coming through
#     </p>
#     </body>
#     </html>"""
#     # f strings
#     return HttpResponse(html_)
#
#
# def home(request):
#     num = None
#     some_list = [
#         random.randint(0, 100000000),
#         random.randint(0, 100000000),
#         random.randint(0, 100000000)
#     ]
#     condition_bool_item = False
#     if condition_bool_item:
#         num = random.randint(0, 100000000)
#     context = {
#         "num": num,
#         "some_list": some_list
#     }
#     return render(request, "home.html", context)
#
#
# def about(request):
#     context = {}
#     return render(request, "about.html", context)


# def contact(request):
#     context = {}
#     return render(request, "contact.html", context)

"""class based view"""
# class ContactView(View):
#     def get(self, request, arg, **kwargs):
#         context = {}
#         return render(request, "contact.html", context)
# class HomeView(TemplateView):
#     template_name = 'home.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(HomeView, self).get_context_data(*args, **kwargs)
#         num = None
#         some_list = [
#             random.randint(0, 100000000),
#             random.randint(0, 100000000),
#             random.randint(0, 100000000)
#         ]
#         condition_bool_item = True
#         if condition_bool_item:
#             num = random.randint(0, 100000000)
#         context = {
#             "num": num,
#             "some_list": some_list
#         }
#         print(context)
#         return context
#
#
# class AboutView(TemplateView):
#     template_name = 'about.html'
#
#
# class ContactView(TemplateView):
#     template_name = 'contact.html'


"""make a new view using model.py"""


# def restaurant_listview(request):
#     template_name = 'restaurants/restaurantlocation_list.html'
#     queryset = RestaurantLocation.objects.all()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, template_name, context)


class RestaurantListView(LoginRequiredMixin, ListView):

    # def get_queryset(self):
    #     slug = self.kwargs.get('slug')
    #     if slug:
    #         queryset = RestaurantLocation.objects.filter(
    #             Q(category__iexact=slug) |
    #             Q(category__icontains=slug)
    #         )
    #     else:
    #         queryset = RestaurantLocation.objects.all()
    #     return queryset
    #     or in forward steps:
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)

    # def get_context_data(self, **kwargs):
    #     print(self.kwargs)
    #     context = super(RestaurantDetailView, self).get_context_data(**kwargs)
    #     print('get_context_data:', context)
    #     return context

    # def get_object(self, **kwargs):
    #     rest_id = self.kwargs.get('rest_id')
    #     obj = get_object_or_404(RestaurantLocation, id=rest_id)
    #     return obj
    #


@login_required(login_url='/login/')
def restaurant_createview(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    errors = None
    if form.is_valid():
        if request.user.is_authenticated:
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            # """use Model Forms instead of Forms. below obj belongs to Forms"""
            # obj = RestaurantLocation.objects.create(
            #     name=form.cleaned_data.get('name'),
            #     location=form.cleaned_data.get('location'),
            #     category=form.cleaned_data.get('category'),
            # )
            return HttpResponseRedirect('/restaurants/')
        else:
            return HttpResponseRedirect('/login/')
    if form.errors:
        errors = form.errors

    template_name = 'restaurants/form.html'
    context = {'form': form, 'errors': errors}
    return render(request, template_name, context)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    login_url = '/login/'
    template_name = 'form.html'
    # success_url = "/restaurants/"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Add Restaurant'
        return context


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/detail_update.html'
    # success_url = '/restaurants/'
    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     instance.owner = self.request.user
    #     return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(**kwargs)
        name = self.get_object().name
        context['title'] = f'Update Restaurant: {name}'
        return context

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)

