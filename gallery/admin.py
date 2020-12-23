from django.contrib import admin
from .models import Exhibition
from .models import Auction
from .models import Images

admin.site.register(Exhibition)
admin.site.register(Auction)
admin.site.register(Images)


# Register your models here.
