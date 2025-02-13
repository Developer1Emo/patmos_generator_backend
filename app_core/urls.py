from django.urls import path
from app_core.views.usuario_view import CreateUsuarioView,GetUsuarioIdView,GetUsuariosView,ActualizarUsuarioView

urlpatterns = [
    path('crearUsuarios', CreateUsuarioView.as_view(), name='createUser'), #POST
    path('listUsers', GetUsuariosView.as_view(), name='listUsers'), # GET
    path('detalle-usuario/<str:id>', GetUsuarioIdView.as_view(), name='detalle_usuario'), # GET
    path('actualizar-usuario/<str:id>', ActualizarUsuarioView.as_view(), name='actualizar_usuario'), # PUT

    
]