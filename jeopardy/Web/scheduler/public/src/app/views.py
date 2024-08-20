from django.shortcuts import render
from app.models import Reminder
from datetime import datetime
from django.db.models.functions import Extract
from django.db import connection
from django.contrib import messages

TO_SECOND = {
    "minute": 60,
    "hour": 60 * 60,
    "day": 24 * 60 * 60,
    "week": 7 * 24 * 60 * 60,
    "month": 30 * 7 * 24 * 60 * 60,
    "year": 12 * 30 * 7 * 24 * 60 * 60,
}

def index(req):
    return render(req, 'index.html')

def new_page(req):
    if req.method == "POST":
        title = req.POST.get('title', '')
        event_date = req.POST.get('event_date', '2022-01-01')
        event_time = req.POST.get('event_time', '00:00')
        repeat = req.POST.get('repeat', 'no repeat')
        
        execdate = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
        period = 0
        if repeat != "no repeat":
            period = Extract(execdate, repeat) * TO_SECOND.get(repeat, 0)
        
        try:
            reminder = Reminder(title=title, execdate=execdate, period=period)
            reminder.save()
            messages.success(req, 'Schedule created successfully.')
        except:
            messages.error(req, 'Something went wrong.')

    return render(req, 'new.html')
