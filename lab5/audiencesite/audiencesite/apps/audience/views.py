from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from .models import Audience, AudienceStatus, User, Order, OrderStatus
from django.http import JsonResponse
import json
import datetime
import dateutil.parser

def check_date_time(date_start1, date_end1, date_start2, date_end2):

    date_start_1 = dateutil.parser.parse(str(date_start1)).date()
    date_end_1 = dateutil.parser.parse(str(date_end1)).date()
    date_start_2 = dateutil.parser.parse(str(date_start2)).date()
    date_end_2 = dateutil.parser.parse(str(date_end2)).date()

    if date_start_1 <= date_start_2 and date_end_2 <= date_end_1:
        return False
    if date_start_1 <= date_start_2 and date_start_2 <= date_end_1:
        return False
    if date_start_1 <= date_end_2 and date_end_2 <= date_end_1:
        return False
    return True

# AUDIENCE_CONTROLL
@csrf_protect
@csrf_exempt
def new_audience(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        number_of_places = json_data['numberOfPlaces']
        size_of_scene = json_data['sizeOfScene']
        ordered_beforehand = json_data['ordered_beforehand']
        status = json_data['status']
        available_status = ["available", "pending(date)", "sold"]
        if status not in available_status:
            return HttpResponseBadRequest()
        Audience.objects.create(audience_number_of_places=number_of_places, audience_size_of_scene=size_of_scene,
                                audience_status=AudienceStatus.statusToInt(status), audience_ordered_beforehand=ordered_beforehand)
    return HttpResponse("New audience has been added")


@csrf_protect
@csrf_exempt
def find_audience_id(request, audience_id):
    if request.method == "GET":
        try:
            audience = Audience.objects.get(id = int(audience_id))
        except:
            raise Http404("audience not found")
        return JsonResponse({"numberOfPlaces": audience.audience_number_of_places,
                             "sizeOfScene": audience.audience_size_of_scene, "status": AudienceStatus.intToStatus(audience.audience_status),
                             "ordered_beforehand": audience.audience_ordered_beforehand})
    return HttpResponse("found")


# YOUR_AUDIENCE
@csrf_protect
@csrf_exempt
def make_order(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        username = json_data['login']
        password = json_data['password']

        try:
            user = User.objects.get(user_name=username)
            if user.password != password:
                return HttpResponse("Your login and password didn't match.")
        except:
            return HttpResponse("Please register firstly")

        audience_id = json_data['AudienceId']
        order_date = json_data['Date']
        order_date_end = json_data['Date_End']
        status = json_data['status']
        available_status = ["using", "canceled"]
        order_address = json_data['address']
        if status not in available_status:
            return HttpResponseBadRequest()

        try:
            audience = Audience.objects.get(id=audience_id)
        except:
            return HttpResponseBadRequest()

        if audience.audience_status == AudienceStatus.SOLD:
            return HttpResponseBadRequest("This audience is already sold, u can order it beforehand")
        elif audience.audience_status == AudienceStatus.AVAILABLE:
            Order.objects.create(audience_id=audience_id, order_date=order_date, order_date_end=order_date_end,
                                 order_status=OrderStatus.statusToInt(status), order_address=order_address, audience=audience, order_user=user)

        audience.audience_status = AudienceStatus.SOLD
        audience.save()

    return HttpResponse("You have bought an audience")

@csrf_protect
@csrf_exempt
def make_order_beforehand(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        username = json_data['login']
        password = json_data['password']

        try:
            user = User.objects.get(user_name=username)
            if user.password != password:
                return HttpResponse("Your login and password didn't match.")
        except:
            return HttpResponse("Please register firstly")

        audience_id = json_data['AudienceId']
        order_date = json_data['Date']
        order_date_end = json_data['Date_End']
        status = json_data['status']
        available_status = ["using", "canceled"]
        order_address = json_data['address']
        if status not in available_status:
            return HttpResponseBadRequest()

        try:
            audience = Audience.objects.get(id=audience_id)
        except:
            return HttpResponseBadRequest()

        try:
            order_list = Order.objects.filter(audience_id=audience_id)
        except:
            return HttpResponseBadRequest()

        if audience.audience_ordered_beforehand is True:
            for i in order_list:
                date_start = i.order_date
                date_end = i.order_date_end

                if check_date_time(date_start, date_end, order_date, order_date_end) is False:
                    return HttpResponseBadRequest("you can not order this audience beforehand, orders are overlaps")
        else:
            audience.audience_ordered_beforehand = True

        Order.objects.create(audience_id=audience_id, order_date=order_date, order_date_end=order_date_end,
                             order_status=OrderStatus.statusToInt(status), order_address=order_address, audience=audience, order_user=user)
        audience.save()
    return HttpResponse("You have ordered an audience beforehand")

@csrf_protect
@csrf_exempt
def find_order_id(request, order_id):
    if request.method == "GET":
        try:
            order = Order.objects.get(id = int(order_id))
        except:
            raise Http404("order not found")
        return JsonResponse({"AudienceId": order.audience_id, "Date": order.order_date, "Date_End": order.order_date_end, "status": OrderStatus.intToStatus(order.order_status), "address": order.order_address})
    return HttpResponse("found")

@csrf_protect
@csrf_exempt
def update_order(request,order_id):
    if request.method == "GET":
        try:
            order = Order.objects.get(id = int(order_id))
        except:
            raise Http404("order not found")

        aud = order.audience_id

        try:
            audience = Audience.objects.get(id=aud)
        except:
            return HttpResponseBadRequest()

    if order.order_status == OrderStatus.USING:
        order.order_status = OrderStatus.CANCELED
        audience.audience_status = AudienceStatus.AVAILABLE
    else:
        order.order_status = OrderStatus.USING
        audience.audience_status = AudienceStatus.SOLD
    order.save()
    audience.save()
    return HttpResponse("status has been changed")

@csrf_protect
@csrf_exempt
def delete_order(request, order_id, audience_id):
    if request.method == "DELETE":
        json_data = json.loads(request.body.decode("utf-8"))
        username = json_data['login']
        password = json_data['password']

        try:
            user = User.objects.get(user_name=username)
            if user.password != password:
                return HttpResponse("Your login and password didn't match.")
        except:
            return HttpResponse("Please register firstly")

        try:
            order = Order.objects.get(id=int(order_id))
        except:
            raise Http404("order not found")

        try:
            audience = Audience.objects.get(id=int(audience_id))
        except:
            raise Http404("order not found")

    if order.audience_id == audience.audience_user_id:
        order.delete()
    else:
        return HttpResponseBadRequest("lol,not your audience")

    audience.audience_status = AudienceStatus.AVAILABLE
    audience.save()
    return HttpResponse("Your order has been deleted")


# USER
@csrf_protect
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        user_name = json_data['username']
        first_name = json_data['firstName']
        last_name = json_data['lastName']
        email = json_data['email']
        password = json_data['password']
        phone = json_data['phone']
        try:
            user = User.objects.get(user_name = user_name)
            return HttpResponseBadRequest()
        except:
            User.objects.create(user_name=user_name, first_name=first_name, last_name=last_name, email=email,
                                password=password, phone=phone)
            return HttpResponse("Successfully created")