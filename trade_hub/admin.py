from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Item)
admin.site.register(models.UserItem)
admin.site.register(models.Trade)
admin.site.register(models.TradeItem)
admin.site.register(models.ItemQuality)
admin.site.register(models.ItemExterior)
admin.site.register(models.Game)

