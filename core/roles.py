"""Uses django-hats to configure roles and permissions for the application."""
from django_hats import roles


class Admin(roles.Role):
    class Meta:
        permissions = (
            # User Permissions
            'add_user',
            'change_user',
            'delete_user',
            # Group Permissions
            'add_group',
            'change_group',
            'delete_group',
        )


class Developer(roles.Role):
    class Meta:
        permissions = (
            'view_workflow',
        )


class SaasUser(roles.Role):
    class Meta:
        permissions = (
            # Analysis
            # Analysis Permissions
            'add_analysis',
            'change_analysis',
            'view_analysis',

            # Clinical
            # Family Permissions
            'add_family',
            'change_family',
            'view_family',

            #  Consent
            # Consent Permissions
            'add_consent',
            'change_consent',
            'delete_consent',
            'view_consent',

            # Operations
            # Specimen Permissions
            'add_specimen',
            'change_specimen',
            'view_specimen',

            # Subject Permissions
            'add_subject',
            'change_subject',
            'view_subject',
            'subject_genetic_information',
            'subject_personal_information',
        )


class WebsiteUser(roles.Role):
    pass


class GenePeeksStaff(roles.Role):
    class Meta:
        permissions = (
            # Analysis Permissions
            'add_analysis',
            'change_analysis',
            'delete_analysis',
            'view_analysis',

            # Operations
            # Subject Permissions
            'add_subject',
            'change_subject',
            'view_subject',
            'subject_genetic_information',
            'subject_personal_information',
            # Specimen Permissions
            'add_specimen',
            'change_specimen',
            'view_specimen',
            # Sample Permissions
            'add_sample',
            'change_sample',
            'delete_sample',
            'view_sample',
            # Kit Permissions
            'add_kit',
            'change_kit',
            'delete_kit',
            'view_kit',
            # Cohort Permissions
            'add_cohort',
            'change_cohort',
            'delete_cohort',
            'view_cohort',
            # Run Permissions
            'add_run',
            'change_run',
            'delete_run',
            'view_run',
            # Package Permissions
            'add_package',
            'change_package',
            'view_package',
            # Panel Permissions
            'view_panel',

            # Clinical
            # Client Match Permissions
            'add_clientmatch',
            'change_clientmatch',
            'delete_clientmatch',
            # Family Permissions
            'add_family',
            'change_family',
            'delete_family',
            'view_family',
            # Condition Permissions
            'add_condition',
            'change_condition',
            'delete_condition',
            # Screen Permissions
            'add_screen',
            'change_screen',
            'delete_screen',
            'view_screen',
            'view_report',

            #  Consent
            # Consent Permissions
            'add_consent',
            'change_consent',
            'delete_consent',
            'view_consent',
            # ElectronicSignature Permissions
            'add_electronicsignature',
            'change_electronicsignature',
            'delete_electronicsignature',
            'view_electronicsignature',
            # Assay Permissions
            'view_assay',
            # AssayRun Permissions
            'add_assayrun',
            'change_assayrun',
            'delete_assayrun',
            'view_assayrun',
            # Reagent Permissions
            'view_reagent',
            'add_reagentkit',
            'change_reagentkit',
            'delete_reagentkit',
            'view_reagentkit',
        )


class ClinicStaff(roles.Role):
    class Meta:
        permissions = (
            # Operations
            # Subject Permissions
            'add_subject',
            'change_subject',
            'delete_subject',
            'view_subject',
            # Specimen Permissions
            'add_specimen',
            'change_specimen',
            'delete_specimen',
            'view_specimen',
            # Package Permissions
            'add_package',
            'change_package',
            'delete_package',
            'view_package',

            # Clinical
            # Client Permissions
            'add_client',
            'change_client',
            'view_client',
            'client_final_report',
            # Client Match Permissions
            'add_clientmatch',
            'change_clientmatch',
            'delete_clientmatch',
            # Condition Permissions
            'add_condition',
            'change_condition',
            'delete_condition',
            # Family Permissions
            'add_family',
            'change_family',
            'delete_family',
            'view_family',
            # Screen permissions
            'add_screen',
            'change_screen',
            'delete_screen',
            'view_screen',
            'authorize_screen',

            # Consent
            # Consent Permissions
            'add_consent',
            'change_consent',
            'delete_consent',
            'view_consent',
            # ElectronicSignature Permissions
            'add_electronicsignature',
            'change_electronicsignature',
            'delete_electronicsignature',
            'view_electronicsignature',
            # Assay Permissions
            'view_assay',
            'add_assayrun',
            'change_assayrun',
            'delete_assayrun',
            'view_assayrun',
            # Reagent Permissions
            'view_reagent',
            'add_reagentkit',
            'change_reagentkit',
            'delete_reagentkit',
            'view_reagentkit',
        )


class Clinician(roles.Role):
    class Meta:
        permissions = ClinicStaff.Meta.permissions + (
            # Clinical
            # Disease Permissions
            'add_disease',
            'change_disease',
            'delete_disease',
            # GIST
            # Subject Permissions
            'subject_genetic_information',
            'subject_personal_information',
        )


class AuthorizingOfficer(roles.Role):
    class Meta:
        permissions = (
            # Screen permissions
            'add_screen',
            'change_screen',
            'delete_screen',
            'view_screen',
            'authorize_screen',
            # Family Permissions
            'add_family',
            'change_family',
            'delete_family',
            'view_family'
        )


class Scientist(roles.Role):
    class Meta:
        permissions = (
            # Client Permissions
            'view_client',
            # Subject Permissions
            'add_subject',
            'change_subject',
            'view_subject',
            'subject_genetic_information',
            # Consent Permissions
            'add_consent',
            'change_consent',
            'delete_consent',
            'view_consent',
            # Specimen Permissions
            'add_specimen',
            'change_specimen',
            'delete_specimen',
            'view_specimen',
            # Sample Permissions
            'add_sample',
            'change_sample',
            'delete_sample',
            'view_sample',
            # Run Permissions
            'add_run',
            'change_run',
            'delete_run',
            'view_run',
            # Assay Permissions
            'view_assay'
            'add_assayrun',
            'change_assayrun',
            'delete_assayrun',
            'view_assayrun',
            # Reagent Permissions
            'view_reagent',
            'add_reagentkit',
            'change_reagentkit',
            'delete_reagentkit',
            'view_reagentkit',
        )


class GeneticCounselor(roles.Role):
    class Meta:
        permissions = (
            # Client Permissions
            'add_client',
            'change_client',
            'view_client',
            'client_final_report',
            # Subject Permissions
            'add_subject',
            'change_subject',
            'view_subject',
            # Consent Permissions
            'add_consent',
            'change_consent',
            'delete_consent',
            'view_consent',
            # Specimen Permissions
            'add_specimen',
            'change_specimen',
            'delete_specimen',
            'view_specimen',
            # Sample Permissions
            'add_sample',
            'change_sample',
            'delete_sample',
            'view_sample',
            # Run Permissions
            'add_run',
            'change_run',
            'delete_run',
            'view_run',
            # Specimen Permissions
            'subject_genetic_information',
            'subject_personal_information',
            # Assay Permissions
            'view_assay',
            'add_assayrun',
            'change_assayrun',
            'delete_assayrun',
            'view_assayrun',
            # Reagent Permissions
            'view_reagent',
            'add_reagentkit',
            'change_reagentkit',
            'delete_reagentkit',
            'view_reagentkit',
        )


class CustomerService(roles.Role):
    class Meta:
        permissions = (
            # Client Permissions
            'add_client',
            'change_client',
            'delete_client',
            'view_client',
            'client_stripe_information',
            # Client Match Permissions
            'add_clientmatch',
            'change_clientmatch',
            'delete_clientmatch',
            # Condition Permissions
            'add_condition',
            'change_condition',
            'delete_condition',
        )


class LabStaff(roles.Role):
    class Meta:
        permissions = (
            # Package Permissions
            'add_package',
            'change_package',
            'delete_package',
            'view_package',
            # Specimen Permissions
            'add_specimen',
            'change_specimen',
            'delete_specimen',
            'view_specimen',
            # Sample Permissions
            'add_sample',
            'change_sample',
            'delete_sample',
            'view_sample',
            # Subject Permission
            'add_subject',
            'change_subject',
            'view_subject',
            # Run Permissions
            'add_run',
            'edit_run',
            'delete_run',
            'view_run',
            # Assay Permissions
            'view_assay',
            # AssayRun Permissions
            'add_assayrun',
            'change_assayrun',
            'delete_assayrun',
            'view_assayrun',
            # Reagent Permissions
            'view_reagent',
            'add_reagentkit',
            'change_reagentkit',
            'delete_reagentkit',
            'view_reagentkit',
            # Consent Permissions
            'add_consent',
            'change_consent',
            'delete_consent',
            'view_consent',
        )


class BankStaff(roles.Role):
    class Meta:
        permissions = (
            # EggDonor Permissions
            'add_eggdonor',
            'change_eggdonor',
            'delete_eggdonor',
            'view_eggdonor',
            # ImageResource Permissions
            'add_imageresource',
            'change_imageresource',
            'delete_imageresource',
            # Package Permissions
            'add_package',
            'change_package',
            'delete_package',
            'view_package',
            # Specimen Permissions
            'add_specimen',
            'change_specimen',
            'delete_specimen',
            'view_specimen',
            # SpermDonor Permissions
            'add_spermdonor',
            'change_spermdonor',
            'delete_spermdonor',
            'view_spermdonor',
            # Subject Permissions
            'add_subject',
            'change_subject',
            'delete_subject',
            'view_subject',
            'subject_personal_information',
            # Assay Permissions
            'view_assay',
            'add_assayrun',
            'change_assayrun',
            'delete_assayrun',
            'view_assayrun',
            # Reagent Permissions
            'view_reagent',
            'add_reagentkit',
            'change_reagentkit',
            'delete_reagentkit',
            'view_reagentkit',
            # Consent Permissions
            'add_consent',
            'change_consent',
            'delete_consent',
            'view_consent',
        )


class ResearchStaff(roles.Role):
    class Meta:
        permissions = (
            # Subject Permissions
            'add_subject',
            'change_subject',
            'view_subject',
            # Consent Permissions
            'add_consent',
            'change_consent',
            'delete_consent',
            'view_consent',
            # Specimen Permissions
            'add_specimen',
            'change_specimen',
            'delete_specimen',
            'view_specimen',
            # Sample Permissions
            'add_sample',
            'change_sample',
            'delete_sample',
            'view_sample',
            # Assay Permissions
            'view_assay',
            'add_assayrun',
            'change_assayrun',
            'view_assayrun',
            # Reagent Permissions
            'view_reagent',
            'add_reagentkit',
            'change_reagentkit',
            'view_reagentkit',
        )
