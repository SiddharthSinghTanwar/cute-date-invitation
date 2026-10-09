from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("dates", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="DateResponse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("activity_title", models.CharField(max_length=100)),
                ("activity_emoji", models.CharField(blank=True, default="", max_length=12)),
                ("date", models.DateField()),
                ("time_slot", models.CharField(max_length=80)),
                ("ride", models.CharField(choices=[("yes", "Yes, needs a ride"), ("no", "No ride needed")], max_length=3)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name": "completed date response", "verbose_name_plural": "completed date responses", "ordering": ["-submitted_at"]},
        ),
    ]
