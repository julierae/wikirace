import json
from urllib.parse import unquote
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import arrow
import logging
from asgiref.sync import sync_to_async

from wikirace.calculate import calculate_path
from wikirace.models import Race

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def input_view(request):
    start_url = request.GET.get("start_url", "")
    end_url = request.GET.get("end_url", "")
    two_weeks_ago = arrow.utcnow().shift(weeks=-2).datetime
    context = {
        "recent_races": Race.objects.filter(
            start_at__gte=two_weeks_ago, end_at__isnull=False
        ).order_by("-start_at")[:10],
        "start_url": start_url,
        "end_url": end_url,
    }
    return render(request, "wikirace/input.html", context)


async def process_urls(start_title, end_title):
    logger.info(f"Processing Pages: {start_title} to {end_title}")
    return await calculate_path(start_title, end_title)


@require_http_methods(["POST"])
async def results_view(request):
    start_url = request.POST.get("start_url")
    end_url = request.POST.get("end_url")
    start_title = unquote(start_url.split("/wiki/")[-1])
    end_title = unquote(end_url.split("/wiki/")[-1])

    time_start = arrow.utcnow().datetime

    race = await sync_to_async(Race.objects.create)(
        start_title=start_title, end_title=end_title, start_at=time_start
    )

    results, error = await process_urls(start_title, end_title)
    time_end = arrow.utcnow().datetime

    race.result = results
    race.error = error
    race.end_at = time_end
    await sync_to_async(race.save)()

    return render(
        request,
        "wikirace/results_partial.html",
        {
            "results": results,
            "time_start": time_start,
            "time_end": time_end,
            "duration": time_end - time_start,
            "error": error,
        },
    )
