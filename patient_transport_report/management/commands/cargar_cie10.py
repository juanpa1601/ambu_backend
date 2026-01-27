import pandas as pd
from django.core.management.base import BaseCommand
from ...models import Diagnosis


class Command(BaseCommand):
    help: str = 'Carga los códigos CIE-10 desde un archivo Excel'

    def add_arguments(
        self, 
        parser
    ):
        parser.add_argument(
            'excel_file',
            type=str,
            help='Ruta al archivo Excel con los códigos CIE-10'
        )

    def handle(
        self, 
        *args: tuple, 
        **options: dict
    ):
        excel_file = options['excel_file']
        
        try:
            # Leer el archivo Excel
            df = pd.read_excel(excel_file)
            
            # Validar que las columnas existan
            if 'codigo' not in df.columns or 'nombre' not in df.columns:
                self.stdout.write(
                    self.style.ERROR('El archivo debe tener columnas "codigo" y "nombre"')
                )
                return
            
            # Limpiar datos existentes (opcional)
            # Diagnosis.objects.all().delete()
            
            registros_creados = 0
            registros_actualizados = 0
            
            for _, row in df.iterrows():
                cie_10 = str(row['codigo']).strip()
                cie_10_name = str(row['nombre']).strip()
                
                # Crear o actualizar el registro
                obj, created = Diagnosis.objects.update_or_create(
                    cie_10=cie_10,
                    defaults={'cie_10_name': cie_10_name}
                )
                
                if created:
                    registros_creados += 1
                else:
                    registros_actualizados += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Proceso completado:\n'
                    f'- Registros creados: {registros_creados}\n'
                    f'- Registros actualizados: {registros_actualizados}'
                )
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Archivo no encontrado: {excel_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al procesar el archivo: {str(e)}')
            )