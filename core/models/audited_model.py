from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .time_stamped_model import TimeStampedModel

class AuditedModel(TimeStampedModel):
    '''
    Extended abstract model that also tracks WHO created/modified.
    
    Critical for healthcare compliance (HIPAA, GDPR, ISO 27001).
    Provides complete audit trail.
    '''
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_created',
        editable=False,
        help_text='User who created this record'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_updated',
        help_text='User who last updated this record'
    )
    
    # Campos opcionales para casos especiales
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Soft delete flag for GDPR compliance'
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the record was soft deleted'
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_deleted',
        help_text='User who soft deleted this record'
    )
    
    class Meta:
        abstract = True
    
    def soft_delete(
        self, 
        user: User = None
    ):
        '''
        Soft delete (mark as deleted without removing from database).
        Required for GDPR compliance and audit trails.
        '''
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])
    
    def restore(self):
        '''Restore a soft-deleted record'''
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])


class ActiveManager(models.Manager):
    '''Manager that excludes soft-deleted records by default'''
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)