from django.db import models

class DateIdea(models.Model):
    title = models.CharField(max_length=100)
    emoji = models.CharField(max_length=12, blank=True, default="💗")
    description = models.CharField(max_length=180, blank=True)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "date idea"
        verbose_name_plural = "date ideas"

    def __str__(self):
        return f"{self.emoji} {self.title}"


class DateResponse(models.Model):
    RIDE_CHOICES = [
        ("yes", "Yes, needs a ride"),
        ("no", "No ride needed"),
    ]
    activity_title = models.CharField(max_length=100)
    activity_emoji = models.CharField(max_length=12, blank=True, default="")
    date = models.DateField()
    time_slot = models.CharField(max_length=80)
    ride = models.CharField(max_length=3, choices=RIDE_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "completed date response"
        verbose_name_plural = "completed date responses"

    def __str__(self):
        return f"{self.date} — {self.activity_title} ({self.get_ride_display()})"
