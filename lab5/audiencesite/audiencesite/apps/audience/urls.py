from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_audience, name='new_audience'),
    path('order/', views.make_order, name='make_order'),
    path('orderBeforehand/', views.make_order_beforehand, name='make_order_beforehand'),
    path('find/<audience_id>/', views.find_audience_id, name='find_audience_id'),
    path('get/<order_id>/', views.find_order_id, name='find_order_id'),
    path('del/<order_id>/<audience_id>/', views.delete_order, name='delete_order'),
    path('change/<order_id>/', views.update_order, name='update_order'),
    path('register/', views.register_user, name='register_user'),
]