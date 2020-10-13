from django_tables2 import columns
import django_tables2 as tables
from django_tables2.utils import A

from core.utils import columns as core_columns
from .models import Organization


class OrganizationTable(tables.Table):
    # name = columns.LinkColumn('oragnization-detail', kwargs={'pk': A('id')}, verbose_name='Organization Name')
    date_created = core_columns.ResourceStatisticsColumn(attr='date_created')
    # screens = columns.TemplateColumn(
    #     template_name='clinical/columns/family_screens_column.html',
    #     verbose_name='Screens',
    #     orderable=False
    # )
    # analyses = columns.TemplateColumn(
    #     template_name='clinical/columns/family_analyses_column.html',
    #     verbose_name='Analyses',
    #     orderable=False
    # )
    # subjects = columns.TemplateColumn(
    #     template_name='clinical/columns/family_subjects_column.html',
    #     verbose_name='Subjects',
    #     orderable=False
    # )
    # members = columns.TemplateColumn(
    #     template_name='clinical/columns/family_members_column.html',
    #     verbose_name='Account Users',
    #     orderable=False
    # )

    class Meta:
        model = Organization
        template_name = "django_tables2/bootstrap.html"
        fields = ('name', 'slug', 'description', 'date_created', )