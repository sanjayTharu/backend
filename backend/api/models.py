from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_code = models.CharField(max_length=20, blank=True)
    # activation_sent = models.DateTimeField(blank=True, null=True)
    # is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    # def generate_activation_code(self):
    #     self.activation_code = get_random_string(length=20)

    # def send_activation_email(self):
    #     subject = 'Activate your account'
    #     message = f'Hello {self.user.username},\n\n' \
    #               f'Please activate your account using the following link:\n\n' \
    #               f'{settings.BASE_URL}/activate/{self.activation_code}/'
    #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.user.email])

from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket for {self.movie.title}'
