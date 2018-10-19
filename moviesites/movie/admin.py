from django.contrib import admin

from .models import MInformation, MGenre

# Register your models here.
class MinformationAdmin(admin.ModelAdmin):
	list_display = ['title', 'sorce', 'id', 'img', 'summary']


admin.site.register(MInformation, MinformationAdmin)
admin.site.register(MGenre)