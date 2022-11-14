from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from categoriesapp.models import Category
from managerapp.models import Transaction

from datetime import datetime, timedelta


class User(AbstractUser):

    balance = models.IntegerField(_('balance'), default=0)
    is_deleted = models.BooleanField(_('deleted'), default=False)

    def __str__(self):
        return self.username

    def recount_balance(self):
        self.balance = Transaction.objects.filter(user=self).values(
            'money_amount').aggregate(balance_=models.Sum('money_amount'))['balance_']
        self.save()

    def get_statistics(self):
        user_transactions = Transaction.objects.filter(user__id=self.id)
        user_categories = Category.objects.filter(user__id=self.id)
        statistics_dict = {}

        total = user_transactions.aggregate(total=models.Sum('money_amount'))
        total_income = user_transactions.filter(
            money_amount__gt=0).aggregate(income=models.Sum('money_amount'))
        total_outcome = user_transactions.filter(
            money_amount__lt=0).aggregate(outcome=models.Sum('money_amount'))
        total.update(total_income)
        total.update(total_outcome)

        year_transactions = user_transactions.filter(
            datetime__gte=datetime.now()-timedelta(days=365))
        year_total = year_transactions.aggregate(
            total=models.Sum('money_amount'))
        year_income = year_transactions.filter(
            money_amount__gt=0).aggregate(income=models.Sum('money_amount'))
        year_outcome = year_transactions.filter(
            money_amount__lt=0).aggregate(outcome=models.Sum('money_amount'))
        year_total.update(year_income)
        year_total.update(year_outcome)

        month_transactions = user_transactions.filter(
            datetime__gte=datetime.now()-timedelta(days=30))
        month_total = month_transactions.aggregate(
            total=models.Sum('money_amount'))
        month_income = month_transactions.filter(
            money_amount__gt=0).aggregate(income=models.Sum('money_amount'))
        month_outcome = month_transactions.filter(
            money_amount__lt=0).aggregate(outcome=models.Sum('money_amount'))
        month_total.update(month_income)
        month_total.update(month_outcome)

        week_transactions = user_transactions.filter(
            datetime__gte=datetime.now()-timedelta(days=7))
        week_total = week_transactions.aggregate(
            total=models.Sum('money_amount'))
        week_income = week_transactions.filter(
            money_amount__gt=0).aggregate(income=models.Sum('money_amount'))
        week_outcome = week_transactions.filter(
            money_amount__lt=0).aggregate(outcome=models.Sum('money_amount'))
        week_total.update(week_income)
        week_total.update(week_outcome)

        day_transactions = user_transactions.filter(
            datetime__gte=datetime.now()-timedelta(days=1))
        day_total = day_transactions.aggregate(
            total=models.Sum('money_amount'))
        day_income = day_transactions.filter(money_amount__gt=0).aggregate(
            income=models.Sum('money_amount'))
        day_outcome = day_transactions.filter(money_amount__lt=0).aggregate(
            outcome=models.Sum('money_amount'))
        day_total.update(day_income)
        day_total.update(day_outcome)

        periods = {'total': total,
                   'year': year_total,
                   'month': month_total,
                   'week': week_total,
                   'day': day_total
                   }
        
        for period in periods:
            for t_i_o in periods[period]:
                if periods[period][t_i_o] == None:
                    periods[period][t_i_o] = 0

        categories_statistics = {}
        for category in user_categories:
            category_transactions = user_transactions.filter(category=category)
            category_total = category_transactions.aggregate(
                total=models.Sum('money_amount'))
            if category_total['total'] == None:
                break
            category_income = category_transactions.filter(
                money_amount__gt=0).aggregate(income=models.Sum('money_amount'))
            category_outcome = category_transactions.filter(
                money_amount__lt=0).aggregate(outcome=models.Sum('money_amount'))
            category_total.update(category_income)
            category_total.update(category_outcome)
            categories_statistics[category.name] = category_total

        for cat in categories_statistics:
            for t_i_o in categories_statistics[cat]:
                if categories_statistics[cat][t_i_o] == None:
                    categories_statistics[cat][t_i_o] = 0

        min_max_categories = {}
        try:
            max_cat = max(categories_statistics, key=lambda x: categories_statistics[x]['total'])
            min_cat = min(categories_statistics, key=lambda x: categories_statistics[x]['total'])
            
            min_max_categories['maximum'] = {max_cat: categories_statistics[max_cat]['total']}
            min_max_categories['minimum'] = {min_cat: categories_statistics[min_cat]['total']}
        except:
            min_max_categories['maximum'] = {}
            min_max_categories['minimum'] = {}


        statistics_dict['periods'] = periods
        statistics_dict['categories'] = categories_statistics
        statistics_dict['min/max categories'] = min_max_categories
                
        return statistics_dict