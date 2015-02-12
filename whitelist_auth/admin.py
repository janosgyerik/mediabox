from django.contrib import admin

from whitelist_auth.models import Whitelisted


class WhitelistedAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'get_last_login', )

admin.site.register(Whitelisted, WhitelistedAdmin)
