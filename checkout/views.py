from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.contrib.auth.decorators import login_required
from packages.models import Package
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages

from .forms import OrderForm
from .models import Order
from profiles.models import UserProfile
from services.models import Services
from profiles.forms import UserProfileForm

import stripe


@require_POST
def cache_checkout_data(request):
    """ A view used to cache some checkout data. """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request, package_id):
    """ A view to handle purchasing of a package. """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    package = get_object_or_404(Package, pk=package_id)
    total = round(package.price)
    if request.method == 'POST':
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
            'package': package,
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.package = package
            order.save()
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        order_form = OrderForm()
        template = 'checkout/checkout.html'

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=total*100,
            currency=settings.STRIPE_CURRENCY,
        )

        # Attempt to prefill form with user profile info
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                'first_name': profile.user.first_name,
                'last_name': profile.user.last_name,
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            })
        except UserProfile.DoesNotExist:
            order_form = OrderForm()

    context = {
        'order_form': order_form,
        'package': package,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ Handle successful checkouts and initialise remaining service values. """
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        package = get_object_or_404(Package, pk=order.package_id)
        if package.name == "Start Up":
            remaining_services = Services(
                        profile=profile,
                        package=package,
                        remaining_pages=6,
                        remaining_email_addresses=2,
                        remaining_seo_updates=2,
                        remaining_website_updates=5,
                    )
        elif package.name == "Business":
            remaining_services = Services(
                                profile=profile,
                                package=package,
                                remaining_pages=12,
                                remaining_email_addresses=5,
                                remaining_seo_updates=2,
                                remaining_website_updates=10,
                            )
        elif package.name == "Executive":
            remaining_services = Services(
                                profile=profile,
                                package=package,
                                remaining_pages=20,
                                remaining_email_addresses=10,
                                remaining_seo_updates=2,
                                remaining_website_updates=20,
                            )
        else:
            remaining_services = Services(
                profile=profile,
                package=package,
                remaining_pages=6,
                remaining_email_addresses=2,
                remaining_seo_updates=2,
                remaining_website_updates=5,
            )

        remaining_services.save()

        profile_data = {
            'default_phone_number': order.phone_number,
            'default_country': order.country,
            'default_postcode': order.postcode,
            'default_town_or_city': order.town_or_city,
            'default_street_address1': order.street_address1,
            'default_street_address2': order.street_address2,
            'default_county': order.county,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
