from app_core.models.factura import Factura

class ToolsAndOthers():

        def dfToListFact(df_a_exclusive):
            facturas = []
            
            # Iterar sobre cada fila del DataFrame
            for index, row in df_a_exclusive.iterrows():
                # Crear una nueva instancia de Factura para cada fila
                factura = Factura(
                    compania="004",  # Puedes adaptar este campo según lo que corresponda a "compania"
                    co=row['C.O.'],
                    tipo_documento=row['Tipo de documento'],
                    consecutivo=row['Consecutivo']
                )
                # Agregar la factura a la lista
                facturas.append(factura)
            
            return facturas