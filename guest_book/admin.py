
#!/usr/bin/env python3

#-*- coding:utf-8; -*-

from django.contrib import admin

from .models import User
from .models import ContactForm

admin.site.register(User)
admin.site.register(ContactForm)


