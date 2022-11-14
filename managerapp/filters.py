from django_filters import rest_framework as filters

from .models import Transaction


class TransactionFilter(filters.FilterSet):
    datetime = filters.DateTimeFromToRangeFilter()
    money_amount = filters.RangeFilter()

    

    class Meta:
        model = Transaction
        fields = ['datetime', 'money_amount']