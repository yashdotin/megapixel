from django.contrib import admin

from .models import DailyHealthLog, HealthAlert, UserHealthProfile

admin.site.register(UserHealthProfile)
admin.site.register(DailyHealthLog)
admin.site.register(HealthAlert)
