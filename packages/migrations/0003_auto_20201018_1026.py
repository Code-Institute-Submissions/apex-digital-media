# Generated by Django 3.1.1 on 2020-10-18 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_auto_20200912_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='remaining_email_addresses',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='remaining_pages',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='remaining_seo_updates',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='remaining_website_updates',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
