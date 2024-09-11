from django.contrib import admin

from wikirace.models import Race


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = (
        "start_title",
        "end_title",
        "start_at",
        "end_at",
        "get_elapsed_time_str",
        "error",
    )
