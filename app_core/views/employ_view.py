from rest_framework.views import APIView
from rest_framework.response import Response
from app_core.serializers.factura_serializer import FacturaSerializer
from app_core.utils.tools import ToolsAndOthers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.http import FileResponse, HttpResponse
import os
from rest_framework.exceptions import NotFound
from rest_framework import status

from app_core.services.implementations.employ_service import EmployService
from app_core.services.interfaces.employ_service_interface import EmployServiceInterface

from rest_framework.pagination import PageNumberPagination  # Importa la paginación


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

class GetFactsPendientes(APIView):
    empleadoService: EmployServiceInterface = EmployService()
    
    def get(self,request):
        try:
            # Usamos el paginador de Django REST Framework
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Número de facturas por página
            
            # Obtener la ruta del archivo generado
            facturasPendientes_df = self.empleadoService.obtenerFacturasPendientes()

            facturasList=ToolsAndOthers.dfToListFact(facturasPendientes_df)

            # Paginamos los usuarios
            result_page = paginator.paginate_queryset(facturasList, request)
            serializer = FacturaSerializer(result_page, many=True)

            # Devolvemos la paginación junto con los datos serializados
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({
                'error': True,
                'respuesta': {'mensaje': f'Error al obtener las facturas: {str(e)}'}
            }, status=500)
        

        