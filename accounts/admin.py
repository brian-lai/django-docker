from django.contrib import admin

# Register your models here.


from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    # inlines = (AnalysisSubjectInline, AnalysisRunInline)
    search_fields = ('name')
    list_display = (
        'name', 'slug', 'description'
    )
    list_filter = ('name')


admin.site.register(Organization)