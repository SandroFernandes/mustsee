from django.contrib import admin
from .models import Attraction, UserRank

class UserRankAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'session_uuid', 'rank')
    list_filter = ('attraction', 'session_uuid')

admin.site.register(Attraction)
admin.site.register(UserRank, UserRankAdmin)

