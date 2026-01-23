# Generated migration to add is_completed field

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "daily_monthly_inventory",
            "0003_shift_dailymonthlyinventory_support_staff_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="dailymonthlyinventory",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
    ]
