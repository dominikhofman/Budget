from decimal import Decimal

import pytest

from budget.models import Budget, BudgetEntry


@pytest.mark.django_db
def test_budget_total(admin_user):
    budget = Budget(name="Family", owner=admin_user)
    budget.save()

    entries = BudgetEntry.objects.bulk_create([
        BudgetEntry(budget=budget, amount=d)
        for d in [Decimal('10.99'), Decimal('-15.99'), Decimal('100.22')]
    ])

    for entry in entries:
        entry.save()

    result = budget.total()
    assert isinstance(result, Decimal)
    assert result == Decimal('95.22')


@pytest.mark.django_db
def test_budget_total_with_no_budget_entries(admin_user):
    budget = Budget(name="Family", owner=admin_user)
    budget.save()

    result = budget.total()
    assert isinstance(result, Decimal)
    assert result == Decimal('0')
