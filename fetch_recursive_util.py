"""
@author: Esteban Petrizzo
Available Functions:\n
- ClearParameters: Function necesaria para setting las variables al estado inicial. \n
- FetchRecursiveFile: Función principal, búsqueda de archivos. \n



"""
from typing import Any
import argparse
import os
import base_64_util
import call_service_rudi_util

LAST_TRAMITE: dict[str, str | list[Any]] = {"directorio": "",
                                            "numeroTramite": "",
                                            "file_id_list": []}

ALTA_RUDI = {"fileName": "",
             "sizeInBase64": "",
             "base64Content": "",
             "isNewTramite": True,
             "lastRequest": {},
             "tramite": "",  # No cambia en toda la ejecución
             "ambiente": ""}  # No cambia en toda la ejecución


def clear_parameters():
    """
    Reset para el nuevo trámite a procesar.

    """
    LAST_TRAMITE.update({"directorio": "",
                         "numeroTramite": "",
                         "file_id_list": []})
    ALTA_RUDI.update({"fileName": "",
                      "sizeInBase64": "",
                      "base64Content": "",
                      "isNewTramite": True,
                      "lastRequest": {}})


def fetch_recursive_file(path, args, **kwargs):
    """

    :param path: Ruta raíz desde donde se comenzara a buscar archivos para el alta de los trámites.
    :param args: Argumentos para el programa, ambiente/comentarios/tipo_tramite/alta_empresas.
    :param kwargs: Cualquier otro campo que se necesite
    """
    path_local = os.scandir(path)
    is_new_tramite = True
    ALTA_RUDI.update(
        {
            "tramite": args.tipo_trm,
            "ambiente": args.ambiente,
            "observation": args.observation,
            "caja": kwargs.get('id_caja', None),
            "directorio": kwargs.get('directorio', None)
        })

    for element in path_local:
        # Caso base - que sea un file - intentamos el alta
        if element.is_file():
            element_encode_base64 = base_64_util.encode_to_base64(path + "/" + element.name)
            file_size = base_64_util.calculate_file_size(element_encode_base64)
            ALTA_RUDI.update({"fileName": element.name,
                              "sizeInBase64": file_size,
                              "base64Content": element_encode_base64,
                              "isNewTramite": is_new_tramite,
                              "lastRequest": LAST_TRAMITE})

            response_service = call_service_rudi_util.call_services_rudi(ALTA_RUDI)
            LAST_TRAMITE.update({"numeroTramite": response_service[0], "file_id_list": response_service[1]})
            # la variable is_new_tramite sera False mientras no se trate de una nueva carpeta
            # hasta que se acaben los archivos en la carpeta actual
            # o si llega a fallar la subida de un archivo
            is_new_tramite = LAST_TRAMITE.get("numeroTramite") == ""

        # Caso recursivo - que sea un dir - estos nos indica que se trata de un nuevo trámite
        elif element.is_dir():

            LAST_TRAMITE.update({"directorio": element.name})
            fetch_recursive_file(path + "/" + element.name, args, id_caja=kwargs.get('id_caja', None),
                                 directorio=kwargs.get('directorio', element.name))

            clear_parameters()
            is_new_tramite = True


def fetch_file(path, args, **kwargs):
    """

    :param path: Ruta raíz desde donde se comenzara a recorrer para intentar subir archivos a RUDI.
    :param args: Argumentos para el programa, ambiente/comentarios/tipo_tramite.
    :param kwargs: Cualquier otro campo que se necesite
    """
    path_local = os.scandir(path)
    is_new_tramite = True
    ALTA_RUDI.update(
        {
            "tramite": args.tipo_trm,
            "ambiente": args.ambiente,
            "observation": args.observation,
            "caja": kwargs.get('id_caja', None),
            "directorio": kwargs.get('directorio', None)
        })

    for element in path_local:
        if element.is_file():
            element_encode_base64 = base_64_util.encode_to_base64(path + "/" + element.name)
            file_size = base_64_util.calculate_file_size(element_encode_base64)
            ALTA_RUDI.update({"fileName": element.name,
                              "sizeInBase64": file_size,
                              "base64Content": element_encode_base64,
                              "isNewTramite": is_new_tramite,
                              "lastRequest": LAST_TRAMITE})

            call_service_rudi_util.call_services_rudi(ALTA_RUDI)
            clear_parameters()


def main():
    parser = argparse.ArgumentParser(description="Fetch recursive files for tramite alta.")
    parser.add_argument("path", type=str, help="Ruta raíz desde donde comenzará la búsqueda de archivos.")
    parser.add_argument("--tipo_trm", type=str, help="Tipo de trámite")
    parser.add_argument("--ambiente", type=str, help="Ambiente")
    parser.add_argument("--observation", type=str, help="Observation")
    parser.add_argument('--dirless', action='store_true', help='Este es un argumento sin valor')
    args = parser.parse_args()

    if args.dirless:
        fetch_file(args.path, args)
    else:
        fetch_recursive_file(args.path, args)


if __name__ == "__main__":
    main()
