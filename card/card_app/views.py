from django.contrib import messages
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CardForm
from .models import Card


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


def card_view(request):
    """
    Fetch all the data from data base and show
    :param request:
    :return:
    """
    card_data = Card.objects.all().order_by('-id')
    card_form = CardForm()
    context = {
        'card_data': card_data,
        'card_form': card_form,
    }
    return render(request, 'card_view.html', context)


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
