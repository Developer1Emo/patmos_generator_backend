import pandas as pd
import os
from pathlib import Path
from app_core.services.interfaces.employ_service_interface import EmployServiceInterface
from app_core.utils.jwt_utils import JWTUtils
from app_core.utils.conversorLogic.generator  import SafiteGenerator
from app_core.services.interfaces.usuario_service_interface import UserServiceInterface
from app_core.services.implementations.usuario_service import UserService


class EmployService(EmployServiceInterface):

    usuario_service: UserServiceInterface = UserService()
    safite_service: SafiteGenerator = SafiteGenerator()
    def crear_plano(self,id):

        current_directory = os.path.dirname(os.path.abspath(__file__))
    
        # CONSULTAR DOCUMENTOS DE SAFITE
        # Ruta de la carpeta que contiene el archivo de credenciales
        ruta_safit = os.path.normpath(os.path.join(current_directory, '../../utils/conversorLogic/data/safit.csv'))
        # Ajusta esta ruta a tu archivo
        safit_df = pd.read_csv(ruta_safit, sep=";", encoding="latin1")
        # CONSULTAR DOCUMENTOS DE SIESA
        ruta_siesa = os.path.normpath(os.path.join(current_directory, '../../utils/conversorLogic/data/siesa.csv'))   # Ajusta esta ruta a tu archivo
        siesa_df = pd.read_csv(ruta_siesa, sep=";", encoding="latin1")

        # HACER COMPARACION PARA DEJAR DOCUMENTOS QUE NO SE HAN GENERADO
        # Realizar el merge con el indicador
        result = safit_df.merge(siesa_df, on=['C.O.', 'Tipo de documento', 'Consecutivo', 'documento tercero cliente'], how='left', indicator=True)

        # Filtrar las filas que están solo en safit_df
        safit_exclusive = result[result['_merge'] == 'left_only'].drop(columns=['_merge'])
        # DEJAR LISTO DATAFRAME CON LA INFORMACIÓN COMO LA TABLA QUE SE LE PIDE A SAFITE
        
        usuario = self.usuario_service.obtener_usuario_por_id(id)
        email = usuario.email

        print(email)

        
        ruta_file = self.safite_service.create_plane(safit_df,email)

        return ruta_file