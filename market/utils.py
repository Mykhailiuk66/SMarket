from users.models import Discount


# def filter_items(request):
#     search_query = ''
    
#     if request.GET.get('search_query'):
#         search_query = request.GET.get('search_query')
    
#     tags = Tag.objects.filter(name__icontains=search_query)
    
#     projects = Project.objects.distinct().filter(
#         Q(title__icontains=search_query) |
#         Q(description__icontains=search_query) |
#         Q(owner__name__icontains=search_query) |
#         Q(tags__in=tags)
#     )
    
#     return projects, search_query



def revise_profile_discount(profile):
    total_trade_amount = profile.total_trade_amount
    discount = Discount.objects.filter(min_trade_amount__lte=total_trade_amount).order_by('-min_trade_amount').first()

    profile.discount = discount.discount
    profile.save()