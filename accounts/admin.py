from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'whatsapp_number', 'outstanding_balance', 'raw_password', 'avatar_preview')
    list_editable = ('outstanding_balance',)
    search_fields = ('user__username', 'phone_number', 'user__first_name', 'user__last_name')
    readonly_fields = ('avatar_preview', 'raw_password')

    def avatar_preview(self, obj):
        if obj.avatar:
            return f'Uploaded: {obj.avatar.name}'
        return 'No Avatar'
    avatar_preview.short_description = 'Avatar'

admin.site.register(UserProfile, UserProfileAdmin)
