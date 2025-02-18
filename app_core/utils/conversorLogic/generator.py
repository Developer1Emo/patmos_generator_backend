import pandas as pd
from app_core.utils.conversorLogic.convers_estruc_plan import ConversorEstructurado
from app_core.utils.conversorLogic.utils_convert.util_tools import ToolsConverter


class SafiteGenerator():
    
    def create_plane(self,safit_df,email):
        
        inicio=ConversorEstructurado.inicio_plano()
        encabezado = ConversorEstructurado.encabezado_plano(safit_df)
        ultimoReg = ToolsConverter.get_final_reg(encabezado)
        movimientos = ConversorEstructurado.movimientos_plano(safit_df,ultimoReg)
        ultimoReg = ToolsConverter.get_final_reg(movimientos)
        cartera = ConversorEstructurado.cartera_plano(safit_df,ultimoReg)
        ultimoReg = ToolsConverter.get_final_reg(cartera)
        final = ConversorEstructurado.final_plano(ultimoReg)


        contenido1 = self.generador_archivo_plano( inicio  )
        contenido2 = self.generador_archivo_plano( encabezado )
        contenido3 = self.generador_archivo_plano( movimientos )
        contenido4 = self.generador_archivo_plano( cartera )
        contenido5 = self.generador_archivo_plano( final )

        contenido_final = contenido1 + contenido2 + contenido3 + contenido4 + contenido5

        nombre_doc= ToolsConverter.nombrar_doc(email)
        
        ruta_file = ToolsConverter.create_file(nombre_doc,contenido_final)

        return ruta_file

    def generador_archivo_plano(self, df ):
    
        try:

            # Validación de columnas y filas
            if df.empty:
                raise ValueError("La hoja está vacía.")
            
            # Eliminar columnas vacías y filas vacías
            df = df.dropna(how='all', axis=1)
            df = df.dropna(how='all', axis=0)
            #df = df.drop(columns=["Enc"])
            
            # Verificar que las columnas tengan encabezados
            encabezados = df.columns.tolist()
            
            if all(pd.isna(col) for col in encabezados):
                raise ValueError("La hoja no contiene encabezados válidos.")
            
            # Extraer las filas de datos a partir de la fila 4 (índice 3 en pandas)
            df_datos = df.iloc[2:].reset_index(drop=True)
            
            # Validar los tipos de datos y longitudes
            tipos = df.iloc[0].tolist()  # Fila 2 define tipos (Num o texto)
            longitudes = df.iloc[1].tolist()  # Fila 3 define longitudes
            
            text=""
            for _, row in df_datos.iterrows():
                line = ""
                for idx, value in enumerate(row):
                    # Manejo de valores nulos
                    if pd.isna(value):
                        value = ""
                    
                    # Aplicar longitud y formato
                    longitud = int(longitudes[idx]) if not pd.isna(longitudes[idx]) else 0
                    if tipos[idx] == "float64":
                        line += str(value).zfill(longitud)
                    else:
                        line += str(value).ljust(longitud)
                text+=line+"\n"

            
            #print(f"Exito")
            return text
        
        except Exception as e:
            print(f"Error: {e}")
            return "Error: "+e
