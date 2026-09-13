# %% Configuracion e imports
# Emula el DataStage: estandarizar fechas y cambiar el delimitador.

import os
import re
from datetime import datetime

# Carpeta donde vive este script 
try:
    CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    CARPETA_BASE = os.getcwd()  # respaldo por si __file__ no existe en algun entorno interactivo


DIRECTORIO_A = os.path.join(CARPETA_BASE, "directorioA")
ARCHIVO_ENTRADA = os.path.join(DIRECTORIO_A, "clientes_input.txt")
ARCHIVO_SALIDA = os.path.join(DIRECTORIO_A, "clientes_transformado.txt")

DELIMITADOR_ENTRADA = "|"
DELIMITADOR_SALIDA = ","

# %% Leer el archivo plano crudo
with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
    lineas = [linea.rstrip("\n") for linea in f]
encabezado = lineas[0].split(DELIMITADOR_ENTRADA)

filas = [linea.split(DELIMITADOR_ENTRADA) for linea in lineas[1:] if linea.strip()]

print(f"Encabezado: {encabezado}")
print(f"Total de filas leidas: {len(filas)}")


# %% Funcion de normalizacion de fechas mixtas
def normalizar_fecha(valor: str) -> str:
    """
      YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, DD/MM/YYYY
    a formato estandar YYYY-MM-DD.
    """
    valor = valor.strip()
    partes = re.split(r"[-/]", valor)

    if len(partes) != 3:
        return None  # formato irreconocible, si hay otro formato podemos llamar a otra funcion que lo procese 

    if len(partes[0]) == 4:
        anno, mes, dia = partes
    elif len(partes[2]) == 4:
        anno = partes[2]
        dia, mes = partes[0], partes[1]
    else:
        return None  # ninguna parte parece un anno de 4 digitos

    try:
        fecha = datetime(int(anno), int(mes), int(dia))
        return fecha.strftime("%Y-%m-%d")
    except ValueError:
        return None  # fecha invalida (mes 13, dia 32)

# Prueba de funciona con los formatos que sabemos que existen en el archivo
pruebas = ["1985-03-15", "01/02/2023", "15-04-1990", "2023/03/05"]
for p in pruebas:
    print(f"{p:15} -> {normalizar_fecha(p)}")


# %% Aplicar la normalizacion a todas las filas
idx_fecha_nacimiento = encabezado.index("FechaNacimiento")
idx_fecha_registro = encabezado.index("FechaRegistro")

filas_transformadas = []
filas_con_error = []

for i, fila in enumerate(filas, start=1):
    fecha_nac_normalizada = normalizar_fecha(fila[idx_fecha_nacimiento])
    fecha_reg_normalizada = normalizar_fecha(fila[idx_fecha_registro])

    if fecha_nac_normalizada is None or fecha_reg_normalizada is None:
        filas_con_error.append((i, fila))
        continue  # esta fila se reporta pero no se incluye en la salida

    nueva_fila = fila.copy()
    nueva_fila[idx_fecha_nacimiento] = fecha_nac_normalizada
    nueva_fila[idx_fecha_registro] = fecha_reg_normalizada
    filas_transformadas.append(nueva_fila)

print(f"Filas transformadas correctamente: {len(filas_transformadas)}")
print(f"Filas con error de formato de fecha: {len(filas_con_error)}")


# %% Control de calidad reporte de la transformacion
print("\n--- Log de etapa (equivalente al log de DataStage) ---")
print(f"Filas leidas:    {len(filas)}")
print(f"Filas escritas:  {len(filas_transformadas)}")
print(f"Filas rechazadas: {len(filas_con_error)}")

if filas_con_error:
    print("\nDetalle de filas rechazadas:")
    for num_fila, fila in filas_con_error:
        print(f"  Fila {num_fila}: {fila}")


# %% Generar el archivo de salida transformado (delimitador coma)
with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
    f.write(DELIMITADOR_SALIDA.join(encabezado) + "\n")
    for fila in filas_transformadas:
        f.write(DELIMITADOR_SALIDA.join(fila) + "\n")

print(f"\nArchivo de salida generado en: {ARCHIVO_SALIDA}")


# %% Configuracion de Control-M 
import shutil
import time
from datetime import datetime as dt

DIRECTORIO_B = os.path.join(CARPETA_BASE, "directorioB")
NOMBRE_ARCHIVO_TRANSFORMADO = "clientes_transformado.txt"

MAX_REINTENTOS = 3
ESPERA_ENTRE_REINTENTOS_SEG = 5
ZONA_HORARIA = "America/Bogota"

LOG_EJECUCION = os.path.join(CARPETA_BASE, "control_m_log.txt")


def registrar_log(mensaje: str) -> None:
    """Escribe en consola y en un archivo de log (equivalente al historial de runs de Control-M)."""
    timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] {mensaje}"
    print(linea)
    with open(LOG_EJECUCION, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


# %% Funcion de alerta ante fallo
def enviar_alerta(mensaje_error: str) -> None:

    registrar_log(f"ALERTA: {mensaje_error}")


# %% Mover el archivo transformado de A a B, con reintentos y validaciones
def job_mover_archivo() -> bool:
    origen = os.path.join(DIRECTORIO_A, NOMBRE_ARCHIVO_TRANSFORMADO)
    destino = os.path.join(DIRECTORIO_B, NOMBRE_ARCHIVO_TRANSFORMADO)

    registrar_log(f"Iniciando job: mover archivo de '{origen}' a '{destino}'")

    intento = 0
    while intento < MAX_REINTENTOS:
        intento += 1
        try:
            # Validacion de completitud/existencia (bandera/semforo)
            if not os.path.exists(origen):
                raise FileNotFoundError(f"No existe el archivo de origen: {origen}")

            tamano_esperado = os.path.getsize(origen)
            if tamano_esperado == 0:
                raise ValueError("El archivo de origen esta vacio")

            os.makedirs(DIRECTORIO_B, exist_ok=True)# Por si no existe el destino lo creamos, tambien podriamos generar una alerta
            shutil.move(origen, destino)

            # Validacion de tamano esperado despues de mover (check)
            tamano_movido = os.path.getsize(destino)
            if tamano_movido != tamano_esperado:
                raise IOError("El tamanno del archivo movido no coincide con el original")

            registrar_log(
                f"Job exitoso en el intento {intento}. "
                f"Archivo movido correctamente ({tamano_movido} bytes)."
            )
            return True

        except Exception as e:
            registrar_log(f"Intento {intento}/{MAX_REINTENTOS} fallido: {e}")
            if intento < MAX_REINTENTOS:
                time.sleep(ESPERA_ENTRE_REINTENTOS_SEG)
            else:
                enviar_alerta(f"El job falla despues de {MAX_REINTENTOS} intentos. ultimo error: {e}")
                return False


# %% Programación tipo Control-M Lunes a Viernes 08:00 America/Bogota
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = BlockingScheduler(timezone=ZONA_HORARIA)
scheduler.add_job(
    job_mover_archivo,
    trigger=CronTrigger(day_of_week="mon-fri", hour=8, minute=0, timezone=ZONA_HORARIA),
    id="mover_clientes_transformado",
    name="Mover archivo transformado de directorioA a directorioB",
)


# %% Ejecutar el scheduler (bloquea el proceso, como un demonio de Control-M corriendo de fondo)

##Prueba de funcionamiento sin disparador
resultado = job_mover_archivo()   # descomenta esta línea para hacer una prueba inmediata
print(f"\n¿Job exitoso? {resultado}")#Eliminar
#registrar_log(f"Scheduler iniciado. Proxima ejecucion programada L-V 08:00 ({ZONA_HORARIA}).")
#scheduler.start()
