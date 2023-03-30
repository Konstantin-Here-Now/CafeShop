from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.conf import settings

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.core.mail import send_mail

from .models import Coffee
from .utils import DefaultValue
from .forms import CoffeeForm, ContactForm, RegistrationForm, LoginForm

from .serializers import CoffeeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from basket.forms import BasketAddProductForm


def index(request):
    return render(request, 'coffee_shop/index.html')


def contact_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['ttemp4376@gmail.com'],
                fail_silently=False
            )
            if mail:
                return redirect('index_page')
    else:
        form = ContactForm()
    return render(request, 'coffee_shop/email.html', {'form': form})


class CoffeeListView(ListView, DefaultValue):
    model = Coffee
    template_name = 'coffee_shop/coffee_list.html'
    context_object_name = 'coffees'

    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.add_title_context(context=context, title_name='Каталог кофе')
        return context

    def get_queryset(self):
        return Coffee.objects.filter(exist=True).order_by('name')


class CoffeeCreateView(CreateView):
    model = Coffee
    form_class = CoffeeForm
    template_name = 'coffee_shop/coffee_add.html'
    context_object_name = 'form'
    success_url = reverse_lazy('coffee_list')

    @method_decorator(permission_required('coffee_shop.add_coffee'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CoffeeDetailView(DetailView):
    model = Coffee
    template_name = 'coffee_shop/coffee_detail.html'
    context_object_name = 'one_coffee'
    pk_url_kwarg = 'coffee_id'

    basket_form = BasketAddProductForm()
    extra_context = {'basket_form': basket_form}


class CoffeeUpdateView(UpdateView):
    model = Coffee
    form_class = CoffeeForm
    template_name = 'coffee_shop/coffee_edit.html'
    context_object_name = 'form'

    @method_decorator(permission_required('coffee_shop.change_coffee'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CoffeeDeleteView(DeleteView):
    model = Coffee
    success_url = reverse_lazy('coffee_list')

    @method_decorator(permission_required('coffee_shop.delete_coffee'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            return redirect('log in')
    else:
        form = RegistrationForm()
    return render(request, 'coffee_shop/auth/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            login(request, user)
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            print(user)
            return redirect('index_page')
    else:
        form = LoginForm()
    return render(request, 'coffee_shop/auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('log in')


@api_view(['GET', 'POST'])
def coffee_api_list(request):
    if request.method == "GET":
        coffee_list = Coffee.objects.all()
        serializer = CoffeeSerializer(coffee_list, many=True)
        return Response({'coffee_list': serializer.data})
    elif request.method == 'POST':
        serializer = CoffeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def coffee_api_detail(request, pk, format=None):
    coffee_obj = get_object_or_404(Coffee, pk=pk)
    if coffee_obj.exist:
        if request.method == 'GET':
            serializer = CoffeeSerializer(coffee_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CoffeeSerializer(coffee_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно изменены', 'coffee': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            coffee_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
