import datetime
from decimal import Decimal

from django.db import models


class Budget(models.Model):
    name = models.CharField(max_length=255)

    def total(self) -> Decimal:
        """
        return sum of associated entries
        """
        entries = self.budget_entries.all()
        return sum([entry.amount for entry in entries])


    def __str__(self):
        return self.name


class BudgetEntryCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "budget entry categories"


class BudgetEntry(models.Model):
    budget = models.ForeignKey(
        Budget, related_name='budget_entries', verbose_name='Budget', on_delete=models.CASCADE)
    category = models.ForeignKey(
        BudgetEntryCategory, related_name='budget_entries', verbose_name='Category', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Amount')

    def __str__(self):
        return f"{self.budget}({self.category}: {self.amount})"

    class Meta:
        verbose_name_plural = "budget entries"
