from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png') 
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    registation_date = models.DateTimeField(auto_now_add=True)
    steam_id = models.PositiveBigIntegerField(null=True, blank=True)
    trade_url = models.CharField(max_length=500, null=True, blank=True)
    discount = models.FloatField(default=0.0)
    total_trade_amount = models.FloatField(default=0.0)

