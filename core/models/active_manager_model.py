from django.db import models

class ActiveManager(models.Manager):
    '''Manager that excludes soft-deleted records by default'''
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)