from django.contrib import admin
from .models import UserPasswords, UserNotes, UserCards, UsersEncryptionKey, CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(UserPasswords)
admin.site.register(UsersEncryptionKey)
admin.site.register(UserNotes)
admin.site.register(UserCards)
# Register your models here.


