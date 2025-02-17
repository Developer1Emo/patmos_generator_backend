import pandas as pd
import os
from datetime import datetime


class ToolsConverter():
    
    def create_file(nombre_doc,data):
        
        ruta="../exports/"+nombre_doc
         # Cargar el archivo JSON en un DataFrame
        current_directory = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.normpath(os.path.join(current_directory, ruta))
        # Abrimos (o creamos) el archivo y escribimos el contenido
        with open(ruta, 'w') as archivo:
            archivo.write(data)
        return ruta

    def get_final_reg(df_g):
        df_g.columns = df_g.columns.str.upper()
        # Verificar que el DataFrame no esté vacío
        if df_g.empty:
            raise ValueError("El DataFrame está vacío.")
        
        # Obtener el último valor de la columna 'F_NUMERO_REG'
        ultimo_valor = df_g["F_NUMERO_REG"].iloc[-1]

        # Validar que el valor no sea nulo
        if pd.isna(ultimo_valor):
            raise ValueError("El campo F_NUMERO_REG está vacío o es nulo.")
        
        return ultimo_valor   
    
    def nombrar_doc(email):
        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now()
        # Convertirla a una cadena con el formato deseado
        cadena_fecha_hora = fecha_hora_actual.strftime("%Y-%m-%d %H-%M-%S")
        # Mostrar la cadena

        return email+" - "+cadena_fecha_hora+".txt"