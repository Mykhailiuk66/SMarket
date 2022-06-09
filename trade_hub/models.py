from django.db import models
import uuid

from users.models import Profile

# Create your models here.

class Item(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    stattrak = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to='items/', default='items/empty_trade_slot.png') 
    game = models.ForeignKey("trade_hub.Game", on_delete=models.CASCADE)
    quality = models.ForeignKey("trade_hub.ItemQuality", on_delete=models.SET_NULL, null=True)
    exterior = models.ForeignKey("trade_hub.ItemExterior", on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return ("StatTrak™ " if self.stattrak else "") + f"{self.name} ({self.quality.name})"
    
    class Meta:
        ordering = ["name"]
        unique_together = [['name', 'stattrak', 'quality', 'exterior']]
        

class UserItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    float = models.DecimalField(max_digits=18, decimal_places=17, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Trade(models.Model):
    NEW = 'N'
    REVIEWING = 'RW'
    DECLINED = 'DC'
    CANCELED = 'CD'
    SUCCESS = 'SC'

    STATUSES = [
        (NEW, 'New'),
        (REVIEWING, 'Reviewing'),
        (DECLINED, 'Declined'),
        (CANCELED, 'Canceled'),
        (SUCCESS, 'Success'),
    ]


    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="creator")
    second_party = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="second_party")
    guarantor = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="guarantor")
    status = models.CharField(max_length=2, choices=STATUSES, default=NEW)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.id} - {self.status}"
    

    class Meta:
        ordering = ["-created"]


class TradeItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.trade.id} - {self.item}"


class ItemQuality(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=500)
    color_hex = models.CharField(default="#FFFFFF", max_length=9)
    game = models.ForeignKey("trade_hub.Game", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.game.short_name})"


class ItemExterior(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=500)
    game = models.ForeignKey("trade_hub.Game", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.game.short_name})"


class Game(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.short_name})"
