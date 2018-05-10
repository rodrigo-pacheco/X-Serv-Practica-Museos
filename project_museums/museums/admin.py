from django.contrib import admin

# Register your models here.

from .models import Museumm
from .models import Comment
from .models import User
from .models import Style

admin.site.register(Museumm)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Style)
