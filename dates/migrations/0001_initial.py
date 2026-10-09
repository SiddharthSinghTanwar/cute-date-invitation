from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="DateIdea",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("emoji", models.CharField(blank=True, default="💗", max_length=12)),
                ("description", models.CharField(blank=True, max_length=180)),
                ("active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["sort_order", "title"], "verbose_name": "date idea", "verbose_name_plural": "date ideas"},
        ),
    ]
