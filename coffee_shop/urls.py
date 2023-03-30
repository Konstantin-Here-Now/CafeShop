from django.urls import path

from coffee_shop.views import *

urlpatterns = [
    path('', index, name='index_page'),

    path('list/', CoffeeListView.as_view(), name='coffee_list'),
    path('add/', CoffeeCreateView.as_view(), name='coffee_add'),
    path('list/<int:coffee_id>/', CoffeeDetailView.as_view(), name='coffee_info'),
    path('edit/<int:pk>/', CoffeeUpdateView.as_view(), name='coffee_edit'),
    path('del/<int:pk>/', CoffeeDeleteView.as_view(), name='coffee_del'),

    path('email/', contact_email, name='contact_email'),

    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),

    path('api/list/', coffee_api_list, name='coffee_api_list'),
    path('api/detail/<int:pk>', coffee_api_detail, name='coffee_api_detail'),
]
