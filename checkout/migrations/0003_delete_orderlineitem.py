# Generated by Django 3.1.1 on 2020-09-19 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_orderlineitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderLineItem',
        ),
    ]