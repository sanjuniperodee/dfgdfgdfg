from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(UserCreateRequest)
admin.site.register(Type)
admin.site.register(Document)
admin.site.register(University)
