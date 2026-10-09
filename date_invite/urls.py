from django.contrib import admin
from django.urls import path
from dates import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.invitation, name="invitation"),
    path("activity/", views.activity, name="activity"),
    path("schedule/", views.schedule, name="schedule"),
    path("ride/", views.ride, name="ride"),
    path("celebration/", views.celebration, name="celebration"),
    path("calendar.ics", views.calendar_invite, name="calendar_invite"),
    path("start-over/", views.start_over, name="start_over"),
]
