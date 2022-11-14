from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    
    name = models.CharField(_('name'), max_length=256)
    user = models.ForeignKey('authapp.User', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name

    def set_user(self, user):
        self.user = user
        self.save()
    

class StandartCategory(models.Model):
    name = models.CharField(_('name'), max_length=256, unique=True)
    def __str__(self):
        return self.name