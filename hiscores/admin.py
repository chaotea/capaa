from django.contrib import admin
from .models import Player

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "wins", "losses", "total", "datetime")

admin.site.register(Player, PlayerAdmin)
