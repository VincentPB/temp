# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Vulnerability, Perimeter, Comment, Tag, Video, URL, Account

#admin.site.register(Perimeter)
admin.site.register(Tag)
admin.site.register(Vulnerability)
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(URL)
admin.site.register(Account)

class PerimeterAdmin(GuardedModelAdmin):
    pass

admin.site.register(Perimeter, PerimeterAdmin)
