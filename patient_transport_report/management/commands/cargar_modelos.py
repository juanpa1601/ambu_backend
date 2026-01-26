import pandas as pd
from django.core.management.base import BaseCommand
from ...models import (
    IPS,
    EPS,
    ARL,
    SOAT
)


class Command(BaseCommand):
    help = 'Carga instituciones, EPS, ARL y SOAT desde un archivo Excel'

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_file',
            type=str,
            help='Ruta al archivo Excel con las entidades'
        )

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        try:
            # Leer el archivo Excel
            df = pd.read_excel(excel_file)
            
            # Validar que las columnas existan
            columnas_requeridas = ['institucion receptora', 'soat', 'arl', 'eps']
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
            
            if columnas_faltantes:
                self.stdout.write(
                    self.style.ERROR(
                        f'El archivo debe tener las columnas: {", ".join(columnas_requeridas)}\n'
                        f'Columnas faltantes: {", ".join(columnas_faltantes)}'
                    )
                )
                return
            
            # Contadores
            stats = {
                'institucion': {'creados': 0, 'actualizados': 0},
                'soat': {'creados': 0, 'actualizados': 0},
                'arl': {'creados': 0, 'actualizados': 0},
                'eps': {'creados': 0, 'actualizados': 0},
            }
            
            # Procesar cada columna
            self.stdout.write(self.style.SUCCESS('Procesando instituciones receptoras...'))
            stats['institucion'] = self._cargar_entidades(
                df, 'institucion receptora', IPS
            )
            
            self.stdout.write(self.style.SUCCESS('Procesando SOAT...'))
            stats['soat'] = self._cargar_entidades(df, 'soat', SOAT)
            
            self.stdout.write(self.style.SUCCESS('Procesando ARL...'))
            stats['arl'] = self._cargar_entidades(df, 'arl', ARL)
            
            self.stdout.write(self.style.SUCCESS('Procesando EPS...'))
            stats['eps'] = self._cargar_entidades(df, 'eps', EPS)
            
            # Resumen final
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n{"="*60}\n'
                    f'RESUMEN DE CARGA\n'
                    f'{"="*60}\n'
                    f'Instituciones Receptoras:\n'
                    f'  - Creadas: {stats["institucion"]["creados"]}\n'
                    f'  - Actualizadas: {stats["institucion"]["actualizados"]}\n'
                    f'\nEPS:\n'
                    f'  - Creadas: {stats["eps"]["creados"]}\n'
                    f'  - Actualizadas: {stats["eps"]["actualizados"]}\n'
                    f'\nARL:\n'
                    f'  - Creadas: {stats["arl"]["creados"]}\n'
                    f'  - Actualizadas: {stats["arl"]["actualizados"]}\n'
                    f'\nSOAT:\n'
                    f'  - Creadas: {stats["soat"]["creados"]}\n'
                    f'  - Actualizadas: {stats["soat"]["actualizados"]}\n'
                    f'{"="*60}'
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
    
    def _cargar_entidades(self, df, columna, modelo):
        """
        Carga entidades desde una columna del DataFrame.
        
        Args:
            df: DataFrame de pandas
            columna: Nombre de la columna a procesar
            modelo: Modelo de Django donde guardar los datos
        
        Returns:
            dict: Diccionario con contadores de creados y actualizados
        """
        creados = 0
        actualizados = 0
        
        # Obtener valores únicos y eliminar nulos/vacíos
        valores = df[columna].dropna().unique()
        valores = [str(v).strip() for v in valores if str(v).strip()]
        
        for nombre in valores:
            if not nombre or nombre.lower() in ['nan', 'none', '']:
                continue
            
            # Crear o actualizar el registro
            obj, created = modelo.objects.update_or_create(
                name=nombre,
                defaults={'is_active': True}
            )
            
            if created:
                creados += 1
                self.stdout.write(f'  ✓ Creado: {nombre}')
            else:
                actualizados += 1
                self.stdout.write(f'  • Actualizado: {nombre}')
        
        return {'creados': creados, 'actualizados': actualizados}