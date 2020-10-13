from django.contrib.contenttypes.models import ContentType

from guardian.models import GroupObjectPermission, UserObjectPermission
from guardian.shortcuts import get_objects_for_group, get_objects_for_user

from core.models import ResourceStatistics
from core.roles import GenePeeksStaff


def _assign_permission(permission_codename, instance, user=None, group=None):
    '''Attempts to assign a `Permission` to a given model instance.

    Raises:
        Permissions.DoesNotExist:
            Cause: Permission codename is invalid. We used to catch this
            and pass, but in reality, this implies the server is in a bad
            state probably and we would want a 500 email to be sent.
    '''
    if user is not None:
        UserObjectPermission.objects.assign_perm(permission_codename, user, instance)

    if group is not None:
        GroupObjectPermission.objects.assign_perm(permission_codename, group, instance)


def assign_creator(instance, user):
    resource, created = ResourceStatistics.objects.get_or_create(
        resource_content_type=ContentType.objects.get_for_model(instance),
        resource_object_id=instance.id,
        defaults={
            'created_by': user
        }
    )
    return (user, created)


def assign_owner(instance, group, user=None):
    '''Attributes the 'owner' guardian permission to a given model instance.
    '''
    return _assign_permission('owner', instance, group=group, user=user)


def guard_filter(queryset, group=None, user=None):
    # Check if we are getting objects for a group
    if group is not None:
        return get_objects_for_group(group, 'owner', klass=queryset)

    # Check if we are getting object for a user
    if user is not None and GenePeeksStaff.check_membership(user) is False:
        return get_objects_for_user(user, 'owner', klass=queryset)

    return queryset
