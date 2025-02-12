from django.urls import path
from app_core.views.usuario_view import CreateUsuarioView

urlpatterns = [
    path('crearUsuarios/', CreateUsuarioView.as_view(), name='createUser'),
    #path('crearDetail/<int:pk>/', UsuarioDetailAPIView.as_view(), name='usuarioDetail'),
]