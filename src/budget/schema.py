from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
import graphene

from .models import Budget, BudgetEntryCategory, BudgetEntry


class BudgetType(DjangoObjectType):
    class Meta:
        model = Budget


class BudgetEntryCategoryType(DjangoObjectType):
    class Meta:
        model = BudgetEntryCategory


class BudgetEntryType(DjangoObjectType):
    class Meta:
        model = BudgetEntry


class Query(graphene.ObjectType):
    # TODO: add pagination https://graphql.org/learn/pagination/
    # TODO: add endpoints for fetching single object by id
    # TODO: rename endpoints to something like 'budgets' for lists 
    #       and 'budget' for single object
    all_budgets = graphene.List(BudgetType)
    all_shared_budgets = graphene.List(BudgetType)
    all_budget_entry_categories = graphene.List(BudgetEntryCategoryType)

    budget_total = graphene.Decimal(budget_id=graphene.ID(required=True))

    def resolve_budget_total(self, info, budget_id):
        try:
            budget = Budget.objects.get(pk=budget_id)
        except Budget.DoesNotExist:
            return None

        # TODO: Move checking permissions to buissnes logic
        user = info.context.user
        if budget.owner != user and not budget.shared_with_users.filter(pk=user.pk).exists():
            return None

        return budget.total()

    def resolve_all_budgets(self, info):
        user = info.context.user
        return Budget.objects.filter(owner=user)

    def resolve_all_shared_budgets(self, info):
        user = info.context.user
        return user.budget_set.all()

    def resolve_all_budget_entry_categories(self, info):
        return BudgetEntryCategory.objects.all()


class CreateBudget(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        shared_with_users = graphene.List(graphene.ID)

    budget = graphene.Field(BudgetType)

    def mutate(self, info, name, shared_with_users=None):
        user = info.context.user

        budget = Budget.objects.create(
            name=name,
            owner=user,
        )

        if shared_with_users is not None:
            shared_with_users_set = []
            for user_id in shared_with_users:
                user_object = User.objects.get(pk=user_id)
                shared_with_users_set.append(user_object)
            budget.shared_with_users.set(shared_with_users_set)

        budget.save()

        return CreateBudget(
            budget=budget
        )


class UpdateBudget(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        shared_with_users = graphene.List(graphene.ID)

    budget = graphene.Field(BudgetType)

    def mutate(self, info, id, name=None, shared_with_users=None):
        try:
            budget = Budget.objects.get(pk=id)
        except Budget.DoesNotExist:
            return None

        user = info.context.user
        if budget.owner != user:
            return None

        budget.name = name if name is not None else budget.name

        if shared_with_users is not None:
            shared_with_users_set = []
            for user_id in shared_with_users:
                user_object = User.objects.get(pk=user_id)
                shared_with_users_set.append(user_object)
            budget.shared_with_users.set(shared_with_users_set)

        budget.save()

        return UpdateBudget(
            budget=budget
        )


class DeleteBudget(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    budget = graphene.Field(BudgetType)

    def mutate(self, info, id):
        try:
            budget = Budget.objects.get(pk=id)
        except Budget.DoesNotExist:
            return None

        user = info.context.user
        if budget.owner != user:
            return None

        budget.delete()

        return DeleteBudget(budget=budget)


class Mutation(graphene.ObjectType):
    # TODO: create CRUD for budget entry
    # TODO: create mutation 'share_budget_with'
    create_budget = CreateBudget.Field()
    update_budget = UpdateBudget.Field()
    delete_budget = DeleteBudget.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
