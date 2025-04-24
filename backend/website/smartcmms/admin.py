from django.contrib import admin
from .models import Form, Activity


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1


class FormAdmin(admin.ModelAdmin):
    inlines = [ActivityInline]


admin.site.register(Form, FormAdmin)
admin.site.register(Activity)
