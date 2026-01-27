from django.db import models

class SOAT(models.Model):
    '''Model for Mandatory Traffic Accident Insurances.'''

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Name of Institution',
        help_text='Name of the institution'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=('Is Active'),
    )
    
    class Meta:
        verbose_name = 'Mandatory Traffic Accident Insurance'
        verbose_name_plural = "Mandatory Traffic Accident Insurances"
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name