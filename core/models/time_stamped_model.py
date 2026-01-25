from django.db import models

class TimeStampedModel(models.Model):
    '''
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    
    Best practice for audit trails in healthcare systems.
    '''
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
        help_text='Timestamp when the record was created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,
        help_text='Timestamp when the record was last updated'
    )
    
    class Meta:
        abstract = True  
        ordering = ['-created_at']