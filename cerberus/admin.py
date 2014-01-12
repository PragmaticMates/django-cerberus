from django.contrib import admin
from django.utils.translation import ugettext as _

from models import Lockout


class LockoutAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['ip_address', 'username', 'user_agent', 'failed_attempts', 'get_expiration_time_text',
                    'is_locked', 'is_expired']
    list_filter = ['is_locked', 'is_expired']
    search_fields = ['ip_address', 'username', 'user_agent']
    fieldsets = (
        ('Main data', {
            'fields': ('ip_address', 'username', 'is_locked', 'is_expired', 'failed_attempts')
        }),
        ('Data recollected', {
            #'classes': ('collapse',),
            'fields': ('user_agent', 'params_get', 'params_post')
        }),
    )
    actions = ['lock', 'unlock']

    def lock(self, request, queryset):
        queryset.update(is_locked=True)
    lock.short_description = _(u'Lock users')

    def unlock(self, request, queryset):
        queryset.update(is_locked=False)
    unlock.short_description = _(u'Unlock users')

admin.site.register(Lockout, LockoutAdmin)
