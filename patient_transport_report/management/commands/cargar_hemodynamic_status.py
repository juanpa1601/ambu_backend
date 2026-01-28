from django.core.management.base import BaseCommand
from patient_transport_report.models import HemodynamicStatus

class Command(BaseCommand):
    help = 'Carga los estados hemodinámicos predefinidos en la base de datos'

    def handle(self, *args, **kwargs):
        hemodynamic_statuses_data = [
            {'name': 'Hemodinámicamente Estable', 'order': 1},
            {'name': 'Paro respiratorio', 'order': 2},
            {'name': 'Hemodinámicamente Inestable', 'order': 3},
            {'name': 'Paro cardiorespiratorio', 'order': 4},
            {'name': 'Orden de no Reanimación', 'order': 5},
            {'name': 'Sin signos vitales', 'order': 6},
        ]

        created_count = 0
        updated_count = 0

        for data in hemodynamic_statuses_data:
            status, created = HemodynamicStatus.objects.update_or_create(
                name=data['name'],
                defaults={
                    'order': data['order'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {status.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Actualizado: {status.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado:\n'
                f'   - {created_count} estados hemodinámicos creados\n'
                f'   - {updated_count} estados hemodinámicos actualizados\n'
                f'   - {created_count + updated_count} total procesados'
            )
        )