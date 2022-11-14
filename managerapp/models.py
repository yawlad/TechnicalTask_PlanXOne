from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class Transaction(models.Model):
    money_amount = models.IntegerField(_('money amount'), default=0)
    datetime = models.DateTimeField(_('datetime'), default=datetime.now())
    organization = models.CharField(_('organization'), max_length=256)
    description = models.CharField(_('description'), max_length=1024)
    category = models.ForeignKey('categoriesapp.Category', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('authapp.User', on_delete=models.CASCADE, blank=True, null=True) 
    def __str__(self):
        return self.datetime

    def set_user(self, user):
        self.user = user
        self.save()