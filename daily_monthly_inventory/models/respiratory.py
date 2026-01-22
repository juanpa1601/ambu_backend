from django.core.validators import MaxValueValidator
from django.db import models


class Respiratory(models.Model):
    simple_humidifier_jar = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Simple humidifier jar quantity",
    )
    venturi_humidifier_jar = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Venturi humidifier jar quantity",
    )
    laryngeal_mask_4 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Laryngeal mask #4 quantity",
    )
    laryngeal_mask_5 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Laryngeal mask #5 quantity",
    )
    adult_nasal_cannula = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult nasal cannula quantity",
    )
    adult_simple_mask = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult simple mask quantity",
    )
    adult_non_rebreather_mask = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult non-rebreather mask quantity",
    )
    adult_venturi_system = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult venturi system quantity",
    )
    adult_nebulizer_kit = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult nebulizer kit quantity",
    )
    oropharyngeal_airway_3 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Oropharyngeal airway #3 quantity",
    )
    oropharyngeal_airway_4 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Oropharyngeal airway #4 quantity",
    )
    oropharyngeal_airway_5 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Oropharyngeal airway #5 quantity",
    )
    o2_connecting_tube = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="O2 connecting tube quantity",
    )
    adult_bvm_bag_valve_mask = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult BVM bag valve mask quantity",
    )
    yankauer_suction_tip = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Yankauer suction tip quantity",
    )
    adult_spacer_chamber = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult spacer chamber quantity",
    )
    suction_tubing = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Suction tubing quantity",
    )
    suction_catheter = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Suction catheter quantity",
    )

    def __str__(self):
        return f"Respiratory #{self.pk}"
