from datetime import datetime, timedelta
from urllib.parse import quote
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import DateIdea, DateResponse
from date_invite import config

TIME_SLOTS = [
    ("morning", "morning (10am–12pm)", 10, 12),
    ("lunch", "lunch time (12pm–2pm)", 12, 14),
    ("afternoon", "afternoon (2pm–5pm)", 14, 17),
    ("evening", "evening (6pm–8pm)", 18, 20),
    ("night", "night (8pm–10pm)", 20, 22),
]

def invitation(request):
    if request.method == "POST":
        request.session["accepted"] = True
        return redirect("activity")
    return render(request, "dates/invitation.html", {"site_title": config.SITE_TITLE})

def activity(request):
    if not request.session.get("accepted"):
        return redirect("invitation")
    ideas = DateIdea.objects.filter(active=True)
    if not ideas.exists():
        ideas = [
            {"pk": "backrooms", "title": "See Backrooms", "emoji": "👻", "description": "do you like scary stuff?"},
            {"pk": "dintaifung", "title": "Dinner at Din Tai Fung", "emoji": "🥟", "description": "little dumplings, big happiness"},
            {"pk": "iceskating", "title": "Ice skating", "emoji": "⛸️", "description": "I'm pretty good"},
            {"pk": "arcade", "title": "Arcade date", "emoji": "🎮", "description": "let's get competitive"},
            {"pk": "museum", "title": "Art museum", "emoji": "🎨", "description": "I'll pretend to understand art"},
        ]
    if request.method == "POST":
        selected = str(request.POST.get("idea", ""))
        valid_ids = {str(i.pk) if hasattr(i, "pk") else str(i["pk"]) for i in ideas}
        if selected not in valid_ids:
            return render(request, "dates/activity.html", {"ideas": ideas, "error": "Pick one, pretty please! 💗"})
        if hasattr(ideas, "filter"):
            idea = ideas.get(pk=selected)
            request.session["idea"] = {"title": idea.title, "emoji": idea.emoji}
        else:
            idea = next(i for i in ideas if str(i["pk"]) == selected)
            request.session["idea"] = {"title": idea["title"], "emoji": idea["emoji"]}
        return redirect("schedule")
    return render(request, "dates/activity.html", {"ideas": ideas})

def schedule(request):
    if not request.session.get("idea"):
        return redirect("activity")
    if request.method == "POST":
        date_text = request.POST.get("date", "")
        slot = request.POST.get("time", "")
        allowed = {s[0]: s for s in TIME_SLOTS}
        try:
            chosen_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            chosen_date = None
        if not chosen_date or chosen_date < timezone.localdate() or slot not in allowed:
            return render(request, "dates/schedule.html", {"slots": TIME_SLOTS, "error": "Choose a future date and a time, please ✨"})
        _, label, start_hour, end_hour = allowed[slot]
        request.session["date"] = date_text
        request.session["time_key"] = slot
        request.session["time_label"] = label
        request.session["start_hour"] = start_hour
        request.session["end_hour"] = end_hour
        return redirect("ride")
    return render(request, "dates/schedule.html", {"slots": TIME_SLOTS, "today": timezone.localdate().isoformat()})

def ride(request):
    if not request.session.get("date"):
        return redirect("schedule")
    if request.method == "POST":
        choice = request.POST.get("ride")
        if choice not in ("yes", "no"):
            return HttpResponseBadRequest("Choose a ride option.")
        request.session["ride"] = choice

        # Persist every completed flow. Redirect-after-POST avoids resubmission on refresh.
        idea = request.session.get("idea", {})
        try:
            chosen_date = datetime.strptime(request.session.get("date", ""), "%Y-%m-%d").date()
        except ValueError:
            return redirect("schedule")

        response_record = DateResponse.objects.create(
            activity_title=idea.get("title", "Our date"),
            activity_emoji=idea.get("emoji", ""),
            date=chosen_date,
            time_slot=request.session.get("time_label", ""),
            ride=choice,
        )
        request.session["last_response_id"] = response_record.pk
        return redirect("celebration")
    return render(request, "dates/ride.html")

def _event_details(request):
    idea = request.session.get("idea", {})
    date_text = request.session.get("date", "")
    slot = request.session.get("time_label", "")
    ride = request.session.get("ride", "")
    ride_text = "Yes please 💚" if ride == "yes" else "I'm good 💙"
    return idea, date_text, slot, ride_text


def _message(request):
    idea, date_text, slot, ride_text = _event_details(request)

    try:
        date_display = datetime.strptime(
            date_text, "%Y-%m-%d"
        ).strftime("%A, %d %B %Y")
    except ValueError:
        date_display = date_text

    return (
        "IT'S A DATE!\n\n"
        f"Plan: {idea.get('title', 'Our date')}\n"
        f"Date: {date_display}\n"
        f"Time: {slot}\n"
        f"Ride: {'Yes please' if request.session.get('ride') == 'yes' else 'I am good'}\n\n"
        "Can't wait!!\n"
        f"— {config.INVITER_NAME}"
    )


def celebration(request):
    if not request.session.get("ride"):
        return redirect("ride")
    phone = config.WHATSAPP_PHONE.strip()
    whatsapp_url = f"https://wa.me/{phone}?text={quote(_message(request))}" if phone else ""
    return render(request, "dates/celebration.html", {
        "whatsapp_url": whatsapp_url,
        "phone_configured": bool(phone),
        "idea": request.session.get("idea", {}),
        "date": request.session.get("date", ""),
        "time_label": request.session.get("time_label", ""),
        "ride": request.session.get("ride", ""),
        "inviter_name": config.INVITER_NAME,
    })

def calendar_invite(request):
    if not request.session.get("date") or not request.session.get("idea"):
        return redirect("invitation")
    idea, date_text, slot, ride_text = _event_details(request)
    try:
        date_obj = datetime.strptime(date_text, "%Y-%m-%d").date()
        start_hour = int(request.session["start_hour"])
        end_hour = int(request.session["end_hour"])
    except (ValueError, KeyError, TypeError):
        return redirect("schedule")
    start = datetime.combine(date_obj, datetime.min.time()).replace(hour=start_hour)
    end = datetime.combine(date_obj, datetime.min.time()).replace(hour=end_hour)
    # Floating local times avoid falsely labelling local times as UTC.
    stamp = timezone.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = start.strftime("%Y%m%dT%H%M%S")
    dtend = end.strftime("%Y%m%dT%H%M%S")
    summary = f"{idea.get('emoji', '💗')} {idea.get('title', 'Date')}"
    description = f"Date plan: {idea.get('title', 'Our date')}\nRide: {ride_text}\nCan't wait! 💗"
    esc = lambda s: str(s).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")
    ics = "\r\n".join([
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Cute Date Invitation//EN",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "BEGIN:VEVENT",
        f"DTSTAMP:{stamp}", f"DTSTART:{dtstart}", f"DTEND:{dtend}",
        f"SUMMARY:{esc(summary)}", f"DESCRIPTION:{esc(description)}",
        "END:VEVENT", "END:VCALENDAR", ""
    ])
    response = HttpResponse(ics, content_type="text/calendar; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="our-date.ics"'
    return response

def start_over(request):
    request.session.flush()
    return redirect("invitation")
