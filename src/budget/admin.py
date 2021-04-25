from django.contrib import admin

from .models import Budget, BudgetEntryCategory, BudgetEntry


class BudgetAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


admin.site.register(Budget, BudgetAdmin)
admin.site.register(BudgetEntryCategory, BudgetAdmin)
admin.site.register(BudgetEntry, BudgetAdmin)
