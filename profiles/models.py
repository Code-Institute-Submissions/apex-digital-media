from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

from packages.models import Package


class UserProfile(models.Model):
    """
    A user profile model for maintaining
    delivery information and user details
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=1, blank=True)
    default_street_address1 = models.CharField(
        max_length=80, null=1, blank=True)
    default_street_address2 = models.CharField(
        max_length=80, null=1, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=1, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()


class ProfileLineItem(models.Model):
    profile = models.ForeignKey(UserProfile, null=False, blank=False,
                                on_delete=models.CASCADE,
                                related_name='lineitems')
    package = models.ForeignKey(Package, null=True, blank=False,
                                editable=False,
                                on_delete=models.CASCADE)

    remaining_pages = models.PositiveSmallIntegerField(null=True, default=0)
    remaining_email_addresses = models.PositiveSmallIntegerField(
        null=True, default=0)
    remaining_seo_updates = models.PositiveSmallIntegerField(
        null=True, default=0)
    remaining_website_updates = models.PositiveSmallIntegerField(
        null=True, default=0)

    def __str__(self):
        return 'Remaining Services'
