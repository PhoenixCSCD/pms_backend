import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from graphene_django.types import DjangoObjectType

from authentication.models import User
from .models import Branch


class BranchType(DjangoObjectType):
    class Meta:
        model = Branch


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission


class AddGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        permissions = graphene.List(graphene.Int)

    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, name, permissions):
        group = Group()
        group.name = name
        group.save()
        group.permissions.set(permissions)
        return AddGroup(group=group)


class EditGroup(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        permissions = graphene.List(graphene.Int)

    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, id, name, permissions):
        group = Group.objects.get(id=id)
        print("Ken here --> ", name)
        group.name = name
        group.permissions.set(permissions)
        group.save()
        return EditGroup(group=group)


class DeleteGroup(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, id):
        Group.objects.get(id=id).delete()
        return DeleteGroup(group=None)


class DeleteGroups(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.Int)

    groups = graphene.List(GroupType)

    @staticmethod
    def mutate(root, info, ids):
        Group.objects.filter(id__in=ids).delete()
        return DeleteGroups(groups=None)


class AddUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        gender = graphene.String()
        date_of_birth = graphene.Date()
        phone_number = graphene.String()
        groups = graphene.List(graphene.Int)
        avatar = graphene.String()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, first_name, last_name, email, gender, date_of_birth, phone_number, groups, avatar):
        user = get_user_model()()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.gender = gender
        user.date_of_birth = date_of_birth
        user.phone_number = phone_number
        user.avatar = avatar
        user.set_unusable_password()
        user.is_staff = True
        user.save()
        user.groups.add(*groups)
        return AddUser(user=user)


class AddBranch(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    branch = graphene.Field(BranchType)

    @staticmethod
    def mutate(root, info, name):
        branch = Branch()
        branch.name = name
        branch.save()
        return AddBranch(branch=branch)


class AddUserBranchesMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID()
        branches = graphene.List(graphene.UUID)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_id, branches):
        user = User.objects.get(id=user_id)
        user.branches.update(branches)
        user.save()
        return AddUserBranchesMutation(user=user)


class Mutation(graphene.ObjectType):
    # Groups
    add_group = AddGroup.Field()
    edit_group = EditGroup.Field()
    delete_group = DeleteGroup.Field()
    delete_groups = DeleteGroups.Field()

    add_user = AddUser.Field()
    add_branch = AddBranch.Field()
    add_user_branches = AddUserBranchesMutation.Field()


class Query(graphene.ObjectType):
    # User
    users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.UUID())
    user_by_email = graphene.Field(UserType, email=graphene.String())
    # Group
    groups = graphene.List(GroupType)
    group_by_id = graphene.Field(GroupType, id=graphene.Int())

    # Permissions
    permissions = graphene.List(PermissionType)

    # Branch
    branches = graphene.List(BranchType)

    @staticmethod
    def resolve_groups(root, info):
        return Group.objects.all()

    @staticmethod
    def resolve_group_by_id(root, info, id):
        return Group.objects.get(id=id)

    @staticmethod
    def resolve_permissions(root, info):
        return Permission.objects.all()

    @staticmethod
    def resolve_users(root, info):
        return User.objects.all()

    @staticmethod
    def resolve_user_by_id(root, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def resolve_branches(root, info):
        return Branch.objects.all()

    @staticmethod
    def resolve_user_by_email(root, info, email):
        try:
            return get_user_model().objects.get(email=email)
        except User.DoesNotExist:
            return None
