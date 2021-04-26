import graphene
from graphene_django import DjangoObjectType
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
    all_budgets = graphene.List(BudgetType)
    all_shared_budgets = graphene.List(BudgetType)
    all_budget_entry_categories = graphene.List(BudgetEntryCategoryType)

    budget_total = graphene.Decimal(budget_id=graphene.ID(required=True))

    def resolve_budget_total(self, info, budget_id):
        try:
            budget = Budget.objects.get(pk=budget_id)
        except Budget.DoesNotExist:
            return None

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


schema = graphene.Schema(query=Query)
