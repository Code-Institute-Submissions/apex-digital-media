# Generated by Django 3.1.1 on 2020-10-31 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20201025_1535'),
        ('website_details', '0008_auto_20201025_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=1, on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile'),
        ),
    ]
