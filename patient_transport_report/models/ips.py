from django.db import models

class IPS(models.Model):
    '''Model for receiving institutions.'''
    
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Name of Institution',
        help_text="Name of the receiving institution"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=('Is Active'),
    )
    
    class Meta:
        verbose_name = 'Receiving Institution'
        verbose_name_plural = "Receiving Institutions"
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name