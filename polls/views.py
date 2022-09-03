from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

def index(request):
    return HttpResponse('Hello its me ')


def showtime(request) -> HttpResponse:
    """Return the local time and date."""
    thaitime = timezone.localtime()
    msg = f"<p>The time is {thaitime}.</p>"
    # return the msg in an HTTP response
    return HttpResponse(msg)
