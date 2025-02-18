from django.urls import path
from app_core.views.usuario_view import CreateUsuarioView,GetUsuarioIdView,GetUsuariosView,ActualizarUsuarioView
from app_core.views.auth_view import IniciarSesionView
from app_core.views.employ_view import  GenerarPlano, GetFactsPendientes

urlpatterns = [
    path('crearUsuarios', CreateUsuarioView.as_view(), name='createUser'), #POST
    path('listUsers', GetUsuariosView.as_view(), name='listUsers'), # GET
    path('detalle-usuario/<str:id>', GetUsuarioIdView.as_view(), name='detalle_usuario'), # GET
    path('actualizar-usuario/<str:id>', ActualizarUsuarioView.as_view(), name='actualizar_usuario'), # PUT
    path('iniciar-sesion', IniciarSesionView.as_view(), name='iniciarSesion'),
    path('crearPlano/<str:id>', GenerarPlano.as_view(), name='crearPlano'),
    path('usuarios/listFact', GetFactsPendientes.as_view(), name='crearPlano'),
    
]