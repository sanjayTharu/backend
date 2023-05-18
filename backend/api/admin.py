from django.contrib import admin
from .models import Movie, Ticket, Customer

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','release_date','created_at','updated_at']
    search_fields = ('title', 'genre')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id','movie','customer','quantity','quantity','price','purchase_date']
    search_fields = ('movie__title', 'customer__user__username')
    list_filter = ('movie', 'customer')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','user')
    search_fields = ('user__username',)
