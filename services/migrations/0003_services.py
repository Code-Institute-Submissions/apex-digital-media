# Generated by Django 3.1.1 on 2020-10-19 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0002_delete_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_pages', models.PositiveSmallIntegerField(default=0, null=True)),
                ('remaining_email_addresses', models.PositiveSmallIntegerField(default=0, null=True)),
                ('remaining_seo_updates', models.PositiveSmallIntegerField(default=0, null=True)),
                ('remaining_website_updates', models.PositiveSmallIntegerField(default=0, null=True)),
            ],
        ),
    ]