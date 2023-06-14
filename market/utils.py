from users.models import Discount


def revise_profile_discount(profile):
    total_trade_amount = profile.total_trade_amount
    discount = Discount.objects.filter(min_trade_amount__lte=total_trade_amount).order_by('-min_trade_amount').first()

    profile.discount = discount.discount
    profile.save()