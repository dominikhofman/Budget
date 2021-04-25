from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model.
    """
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)

    class Meta:
        abstract = True


class Budget(BaseModel):
    """
    Holds information about income and expenses
    """

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name='budgets', verbose_name='Owner', on_delete=models.CASCADE)

    def total(self) -> Decimal:
        """
        return sum of associated entries
        """
        entries = self.budget_entries.all()
        return sum([entry.amount for entry in entries])

    def __str__(self):
        return self.name


class BudgetEntryCategory(BaseModel):
    """
    Category of income or expense
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "budget entry categories"


class BudgetEntry(BaseModel):
    """
    The component that makes up the budget
    """
    budget = models.ForeignKey(
        Budget, related_name='budget_entries', verbose_name='Budget', on_delete=models.CASCADE)
    category = models.ForeignKey(
        BudgetEntryCategory, related_name='budget_entries', verbose_name='Category',
        on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Amount')

    def __str__(self):
        return f"{self.budget}({self.category}: {self.amount})"

    class Meta:
        verbose_name_plural = "budget entries"
