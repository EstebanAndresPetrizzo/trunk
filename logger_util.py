import logging as log
from datetime import datetime


def configure_logging(log_file_prefix):
    # Obtén la fecha y hora actual
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Nombre de los archivos de registro con fecha y hora
    ok_log_filename = f"{log_file_prefix}_ok_log_{formatted_datetime}.log"
    error_log_filename = f"{log_file_prefix}_error_log_{formatted_datetime}.log"

    # Configuración de los archivos de registro
    ok_log = log.getLogger("ok_log")
    error_log = log.getLogger("error_log")

    # Configuración de nivel de registro para cada archivo
    ok_log.setLevel(log.INFO)
    error_log.setLevel(log.ERROR)

    # Crear manejadores de archivo para los archivos de registro
    ok_log_handler = log.FileHandler(ok_log_filename)
    error_log_handler = log.FileHandler(error_log_filename)

    # Crear formateadores para los registros
    log_format = log.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ok_log_handler.setFormatter(log_format)
    error_log_handler.setFormatter(log_format)

    # Asignar manejadores a los archivos de registro
    ok_log.addHandler(ok_log_handler)
    error_log.addHandler(error_log_handler)

    return ok_log, error_log
