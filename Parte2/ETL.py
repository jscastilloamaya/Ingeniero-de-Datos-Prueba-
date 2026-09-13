# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 09:58:08 2026

@author: jcast
"""
import pandas as pd
import unicodedata
datoscrudos= pd.read_csv('fechasok.csv')

#%% Correccion de tildes, se quitan
def quitar_tildes(texto):
    if isinstance(texto, str):
        # Primero reparamos el mojibake por si viene corrupto
        try:
            texto = texto.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        
        # Descompone los caracteres con tilde y remueve los acentos (NFD)
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        return texto
    return texto

# 1. Limpiar encabezados de columnas
datoscrudos.columns = [quitar_tildes(col) for col in datoscrudos.columns]

# 2. Limpiar todo el contenido de la tabla
datoscrudos = datoscrudos.map(quitar_tildes)

# %%  Tabla Ciudad
# Asignar el ID unico a cada ciudad
datoscrudos['ID_Ciudad'] =datoscrudos.groupby('ciudad').ngroup() + 1
# Crear la Tabla de Dimension Ciudad
dim_ciudad = datoscrudos[['ID_Ciudad', 'ciudad']].drop_duplicates().reset_index(drop=True)
dim_ciudad.to_csv('dimCiudad.csv', index=False, encoding='latin1')

# %%  Tabla Producto
# Asignar el ID unico a cada tipo producto
datoscrudos['Id_producto'] =datoscrudos.groupby('tipo de producto').ngroup() + 1
# Crear la Tabla de Dimension producto
dim_producto = datoscrudos[['Id_producto', 'tipo de producto']].drop_duplicates().reset_index(drop=True)
dim_producto['tipo de producto'] = dim_producto['tipo de producto'].fillna('Sin Clasificar')

dim_producto = dim_producto.dropna(subset=['tipo de producto'])
dim_producto.to_csv('dimProducto.csv', index=False, encoding='latin1')

# %%  Tabla Tiempo

# Asegurarte de que la columna sea de tipo datetime
datoscrudos['fecha'] = pd.to_datetime(datoscrudos['fecha'])
#La llave
datoscrudos['Id_tiempo'] =datoscrudos.groupby('fecha').ngroup() + 1
# Diccionarios para los nombres 
meses_es = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}
dias_es = {
    0: 'Lunes', 1: 'Martes', 2: 'Miercoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'
}
# Agregar lo nuevos campos
datoscrudos['anno'] = datoscrudos['fecha'].dt.year
datoscrudos['mes'] = datoscrudos['fecha'].dt.month
datoscrudos['dia'] = datoscrudos['fecha'].dt.day
# Trimestre en formato 'Q1', 'Q2'
datoscrudos['trimestre'] = 'Q' + datoscrudos['fecha'].dt.quarter.astype(str)
# Nombres 
datoscrudos['nombre_mes'] = datoscrudos['mes'].map(meses_es)
datoscrudos['dia_semana'] = datoscrudos['fecha'].dt.dayofweek.map(dias_es)

dim_tiempo = datoscrudos[['Id_tiempo','fecha','anno', 'mes', 'dia', 'trimestre', 'nombre_mes', 'dia_semana']].drop_duplicates().reset_index(drop=True)
dim_tiempo.to_csv('dimTiempo.csv', index=False, encoding='latin1')
# %%  Tabla Cliente
#La llave
datoscrudos['Id_cliente'] =datoscrudos.groupby('numero de identificacion').ngroup() + 1
dim_cliente = datoscrudos[['Id_cliente','tipo de identificacion','numero de identificacion','nombres','fecha de nacimiento','direccion del cliente','telefono del cliente','correo del cliente','ID_Ciudad']].drop_duplicates().reset_index(drop=True)
dim_cliente.to_csv('dimCliente.csv', index=False, encoding='latin1')

# %%  Tabla Transacciones
#La llave (En teoria deberia existir uno pero al no tenerlo lo creo yo)
datoscrudos['Id_transaccion'] = datoscrudos.index + 1
fact_transacciones = datoscrudos[['Id_transaccion','Id_cliente','Id_producto','Id_tiempo','tipo transaccion','monto transaccion','numero de cuenta']].drop_duplicates().reset_index(drop=True)
fact_transacciones.to_csv('factTransacciones.csv', index=False, encoding='latin1')


# %%  Tabla Reportes
# Filtrar por el texto exacto 'Si' (o 'SI')
df_filtrado = datoscrudos[datoscrudos['reporte centrales de riesgo'].str.strip().str.upper() == 'SI'].copy()

# Asignar el Id_reporte consecutivo (1, 2, 3...)
df_filtrado = df_filtrado.reset_index(drop=True)
df_filtrado['Id_reporte'] = df_filtrado.index + 1

fact_reporte = df_filtrado[['Id_reporte','Id_cliente','Id_tiempo','reporte centrales de riesgo','monto reporte de central de riesgo','tiempo en mora del reporte de riesgo']].drop_duplicates().reset_index(drop=True)
fact_reporte.to_csv('factReporte.csv', index=False, encoding='latin1')








