from django.db import models


class Shift(models.Model):
    """
    Model to represent work shifts (day or night).
    This table should have 2 pre-created records: 'day' and 'night'.
    """

    name = models.CharField(
        max_length=50, unique=True, help_text="Shift name: day or night"
    )

    class Meta:
        verbose_name = "Shift"
        verbose_name_plural = "Shifts"
        ordering = ["name"]

    def __str__(self):
        return self.name
