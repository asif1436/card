import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mass_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import CardForm
from .models import Card, OTP, MyUser


def otp_generate(request, user):
    """
    Generate OTP on user authenticated
    :param request:
    :param user:
    :return:
    """
    otp = random.randint(100000, 999999)
    request.session[str(otp)] = user
    return otp


def otp_expiry(request):
    """
    make OTPs inactive which are more then one minute older
    :param request:
    :return:
    """
    active_otp = OTP.objects.filter(
        timestamp__lt=timezone.now() - timezone.timedelta(minutes=1),
        is_active=True)
    for at in active_otp:
        at.is_active = False
        at.save()
    return HttpResponse('OTP Expired')


def user_login(request):
    """
    authenticating user
    :param request:
    :return: student detail page
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            otp = otp_generate(request, email)
            OTP.objects.create(user=user, otp=otp)
            message1 = ('OTP', 'Your OTP: '+str(otp), settings.EMAIL_HOST_USER, [email,])
            send_mass_mail((message1,), fail_silently=False)
            messages.success(request, 'OTP sent to your Email')
            return render(request, 'otp.html', {'otp': otp})
        messages.error(request, 'Email or Password incorrect')
        return HttpResponseRedirect(reverse('login',))

    return render(request, 'login.html')


def verify_user_with_otp(request):
    """
    Verify user with OTP
    :param request:
    :return:
    """
    if request.method == "POST":
        user_enter_otp = request.POST['otp']
        try:
            user_otp = OTP.objects.get(otp=user_enter_otp, is_active=True)
        except ObjectDoesNotExist:
            messages.error(request, "OTP Expired")
            return render(request, 'otp.html')
        else:
            user_email = request.session[str(user_enter_otp)]
            user = MyUser.objects.get(email=user_email)
            login(request, user)
            user_otp.is_active=False
            user_otp.save()
            return HttpResponseRedirect(reverse('card_add',))
    messages.error(request, "OTP Expired")
    return render(request, 'otp.html')


@login_required(login_url='/')
def user_logout(request):
    """
    user get logout
    :param request:
    :return: login_page
    """
    logout(request)
    messages.success(request, 'User Logout Successfully')
    return HttpResponseRedirect('/')


@login_required(login_url='login/')
def card_add(request):
    """
    get all card details and save it
    :param request:
    :return:
    """
    if request.method == "POST":
        card_form = CardForm(request.POST)
        if card_form.is_valid():
            card_form.save()
            return HttpResponseRedirect(reverse('card_view', ))
        else:
            return HttpResponse(card_form.errors)
    card_form = CardForm()
    context = {
        'form': card_form,
    }
    return render(request, 'card_add.html', context)

@login_required(login_url='login/')
def card_view(request):
    """
    Fetch all the data from data base and show
    :param request:
    :return:
    """
    card_data = Card.objects.all().order_by('-id')
    print("##"*20)
    print(card_data)
    print(type(card_data[0]))
    print(type(card_data))
    card_form = CardForm()
    context = {
        'card_data': card_data,
        'card_form': card_form,
    }
    return render(request, 'card_view.html', context)


@login_required(login_url='login/')
def card_delete(request, id=None):
    """
    Fetch the particular data and delete it
    :param request:
    :param id: card id
    :return:
    """
    try:
        card_data = Card.objects.get(id=id)
    except Card.DoesNotExist:
        messages.error(request, "Not valid data", extra_tags='red')
        return redirect(reverse('card_view', ))
    else:
        card_data.delete()
        return redirect(reverse('card_view', ))


@login_required(login_url='login/')
def ajax_call(request):
    """
    Using ajax request save the card details
    :param request:
    :return:
    """
    if request.method == "POST":
        card_form = CardForm(request.POST)
        card_title = request.POST['card_title']
        card_text = request.POST['card_text']
        if not Card.objects.filter(card_title__iexact=card_title,
                                   card_text__iexact=card_text).exists() and card_form.is_valid():
            card_form.save()
            card_data = Card.objects.only('card_title', 'card_text').order_by(
                '-id')
            v = serializers.serialize('json', card_data)
            return HttpResponse(v, content_type="application/json")
        else:
            messages.error(request, "Card Not added")
            return HttpResponse("None")
