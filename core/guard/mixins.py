"""Mixins used to enforce permissions."""
from django.contrib.auth.models import Group, User

from core.guard.shortcuts import assign_creator, assign_owner, guard_filter
from core.guard.utils import delete_guardian_models


class GuardBaseCreateMixin(object):
    '''Facilitates requiring the definition of the `Group` receiving permission on creation.
    '''
    instance_owners = ()

    def get_instances(self, **kwargs):
        '''Returns the instances that the permissions should be assigned.
        '''
        raise NotImplementedError('%s must implement `get_instances()`' % self.__class__.__name__)

    def get_instance_owners(self, instance):
        '''Returns a list of the `Group`/`User` instances which should have access to this resource.
        '''
        attributes = self.instance_owners
        if isinstance(attributes, str) is True:
            attributes = [attributes, ]

        # Aggregate all the `Groups`/`Users
        owners = []
        for attr in attributes:
            owner = getattr(instance, attr, None)

            # Catch `None` case
            if owner is None:
                raise ValueError('Cannot assign permissions to a non-existant `%s` for `%s`' % (type(owner), attr))
            owners.append(owner)

        return owners

    def assign_permissions(self, instances, created=True):
        '''Assigns guardian permissions to all necessary parties.

        Work primarily off of the `get_instances()` hook, which allows a mixin
        to declare which instances will be given access to a `User`/`Group`.
        '''
        for instance in instances:
            # Determine if a creator should be assigned
            if created:
                assign_creator(instance=instance, user=self.request.user)

            # Iterate over the owners and give access to the instance
            owners = self.get_instance_owners(instance)
            for owner in owners:
                kwargs = {
                    'group': owner if isinstance(owner, Group) else None,
                    'user': owner if isinstance(owner, User) else None
                }
                assign_owner(instance=instance, **kwargs)


class GuardCreateMixin(GuardBaseCreateMixin):
    '''For a given 'create' view, assign ownership and creator tracking to the given resources.
    '''
    def get_instances(self, form):
        return [form.instance, ]

    def form_valid(self, form):
        ret = super(GuardCreateMixin, self).form_valid(form)
        self.assign_permissions(self.get_instances(form=form))
        return ret


class GuardUpdateReplaceMixin(GuardBaseCreateMixin):
    '''Replaces all existing `Group` permissions for an instance on update.
    '''
    def get_instances(self, form):
        return [form.instance, ]

    def form_valid(self, form):
        ret = super(GuardCreateMixin, self).form_valid(form)
        instances = self.get_instances(form=form)

        # Clear existing owners first
        for instance in instances:
            delete_guardian_models(instance, users=False)

        self.assign_permissions(instances, created=False)
        return ret


class GuardAPICreateMixin(GuardBaseCreateMixin):
    '''For a given API 'create' view, assign ownership and creator tracking to the given resources.
    '''
    def get_instances(self, serializer):
        return [serializer.instance, ]

    def perform_create(self, serializer):
        # Call the super
        ret = super(GuardAPICreateMixin, self).perform_create(serializer)

        # Assign guardian permissions
        self.assign_permissions(self.get_instances(serializer=serializer))

        return ret


class GuardQuerysetMixin(object):
    '''Filters a given queryset for a view based on the `User`/`Group` permissions assigned per-resource.
    '''
    def get_queryset(self):
        return guard_filter(super(GuardQuerysetMixin, self).get_queryset(), user=self.request.user)
