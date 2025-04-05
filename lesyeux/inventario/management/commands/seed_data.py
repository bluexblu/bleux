from django.core.management.base import BaseCommand
from django_seed import Seed
from inventario.models import Usuario, Producto, ListaDeseos, Resena, Transaccion

class Command(BaseCommand):
    help = 'Genera datos ficticios para las tablas de la base de datos'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()
        
        # Genera usuarios
        seeder.add_entity(Usuario, 10)  # 10 usuarios
        # Genera productos
        seeder.add_entity(Producto, 10)  # 10 productos
        # Genera lista de deseos
        seeder.add_entity(ListaDeseos, 10)  # 10 lista de deseos
        # Genera reseñas
        seeder.add_entity(Resena, 10)  # 10 reseñas
        # Genera transacciones
        seeder.add_entity(Transaccion, 10)  # 10 transacciones

        inserted_pks = seeder.execute()

        self.stdout.write(self.style.SUCCESS('Datos generados con éxito!'))
