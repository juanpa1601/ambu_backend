from django.db import models

class ARL(models.Model):
    '''Model for Occupational Risk Managements.'''

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Name of Institution',
        help_text='Name of the receiving institution'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=('Is Active'),
    )
    
    class Meta:
        verbose_name = 'Occupational Risk Management'
        verbose_name_plural = "Occupational Risk Managements"
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name