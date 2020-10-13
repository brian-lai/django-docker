from guardian.models import GroupObjectPermission, UserObjectPermission

from django.contrib.contenttypes.models import ContentType


def delete_guardian_group_permission(permission, group, instance):
    # Locate all of the permissions associated with the instance
    GroupObjectPermission.objects.filter(
        group=group,
        permission__codename=permission,
        permission__content_type=ContentType.objects.get_for_model(instance),
        object_pk=instance.pk,
        content_type=ContentType.objects.get_for_model(instance)
    ).delete()


def delete_guardian_models(instance, groups=True, users=True):
    # Locate all of the permissions associated with the instance
    content_type = ContentType.objects.get_for_model(instance)
    kwargs = {'object_pk': instance.pk, 'content_type': content_type}
    if groups:
        GroupObjectPermission.objects.filter(**kwargs).delete()
    if users:
        UserObjectPermission.objects.filter(**kwargs).delete()
