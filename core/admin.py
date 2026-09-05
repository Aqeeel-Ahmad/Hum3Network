from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

admin.site.register(Feedback, FeedbackAdmin)
