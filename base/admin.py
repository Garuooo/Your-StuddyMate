from django.contrib import admin

# Register your models here.
# adding you models to the admin panel

from .models import Room , Topic , Message , User

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
