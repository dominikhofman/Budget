from django.contrib import admin

from .models import Budget, BudgetEntryCategory, BudgetEntry

admin.site.register(Budget)
admin.site.register(BudgetEntryCategory)
admin.site.register(BudgetEntry)
