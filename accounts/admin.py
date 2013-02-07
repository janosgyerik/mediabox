from django.contrib import admin

from accounts.models import Whitelisted

class WhitelistedAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')


admin.site.register(Whitelisted, WhitelistedAdmin)

# eof
