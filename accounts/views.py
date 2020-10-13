from django.shortcuts import render
import os.path
from django_tables2 import SingleTableView
from django.conf import settings
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic
from accounts.models import Organization
from .tables import OrganizationTable

# Create your views here.


def index(request):
    return HttpResponse("Hello, world.")


class OrganizationListView(SingleTableView):
    '''`Organizations` list view.
    '''
    model = Organization
    queryset = Organization.objects.all()
    table_class = OrganizationTable
    template_name = 'accounts/organization_list.html'
    # filterset_class = FamilyFilter
    # paginate_by = 25
    # permission_required = ('clinical.view_family', )
    # table_pagination = {'per_page': paginate_by}

    # export_filename = 'families'
    # export_template_name = 'genepeeks/components/table.tsv'
    # staff_role = GenePeeksStaff
    # staff_only_fields = ('members', 'date_of_birth', )

    # return HttpResponse("Hello, world. You're at the polls fuck that.")

    def get_table_data(self):
        return self.object_list

# class OrganizationCreateView(HostLoginRequiredMixin, RoleRequiredMixin, AtomicTransactionMixin, generic.CreateView):
#     '''Onboarding view for all base `Organizations` in the system.
#     '''
#     model = Organization
#     form_class = OrganizationCreateForm
#     role_required = (Admin, GenePeeksStaff)
#     template_name = 'accounts/organization_create.html'

