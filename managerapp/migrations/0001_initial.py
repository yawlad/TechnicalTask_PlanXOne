# Generated by Django 3.2 on 2022-11-14 15:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoriesapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_amount', models.IntegerField(default=0, verbose_name='money amount')),
                ('datetime', models.DateTimeField(default=datetime.datetime(2022, 11, 14, 18, 44, 49, 236510), verbose_name='datetime')),
                ('organization', models.CharField(max_length=256, verbose_name='organization')),
                ('description', models.CharField(max_length=1024, verbose_name='description')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categoriesapp.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
