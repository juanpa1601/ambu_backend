from django.core.management.base import BaseCommand
from patient_transport_report.models import SkinCondition

class Command(BaseCommand):
    help = 'Carga las condiciones de piel predefinidas en la base de datos'

    def handle(self, *args, **kwargs):
        skin_conditions_data = [
            {'name': 'Normal', 'order': 1},
            {'name': 'Húmeda', 'order': 2},
            {'name': 'Pálida', 'order': 3},
            {'name': 'Caliente', 'order': 4},
            {'name': 'Enrojecida', 'order': 5},
            {'name': 'Seca', 'order': 6},
            {'name': 'Cianótica', 'order': 7},
            {'name': 'Ictérica', 'order': 8},
            {'name': 'Fría', 'order': 9},
        ]

        created_count = 0
        updated_count = 0

        for data in skin_conditions_data:
            condition, created = SkinCondition.objects.update_or_create(
                name=data['name'],
                defaults={
                    'order': data['order'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creada: {condition.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Actualizada: {condition.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado:\n'
                f'   - {created_count} condiciones creadas\n'
                f'   - {updated_count} condiciones actualizadas\n'
                f'   - {created_count + updated_count} total procesadas'
            )
        )