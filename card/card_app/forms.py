from django.forms import ModelForm

from .models import Card


class CardForm(ModelForm):
    """
    Card Model Form
    """

    class Meta:
        model = Card
        fields = ['card_title', 'card_text']
