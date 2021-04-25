from decimal import Decimal
import pytest

from budget.models import Budget, BudgetEntry, BudgetEntryCategory


@pytest.mark.django_db
def test_budget_total():
    budget = Budget(name="Family")
    budget.save()

    entries = BudgetEntry.objects.bulk_create([
        BudgetEntry(budget=budget, amount=d)
        for d in [Decimal('10.99'), Decimal('-15.99'), Decimal('100.22')]
    ])

    for entry in entries:
        entry.save()

    assert budget.total() == Decimal('95.22')
