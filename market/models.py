from django.db import models
import uuid

from trade_hub.models import UserItem
from users.models import Profile
# Create your models here.

class MarketItem(models.Model):
    NEW = 'N'
    SOLD = 'SD'
    CANCELED = 'CD'

    STATUSES = [
        (NEW, 'New'),
        (SOLD, 'Sold'),
        (CANCELED, 'Canceled'),
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user_item = models.ForeignKey(UserItem, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="seller")
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="buyer")
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUSES, default=NEW)


    def __str__(self):
        return f"{self.user_item} - ${self.price}"
