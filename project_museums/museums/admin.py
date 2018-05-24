from django.contrib import admin

# Register your models here.

from .models import Museum
from .models import Comment
from .models import User
from .models import Style

admin.site.register(Museum)
admin.site.register(Comment)
admin.site.register(Style)
