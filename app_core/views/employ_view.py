from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.http import FileResponse, HttpResponse
import os
from rest_framework.exceptions import NotFound
from rest_framework import status

from app_core.services.implementations.employ_service import EmployService
from app_core.services.interfaces.employ_service_interface import EmployServiceInterface


class GenerarPlano(APIView):
    empleadoService: EmployServiceInterface = EmployService()
    
    def get(self,request,id):
        # Obtener la ruta del archivo generado
        file_path = self.empleadoService.crear_plano(id)

        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            return HttpResponse("Archivo no encontrado", status=404)

        try:
            # Abrir el archivo usando FileResponse, que maneja el archivo adecuadamente
            response = FileResponse(open(file_path, 'rb'), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="archivo.txt"'
            return response
        except Exception as e:
            # Manejo de errores si algo falla al intentar leer o enviar el archivo
            print(f"Error al enviar el archivo: {e}")
            return HttpResponse("Error al generar el archivo.", status=500)