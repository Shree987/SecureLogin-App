from django.contrib import admin
from django.contrib.auth.models import Group
from accounts.forms import UserAdmin
from accounts.models import MyUser

admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)