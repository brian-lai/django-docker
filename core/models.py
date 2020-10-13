from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from guardian.models import GroupObjectPermission, UserObjectPermission

from core.utils.display import get_datetime_display


class ResourceStatisticsManager(models.Manager):
    def get_for_resource(self, resource):
        stats, _ = super(ResourceStatisticsManager, self).get_queryset().get_or_create(
            resource_content_type=ContentType.objects.get_for_model(resource),
            resource_object_id=resource.id
        )
        return stats


class ResourceStatistics(models.Model):
    class Meta:
        unique_together = (('resource_content_type', 'resource_object_id'), )
    # Custom manager for easy lookup
    objects = ResourceStatisticsManager()

    # What is this CostCenter being attributed towards
    resource_content_type = models.ForeignKey(ContentType)
    resource_object_id = models.PositiveIntegerField()
    resource = GenericForeignKey('resource_content_type', 'resource_object_id')

    # DateTime resounce was created
    date_created = models.DateTimeField(db_index=True, auto_now_add=True, editable=False)

    # DateTime resource was last changed
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    # User we triggered creation of the resource
    created_by = models.ForeignKey(User, null=True, editable=False)

    def get_date_created_display(self):
        return get_datetime_display(self.date_created)

    def __unicode__(self):
        return '%s %s' % (unicode(self.resource_content_type).title(), unicode(self.resource))


class VisualModel(object):
    # DO NOT REMOVE UNTIL MIGRATION SQUASH HAPPENS
    # This code is kept to maintain backwards compatability
    pass


class ManagedModel(models.Model):
    class Meta:
        abstract = True
        permissions = (
            ('owner', 'Grants full access'),
        )
        default_permissions = ('add', 'change', 'delete', 'view')

    statistics = GenericRelation(
        ResourceStatistics,
        related_query_name='statistics',
        content_type_field='resource_content_type',
        object_id_field='resource_object_id'
    )

    def date_created(self):
        return self.get_statistics().date_created
    date_created.short_description = 'Date created'

    def get_statistics(self):
        '''Attempts to get the potentially prefetched ResourceStatistics.

        Provides a fallback with a get_or_create since this object should always exist.
        '''
        try:
            return self.statistics.all()[0]
        except IndexError:
            pass
        return ResourceStatistics.objects.get_for_resource(self)

    # Returns a list of groups which can access this resource
    def get_groups_access(self, **kwargs):
        kwargs.update({
            'object_pk': self.pk,
            'content_type': ContentType.objects.get_for_model(self)
        })

        # Perform the query
        return Group.objects.filter(
            id__in=GroupObjectPermission.objects.filter(
                **kwargs
            ).values_list('group_id', flat=True)
        )

    # Returns a list of groups which have explicit access to this resource
    # TODO: Does users list need to include those who have access through a group, or just explicit user access?
    def get_users_access(self):
        # Perform the query
        return User.objects.filter(
            id__in=UserObjectPermission.objects.filter(
                object_pk=self.pk,
                content_type=ContentType.objects.get_for_model(self)
            ).values_list('user_id', flat=True)
        )

    @property
    def creator(self):
        return self.get_statistics().created_by

    def get_creator_display(self):
        creator = self.creator
        if creator is not None:
            return creator.get_full_name()
        return 'SYSTEM'
