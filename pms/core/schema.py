import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from graphene_django.types import DjangoObjectType

from pms.core.models import User, Allergy
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


class AllergyType(DjangoObjectType):
    class Meta:
        model = Allergy


class AddGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        permissions = graphene.List(graphene.Int)

    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(_root, _info, name, permissions):
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
    def mutate(_root, _info, group_id, name, permissions):
        group = Group.objects.get(id=group_id)
        group.name = name
        group.permissions.set(permissions)
        group.save()
        return EditGroup(group=group)


class DeleteGroup(graphene.Mutation):
    class Arguments:
        group_id = graphene.Int()

    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(_root, _info, group_id):
        Group.objects.get(id=group_id).delete()
        return DeleteGroup(group=None)


class DeleteGroups(graphene.Mutation):
    class Arguments:
        group_ids = graphene.List(graphene.Int)

    groups = graphene.List(GroupType)

    @staticmethod
    def mutate(_root, _info, group_ids):
        Group.objects.filter(id__in=group_ids).delete()
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
    def mutate(_root, _info, first_name, last_name, email, gender, date_of_birth, phone_number, groups, avatar):
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
    def mutate(_root, _info, name):
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
    def mutate(_root, _info, user_id, branches):
        user = User.objects.get(id=user_id)
        user.branches.update(branches)
        user.save()
        return AddUserBranchesMutation(user=user)


class AddAllergy(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    allergy = graphene.Field(AllergyType)

    @staticmethod
    def mutate(_root, _info, name):
        allergy = Allergy()
        allergy.name = name
        allergy.save()
        return AddAllergy(allergy= allergy)


class Mutation(graphene.ObjectType):
    # Groups
    add_group = AddGroup.Field()
    edit_group = EditGroup.Field()
    delete_group = DeleteGroup.Field()
    delete_groups = DeleteGroups.Field()

    add_user = AddUser.Field()
    add_branch = AddBranch.Field()
    add_user_branches = AddUserBranchesMutation.Field()

    add_allergy = AddAllergy.Field()


class Query(graphene.ObjectType):
    # User
    users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, user_id=graphene.UUID())
    user_by_email = graphene.Field(UserType, email=graphene.String())
    # Group
    groups = graphene.List(GroupType)
    group_by_id = graphene.Field(GroupType, group_id=graphene.Int())

    # Permissions
    permissions = graphene.List(PermissionType)

    # Branch
    branches = graphene.List(BranchType)

    # Allergy
    allergies = graphene.List(AllergyType)

    @staticmethod
    def resolve_allergies(_root, _info):
        return Allergy.objects.all()

    @staticmethod
    def resolve_groups(_root, _info):
        return Group.objects.all()

    @staticmethod
    def resolve_group_by_id(_root, _info, group_id):
        return Group.objects.get(id=group_id)

    @staticmethod
    def resolve_permissions(_root, _info):
        return Permission.objects.all()

    @staticmethod
    def resolve_users(_root, _info):
        return User.objects.all()

    @staticmethod
    def resolve_user_by_id(_root, _info, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def resolve_branches(_root, _info):
        return Branch.objects.all()

    @staticmethod
    def resolve_user_by_email(_root, _info, email):
        try:
            return get_user_model().objects.get(email=email)
        except User.DoesNotExist:
            return None
