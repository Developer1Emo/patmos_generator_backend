from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

class AppCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_core'

    def ready(self):
        # Conectar la señal post_migrate para crear el usuario admin después de las migraciones
        post_migrate.connect(crear_usuario_admin, sender=self)

# Función que maneja la creación del usuario admin
def crear_usuario_admin(sender, **kwargs):
    from app_core.models.usuario import Usuario  # Importar el modelo solo cuando se ejecute la señal
    if not Usuario.objects.filter(identificacion='4dm1n').exists():
        try:
            # Si no existe, crea el usuario admin
            password_hash = make_password("1q2w3e4r")  # Cifra la contraseña
            usuario = Usuario.objects.create(
                identificacion="4dm1n",
                nombre="Administrador",
                rol="ADMINISTRADOR",
                email="asistentededatos@materialesemo.com.co",
                password=password_hash,
                estadoUsuario=True,
                telefono="3128028428",
                direccion="Barrio la milagrosa"
            )
            usuario.save()
            print("Usuario administrador creado.")
        except Exception as e:
            print("Error al crear el usuario: " + str(e))
