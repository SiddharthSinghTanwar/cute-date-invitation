from django.contrib import admin
from .models import DateIdea, DateResponse

@admin.register(DateIdea)
class DateIdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "emoji", "active", "sort_order")
    list_editable = ("active", "sort_order")
    search_fields = ("title", "description")
    list_filter = ("active",)


@admin.register(DateResponse)
class DateResponseAdmin(admin.ModelAdmin):
    list_display = ("submitted_at", "activity_title", "date", "time_slot", "get_ride_display")
    list_filter = ("ride", "date", "submitted_at")
    search_fields = ("activity_title", "time_slot")
    readonly_fields = ("activity_title", "activity_emoji", "date", "time_slot", "ride", "submitted_at")
    ordering = ("-submitted_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.method in ("GET", "HEAD") and super().has_change_permission(request, obj)
