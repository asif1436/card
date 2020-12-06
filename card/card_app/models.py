from django.db import models


class Card(models.Model):
    """
    Card Model.
    """
    card_title = models.CharField(max_length=100, null=True,
                                  verbose_name="Card Title")
    card_text = models.CharField(max_length=100, null=True,
                                 verbose_name="Card Text")
    card_status = models.BooleanField(default=True)
    card_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        :return: card title.
        """
        return self.card_title
