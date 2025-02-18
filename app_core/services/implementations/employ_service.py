import pandas as pd
import os
from pathlib import Path
from app_core.services.interfaces.employ_service_interface import EmployServiceInterface
from app_core.utils.jwt_utils import JWTUtils
from app_core.utils.conversorLogic.generator  import SafiteGenerator
from app_core.services.interfaces.usuario_service_interface import UserServiceInterface
from app_core.services.implementations.usuario_service import UserService
from app_core.services.interfaces.registro_service_interface import RegistroServiceInterface
from app_core.services.implementations.registro_service import RegistroService


class EmployService(EmployServiceInterface):

    usuario_service: UserServiceInterface = UserService()
    safite_service: SafiteGenerator = SafiteGenerator()
    registro_service: RegistroServiceInterface = RegistroService()

    def crear_plano(self,id):

        # Filtrar las filas que están solo en safit_df
        safit_exclusive = self.obtenerFacturasPendientes()
        # DEJAR LISTO DATAFRAME CON LA INFORMACIÓN COMO LA TABLA QUE SE LE PIDE A SAFITE
        
        usuario = self.usuario_service.obtener_usuario_por_id(id)
        email = usuario.email
        
        ruta_file = self.safite_service.create_plane(safit_exclusive,email)

        self.registro_service.crear_registro(usuario,ruta_file)

        return ruta_file
    
    def obtenerFacturasPendientes(self):

        current_directory = os.path.dirname(os.path.abspath(__file__))

         # CONSULTAR DOCUMENTOS DE SAFITE
        # Ruta de la carpeta que contiene el archivo de credenciales
        ruta_safit = os.path.normpath(os.path.join(current_directory, '../../utils/conversorLogic/data/safit.csv'))
        # Ajusta esta ruta a tu archivo
        safit_df = pd.read_csv(ruta_safit, sep=";", encoding="latin1")



        # CONSULTAR DOCUMENTOS DE SIESA
        ruta_siesa = os.path.normpath(os.path.join(current_directory, '../../utils/conversorLogic/data/siesa.csv'))   # Ajusta esta ruta a tu archivo
        siesa_df = pd.read_csv(ruta_siesa, sep=";", encoding="latin1")

        result = safit_df.merge(siesa_df[['C.O.', 'Tipo de documento', 'Consecutivo', 'documento tercero cliente']], 
                        on=['C.O.', 'Tipo de documento', 'Consecutivo', 'documento tercero cliente'], 
                        how='left', indicator=True)
    
        # Filtrar los registros que están solo en df_a
        safit_exclusive = result[result['_merge'] == 'left_only'].drop(columns=['_merge'])

        #print(safit_exclusive.columns)

        return safit_exclusive