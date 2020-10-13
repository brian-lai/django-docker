from django.contrib import admin
from django.contrib.admin.models import LogEntry

from guardian.models import GroupObjectPermission, UserObjectPermission

from core.models import ResourceStatistics


class ResourceStatsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'date_created', 'date_modified',)


# Guardian model registration
admin.site.register(LogEntry)
admin.site.register(GroupObjectPermission)
admin.site.register(UserObjectPermission)
admin.site.register(ResourceStatistics, ResourceStatsAdmin)
