# Generated by Django 2.0 on 2019-12-16 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_auto_20191211_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcart',
            name='size',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]