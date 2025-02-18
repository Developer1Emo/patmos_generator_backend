import pandas as pd

from dateutil.relativedelta import relativedelta

import os
class ConversorEstructurado():
    
    def inicio_plano():
        # Definimos los datos según la imagen
        data = {
            "F_NUMERO_REG": ["0000001"],
            "F_TIPO_REG": ["0000"],
            "F_SUBTIPO_REG": ["00"],
            "F_VERSION_REG": ["01"],
            "F_CIA": ["004"]
        }
        
        # Creamos el DataFrame
        df = pd.DataFrame(data)
        
        # Añadimos las filas adicionales
        df = pd.concat([
            pd.DataFrame([[ "Numérico", "Numérico", "Numérico", "Numérico", "Numérico"]], columns=df.columns),
            pd.DataFrame([[ 7, 4, 2, 2, 3]], columns=df.columns),
            df
        ], ignore_index=True)
        
        return df

    def encabezado_plano(safit): 
        # Cargar el archivo JSON en un DataFrame
        current_directory = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.normpath(os.path.join(current_directory, 'data/json_output/encabezado.json'))
        conector_enc_df = pd.read_json(ruta)
        
        transpuesta = conector_enc_df.T

        # Se transpone el DataFrame(conector) para empezar a diligenciar las columnas con los datos entrantes
        resultado = pd.DataFrame(columns=["F_NUMERO_REG", "F_TIPO_REG", "F_SUBTIPO_REG", "F_VERSION_REG", "F_CIA",
                                        "F_CONSEC_AUTO_REG","F350_ID_CO","F350_ID_TIPO_DOCTO","F350_CONSEC_DOCTO","F350_FECHA",
                                        "F350_ID_TERCERO","F350_ID_CLASE_DOCTO","F350_IND_ESTADO","F350_IND_IMPRESION","F350_NOTAS",
                                        "f350_id_mandato" ])
        
        resultado["F350_ID_CO"] = safit["C.O."]
        resultado["F350_ID_TIPO_DOCTO"] = safit["Tipo de documento"]
        resultado["F350_CONSEC_DOCTO"] = safit["Consecutivo"]
        resultado["F350_FECHA"] = safit["Fecha"]
        # Convertir la columna a tipo datetime
        resultado["F350_FECHA"] = pd.to_datetime(resultado["F350_FECHA"], format="%d/%m/%Y")
        # Formatear la fecha como YYYYMMDD
        resultado["F350_FECHA"] = resultado["F350_FECHA"].dt.strftime("%Y%m%d")
        resultado["F350_ID_TERCERO"] = safit["documento tercero cliente"]
        resultado["F350_NOTAS"] = safit["Notas del documento"]
        
        resultado["F_CIA"] = "004"
        resultado["F_CONSEC_AUTO_REG"] = "0"
        resultado["F_VERSION_REG"] = "02"
        resultado["F_SUBTIPO_REG"] = "00"
        resultado["F_TIPO_REG"] = "0350"
        resultado["F350_ID_CLASE_DOCTO"] = "00030"
        resultado["F350_IND_ESTADO"] = "1"
        resultado["F350_IND_IMPRESION"] = "0"
        resultado["F_NUMERO_REG"] = [str(i).zfill(7) for i in range(2, 2 + len(resultado))]
        resultado["f350_id_mandato"] = ""
        
        # Convertir la primera fila en nombres de columnas
        transpuesta.columns = transpuesta.iloc[0]  # Asignar la primera fila como encabezados
        transpuesta = transpuesta[1:].reset_index(drop=True)  # Eliminar la primera fila y resetear índices
        
        resultado = pd.concat([transpuesta,resultado ], axis=0)
            
        return resultado

    def movimientos_plano(safit,ultimo_reg_encab):
        
        ultimo_reg_encab=int(ultimo_reg_encab)
        
        # Lista de columnas a convertir
        columnas_a_convertir = [
            'Valor bruto local', 'Valor descuentos local', 'Valor subtotal local',
            'Valor impuestos local', 'Valor neto local', 'Valor impuestos',
            'Valor neto', 'Valor subtotal'
        ]

        # Aplicar la transformación a todas las columnas
        safit[columnas_a_convertir] = safit[columnas_a_convertir].replace('[\$,]', '', regex=True).astype(float)
        
        # Cargar el archivo JSON en un DataFrame
        current_directory = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.normpath(os.path.join(current_directory, 'data/json_output/movimiento.json'))
        conector_enc_df = pd.read_json(ruta)

        transpuesta = conector_enc_df.T
        resultado = pd.DataFrame(columns=["f_numero_reg" ,"f_tipo_reg",	"f_subtipo_reg","f_version_reg","f_cia",
                                        "f350_id_co","f350_id_tipo_docto","f350_consec_docto","f351_id_auxiliar","f351_id_tercero",
                                        "f351_id_co_mov","f351_id_un","f351_id_ccosto",	"f351_id_fe",	"f351_valor_db",
                                        "f351_valor_cr",	"f351_valor_db_alt",	"f351_valor_cr_alt",	"f351_base_gravable",	"f351_valor_db2",
                                        "f351_valor_cr2",	"f351_valor_db_alt2",	"f351_valor_cr_alt2",	"f351_base_gravable2",
                                        "f351_valor_db3" ,	"f351_valor_cr3",	"f351_valor_db_alt3",	"f351_valor_cr_alt3",	"f351_base_gravable3",
                                        "f351_valor_imp_asum",	"f351_valor_imp_asum2",	"f351_valor_imp_asum3",	"f351_docto_banco",	"f351_nro_docto_banco",
                                        "f351_nro_alt_docto_banco","f351_notas"

                                        ])
        
        for idx, factura in safit.iterrows():
            # Si el tipo de tercero es persona jurídica
            if factura['Tipo tercero cliente']=="Persona juridica":
                
                subtotal = factura['Valor subtotal']
                porcentaje_1 = subtotal * 0.01
                porcentaje_1_1 = subtotal * 0.011
                
                # Dar formato de 21 caracteres
                subtotal="{:021.4f}".format(subtotal)
                porcentaje_1="{:021.4f}".format(porcentaje_1)
                porcentaje_1_1="{:021.4f}".format(porcentaje_1_1)
                
                df_j = pd.DataFrame({                               
                                    "f_numero_reg":[ultimo_reg_encab+1,ultimo_reg_encab+2,ultimo_reg_encab+3,ultimo_reg_encab+4,ultimo_reg_encab+5],
                                    "f_tipo_reg":["0351","0351","0351","0351","0351"],	
                                    "f_subtipo_reg":["00","00","00","00","00"],
                                    "f_version_reg":["04","04","04","04","04"],
                                    "f_cia":["004", "004", "004", "004", "004"],
                                    "f350_id_co":[factura["C.O."],factura["C.O."],factura["C.O."],factura["C.O."],factura["C.O."]],
                                    "f350_id_tipo_docto":[factura["Tipo de documento"],factura["Tipo de documento"],factura["Tipo de documento"],factura["Tipo de documento"],factura["Tipo de documento"]],
                                    "f350_consec_docto":[factura["Consecutivo"],factura["Consecutivo"],factura["Consecutivo"],factura["Consecutivo"],factura["Consecutivo"]],
                                    "f351_id_auxiliar":["41450501","13551511","23657501","13551509","23658502"],
                                    "f351_id_tercero":[factura["documento tercero cliente"],factura["documento tercero cliente"],factura["documento tercero cliente"],factura["documento tercero cliente"],factura["documento tercero cliente"]],
                                    "f351_id_co_mov":[factura["C.O."],factura["C.O."],factura["C.O."],factura["C.O."],factura["C.O."]],
                                    "f351_id_un":["UN01","UN08","UN08","UN08","UN08"],
                                    "f351_id_ccosto":["V219","","","",""],# IMPORTANTE VALIDAR CENTRO DE COSTO CON KARIME
                                    "f351_id_fe":["","","","",""],
                                    "f351_valor_db":["0000000000000000.0000",porcentaje_1,"0000000000000000.0000",porcentaje_1_1,"0000000000000000.0000"],
                                    "f351_valor_cr":[subtotal,"0000000000000000.0000",porcentaje_1,"0000000000000000.0000",porcentaje_1_1],
                                    "f351_valor_db_alt":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_cr_alt":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_base_gravable":["0000000000000000.0000",subtotal,subtotal,subtotal,subtotal],
                                    "f351_valor_db2":["0000000000000000.0000",porcentaje_1,"0000000000000000.0000",porcentaje_1_1,"0000000000000000.0000"],
                                    "f351_valor_cr2":[subtotal,"0000000000000000.0000",porcentaje_1,"0000000000000000.0000",porcentaje_1_1],
                                    "f351_valor_db_alt2":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_cr_alt2":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_base_gravable2":["0000000000000000.0000",subtotal,subtotal,subtotal,subtotal],
                                    "f351_valor_db3":["0000000000000000.0000",porcentaje_1,"0000000000000000.0000",porcentaje_1_1,"0000000000000000.0000"] ,
                                    "f351_valor_cr3":[subtotal,"0000000000000000.0000",porcentaje_1,"0000000000000000.0000",porcentaje_1_1],
                                    "f351_valor_db_alt3":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_cr_alt3":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_base_gravable3":["0000000000000000.0000",subtotal,subtotal,subtotal,subtotal],
                                    "f351_valor_imp_asum":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_imp_asum2":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_imp_asum3":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_docto_banco":["","","","",""],
                                    "f351_nro_docto_banco":["00000000","00000000","00000000","00000000","00000000"],
                                    "f351_nro_alt_docto_banco":["0000000000000000000000000.0000","0000000000000000000000000.0000","0000000000000000000000000.0000","0000000000000000000000000.0000","0000000000000000000000000.0000"],
                                    "f351_notas":["nota provicional","nota provicional","nota provicional","nota provicional","nota provicional"]
                                    })
                resultado = pd.concat([resultado,df_j], axis=0)
                ultimo_reg_encab=ultimo_reg_encab+5
            else:
                # Si el tipo de tercero es persona natural
            
                subtotal = factura['Valor subtotal']
                #porcentaje_1 = subtotal * 0.01
                porcentaje_1_1 = subtotal * 0.011
                
                # Dar formato de 21 caracteres
                subtotal="{:021.4f}".format(subtotal)
                #porcentaje_1="{:021.4f}".format(porcentaje_1)
                porcentaje_1_1="{:021.4f}".format(porcentaje_1_1)
            
                df_n = pd.DataFrame({                               
                                    "f_numero_reg":[ultimo_reg_encab+1,ultimo_reg_encab+2,ultimo_reg_encab+3],
                                    "f_tipo_reg":["0351","0351","0351"],	
                                    "f_subtipo_reg":["00","00","00"],
                                    "f_version_reg":["04","04","04"],
                                    "f_cia":["004", "004", "004"],
                                    "f350_id_co":[factura["C.O."],factura["C.O."],factura["C.O."]],
                                    "f350_id_tipo_docto":[factura["Tipo de documento"],factura["Tipo de documento"],factura["Tipo de documento"]],
                                    "f350_consec_docto":[factura["Consecutivo"],factura["Consecutivo"],factura["Consecutivo"]],
                                    "f351_id_auxiliar":["41450501","13551509","23658502"],
                                    "f351_id_tercero":[factura["documento tercero cliente"],factura["documento tercero cliente"],factura["documento tercero cliente"]],
                                    "f351_id_co_mov":[factura["C.O."],factura["C.O."],factura["C.O."]],
                                    "f351_id_un":["UN01","UN08","UN08"],
                                    "f351_id_ccosto":["V219","",""],# IMPORTANTE VALIDAR CENTRO DE COSTO CON KARIME
                                    "f351_id_fe":["","",""],
                                    "f351_valor_db":["0000000000000000.0000",porcentaje_1_1,"0000000000000000.0000"],
                                    "f351_valor_cr":[subtotal,"0000000000000000.0000",porcentaje_1_1],
                                    "f351_valor_db_alt":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_cr_alt":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_base_gravable":["0000000000000000.0000",subtotal,subtotal],
                                    "f351_valor_db2":["0000000000000000.0000",porcentaje_1_1,"0000000000000000.0000"],
                                    "f351_valor_cr2":[subtotal,"0000000000000000.0000",porcentaje_1_1],
                                    "f351_valor_db_alt2":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_cr_alt2":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_base_gravable2":["0000000000000000.0000",subtotal,subtotal],
                                    "f351_valor_db3":["0000000000000000.0000",porcentaje_1_1,"0000000000000000.0000"] ,
                                    "f351_valor_cr3":[subtotal,"0000000000000000.0000",porcentaje_1_1],
                                    "f351_valor_db_alt3":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_cr_alt3":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_base_gravable3":["0000000000000000.0000",subtotal,subtotal],
                                    "f351_valor_imp_asum":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_imp_asum2":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_valor_imp_asum3":["0000000000000000.0000","0000000000000000.0000","0000000000000000.0000"],
                                    "f351_docto_banco":["","",""],
                                    "f351_nro_docto_banco":["00000000","00000000","00000000"],
                                    "f351_nro_alt_docto_banco":["0000000000000000000000000.0000","0000000000000000000000000.0000","0000000000000000000000000.0000"],
                                    "f351_notas":["nota provicional","nota provicional","nota provicional"]
                                    })
                resultado = pd.concat([resultado,df_n], axis=0)
                ultimo_reg_encab=ultimo_reg_encab+3
        
        # Formatear la columna numero de registro con ceros a la izquierda
        resultado['f_numero_reg'] = resultado['f_numero_reg'].astype(str).str.zfill(7)
        
        
        columnas_a_convertir_result = ['f351_valor_db',
                                'f351_valor_cr',
                                'f351_base_gravable',
                                'f351_valor_db2',
                                'f351_valor_cr2',
                                'f351_base_gravable2',
                                'f351_valor_db3',
                                'f351_valor_cr3',
                                'f351_base_gravable3']
        
        # Aplicar la transformación a todas las columnas
        resultado[columnas_a_convertir_result] = resultado[columnas_a_convertir_result].astype(str)
        
        # Convertir la primera fila en nombres de columnas
        transpuesta.columns = transpuesta.iloc[0]  # Asignar la primera fila como encabezados
        transpuesta = transpuesta[1:].reset_index(drop=True)  # Eliminar la primera fila y resetear índices
        
        resultado = pd.concat([transpuesta,resultado ], axis=0)
        
        
        return resultado

    def cartera_plano(safit,ultimo_reg_mov):
        
        ultimo_reg_mov=int(ultimo_reg_mov)
        # Convertir la columna a string y rellenar ceros a la izquierda (3 dígitos)
        safit['SUCURSAL DE FACTURA'] = safit['SUCURSAL DE FACTURA'].astype(str).str.zfill(3)
        # print(safit['SUCURSAL DE FACTURA'])
    # Lista de columnas a convertir
        columnas_a_convertir = [
            'Valor bruto local', 'Valor descuentos local', 'Valor subtotal local',
            'Valor impuestos local', 'Valor neto local', 'Valor impuestos',
            'Valor neto', 'Valor subtotal'
        ]

        # Aplicar la transformación a todas las columnas
        safit[columnas_a_convertir] = safit[columnas_a_convertir].replace('[\$,]', '', regex=True).astype(float)
        # Cargar el archivo JSON en un DataFrame
         # Cargar el archivo JSON en un DataFrame
        current_directory = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.normpath(os.path.join(current_directory, 'data/json_output/cartera.json'))
        conector_enc_df = pd.read_json(ruta)
        transpuesta = conector_enc_df.T
        resultado = pd.DataFrame(columns=["F_NUMERO_REG","F_TIPO_REG","F_SUBTIPO_REG","F_VERSION_REG","F_CIA",
                                            "F350_ID_CO","F350_ID_TIPO_DOCTO","F350_CONSEC_DOCTO","F351_ID_AUXILIAR","F351_ID_TERCERO",
                                            "F351_ID_CO_MOV","F351_ID_UN","F351_ID_CCOSTO","F351_VALOR_DB","F351_VALOR_CR",
                                            "F351_VALOR_DB_ALT","F351_VALOR_CR_ALT","F351_VALOR_DB2","F351_VALOR_CR2","F351_VALOR_DB_ALT2",
                                            "F351_VALOR_CR_ALT2","f351_valor_imp_asum","f351_valor_imp_asum2","F351_NOTAS","F353_ID_SUCURSAL",
                                            "F353_ID_TIPO_DOCTO_CRUCE","F353_CONSEC_DOCTO_CRUCE","F353_NRO_CUOTA_CRUCE","F353_FECHA_VCTO","F353_FECHA_DSCTO_PP",
                                            "F353_VLR_DSCTO_PP","F354_VALOR_APLICADO_PP","F354_VALOR_APLICADO_PP_ALT","F354_VALOR_APROVECHA","F354_VALOR_APROVECHA_ALT",
                                            "F354_VALOR_RETENCION","F354_VALOR_RETENCION_ALT","F354_TERCERO_VEND","F353_FECHA_DOCTO_CRUCE","F353_FECHA_RADICACION",
                                            "F354_NOTAS"
                                        ])
        for idx, factura in safit.iterrows():
            subtotal = factura['Valor subtotal']
            
            # Dar formato de 21 caracteres
            subtotal="{:021.4f}".format(subtotal)
            
            fecha= pd.to_datetime(factura['Fecha'], format="%d/%m/%Y")
            
            fechaVencimiento = (fecha + relativedelta(months=1))
            
            df_j = pd.DataFrame({                               
                                "F_NUMERO_REG":[ultimo_reg_mov+1],
                                "F_TIPO_REG":["0351"],
                                "F_SUBTIPO_REG":["01"],
                                "F_VERSION_REG":["05"],
                                "F_CIA":["004"],
                                "F350_ID_CO":[factura["C.O."]],
                                "F350_ID_TIPO_DOCTO":[factura["Tipo de documento"]],
                                "F350_CONSEC_DOCTO":[factura["Consecutivo"]],
                                "F351_ID_AUXILIAR":["13050501"],
                                "F351_ID_TERCERO":[factura["documento tercero cliente"]],
                                "F351_ID_CO_MOV":[factura["C.O."]],
                                "F351_ID_UN":["UN08"],
                                "F351_ID_CCOSTO":[""],
                                "F351_VALOR_DB":[subtotal],
                                "F351_VALOR_CR":["0000000000000000.0000"],
                                "F351_VALOR_DB_ALT":["+000000000000000.0000"],
                                "F351_VALOR_CR_ALT":["+000000000000000.0000"],
                                "F351_VALOR_DB2":[subtotal],
                                "F351_VALOR_CR2":["0000000000000000.0000"],
                                "F351_VALOR_DB_ALT2":["+000000000000000.0000"],
                                "F351_VALOR_CR_ALT2":["+000000000000000.0000"],
                                "f351_valor_imp_asum":["+000000000000000.0000"],
                                "f351_valor_imp_asum2":["+000000000000000.0000"],
                                "F351_NOTAS":[""],
                                "F353_ID_SUCURSAL":[factura['SUCURSAL DE FACTURA']],
                                "F353_ID_TIPO_DOCTO_CRUCE":[factura['Tipo de documento']],
                                "F353_CONSEC_DOCTO_CRUCE":[factura['Consecutivo']],
                                "F353_NRO_CUOTA_CRUCE":["000"],
                                "F353_FECHA_VCTO":[fecha],
                                "F353_FECHA_DSCTO_PP":[fechaVencimiento],
                                "F353_VLR_DSCTO_PP":["+000000000000000.0000"],
                                "F354_VALOR_APLICADO_PP":["+000000000000000.0000"],
                                "F354_VALOR_APLICADO_PP_ALT":["+000000000000000.0000"],
                                "F354_VALOR_APROVECHA":["+000000000000000.0000"],
                                "F354_VALOR_APROVECHA_ALT":["+000000000000000.0000"],
                                "F354_VALOR_RETENCION":["+000000000000000.0000"],
                                "F354_VALOR_RETENCION_ALT":["+000000000000000.0000"],
                                "F354_TERCERO_VEND":[factura["documento vendedor"]],
                                "F353_FECHA_DOCTO_CRUCE":[fecha],
                                "F353_FECHA_RADICACION":[""],
                                "F354_NOTAS":["Notas provisionales de movimiento de cartera"]
                                })
            resultado = pd.concat([resultado,df_j], axis=0)
            ultimo_reg_mov=ultimo_reg_mov+1
                
        # Formatear la columna numero de registro con ceros a la izquierda
        resultado['F_NUMERO_REG'] = resultado['F_NUMERO_REG'].astype(str).str.zfill(7)
        
        # Formatear la columna numero de registro con ceros a la izquierda
        columnas_a_convertir_result = ['F351_VALOR_DB','F351_VALOR_DB2']
        # Aplicar la transformación a todas las columnas
        resultado[columnas_a_convertir_result] = resultado[columnas_a_convertir_result].astype(str)
        

        # Formatear la fecha como YYYYMMDD
        resultado['F353_FECHA_VCTO'] = resultado['F353_FECHA_VCTO'].dt.strftime("%Y%m%d")
        resultado['F353_FECHA_DSCTO_PP'] = resultado['F353_FECHA_DSCTO_PP'].dt.strftime("%Y%m%d")
        resultado['F353_FECHA_DOCTO_CRUCE'] = resultado['F353_FECHA_DOCTO_CRUCE'].dt.strftime("%Y%m%d")
        
        
        # Convertir la primera fila en nombres de columnas
        transpuesta.columns = transpuesta.iloc[0]  # Asignar la primera fila como encabezados
        transpuesta = transpuesta[1:].reset_index(drop=True)  # Eliminar la primera fila y resetear índices
        
        resultado = pd.concat([transpuesta,resultado ], axis=0)
        
        
        return resultado

    def final_plano(ultimo_reg_cart):
        # Definimos los datos según la imagen
        ultimo_reg_cart=int(ultimo_reg_cart)
        
        data = {
            "F_NUMERO_REG": [ultimo_reg_cart+1],
            "F_TIPO_REG": ["9999"],
            "F_SUBTIPO_REG": ["00"],
            "F_VERSION_REG": ["01"],
            "F_CIA": ["004"]
        }
        
        # Creamos el DataFrame
        df = pd.DataFrame(data)
        df['F_NUMERO_REG'] = df['F_NUMERO_REG'].astype(str).str.zfill(7)
        # Añadimos las filas adicionales
        df = pd.concat([
            pd.DataFrame([["Numérico", "Numérico", "Numérico", "Numérico", "Numérico"]], columns=df.columns),
            pd.DataFrame([[ 7, 4, 2, 2, 3]], columns=df.columns),
            df
        ], ignore_index=True)
        
        # Formatear la columna numero de registro con ceros a la izquierda
        
        
        return df
