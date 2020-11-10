from django.contrib import admin

from .models import User, Category, Listing, Bid, Comment, Watch 
# Register your models here.
class WatchAdmin(admin.ModelAdmin):
    list_display = ("id","user","listing")

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watch, WatchAdmin)