from django.db import models

class EPS(models.Model):
    '''Model for health promoting entities.'''

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Name of Institution',
        help_text="Name of the health promoting entity"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=('Is Active'),
    )
    
    class Meta:
        verbose_name = 'Health Promoting Entity'
        verbose_name_plural = "Health Promoting Entities"
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name