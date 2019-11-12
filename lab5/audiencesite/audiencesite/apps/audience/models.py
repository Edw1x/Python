from django.db import models
from django_enumfield import enum
import json
from datetime import datetime


class User(models.Model):
    user_name = models.CharField("username",max_length=100)
    first_name = models.CharField("First Name", max_length=100)
    last_name = models.CharField("Last Name", max_length=100)
    email = models.CharField("Email", max_length=100)
    password = models.CharField("Password", max_length=100)
    phone = models.CharField("Phone", max_length=100)

class OrderStatus(enum.Enum):
    USING = 1
    CANCELED = 0

    @staticmethod
    def statusToInt(st):
        if st == "canceled":
            return 0
        elif st == "using":
            return 1

    @staticmethod
    def intToStatus(st):
        if st == 0:
            return "canceled"
        elif st == 1:
            return "using"

class AudienceStatus(enum.Enum):
    PENDING = 0
    SOLD = 1
    AVAILABLE = 2

    @staticmethod
    def statusToInt(st):
        if st == "pending":
            return 0
        elif st == "sold":
            return 1
        else:
            return 2

    @staticmethod
    def intToStatus(st):
        if st == 0:
            return "pending"
        elif st == 1:
            return "sold"
        else:
            return "available"




class Audience(models.Model):
    audience_number_of_places = models.IntegerField()
    audience_size_of_scene = models.CharField('Size of the scene', max_length=200)
    audience_ordered_beforehand = models.BooleanField(default=False)
    audience_status = enum.EnumField(AudienceStatus, default=AudienceStatus.AVAILABLE)


class Order(models.Model):
    order_date = models.DateTimeField()
    order_date_end = models.DateTimeField(default=datetime.now, blank=True)
    order_address = models.CharField('Your address', max_length=200)
    order_status = enum.EnumField(OrderStatus, default=OrderStatus.USING)
    audience = models.ForeignKey(Audience,on_delete = models.CASCADE,null=True)
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
