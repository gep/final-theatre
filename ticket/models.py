from django.db import models
from django.utils.datetime_safe import date, datetime
from registration.models import User


class Play(models.Model):
    genre = models.CharField(max_length=255, verbose_name='Genre')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField('date published')
    author = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class PlayProduction(models.Model):
    play = models.ForeignKey(Play)
    date = models.DateField(unique=True, verbose_name='Date')

    def __unicode__(self):
        return self.date.strftime('%m-%d')

    @property
    def is_past_due(self):
        return date.today() > self.date


class SeatCategory(models.Model):
    price = models.IntegerField()
    name = models.CharField(max_length=255)
    max_seats = models.IntegerField(default=100)

    def __unicode__(self):
        return self.name


class Ticket(models.Model):
    production = models.ForeignKey(PlayProduction)
    category = models.ForeignKey(SeatCategory)
    number = models.IntegerField()
    user = models.ForeignKey(User)
    is_bought = models.BooleanField(default=False)
    created_at = models.DateTimeField('date ordered', default=datetime.today())

    class Meta:
        unique_together = ('category', 'production', 'number', 'user')

    def __unicode__(self):
        return '%d - %s' % (self.number, self.user.username)