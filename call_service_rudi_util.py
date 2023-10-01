"""
@author: Esteban Petrizzo
Available Functions:\n
- CallServicesRudi: Llamada literal a los servicios de RUDI. \n

"""
from logger_util import configure_logging
from csv_util import csv_generate
from json_util import json_generate
import json
import requests

ok_log, error_log = configure_logging("alta_masiva_rudi")
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}


def call_services_rudi_tipo_tramite(ambiente, tipo_tramite):
    url_tipo_tramite = "http://sgi{}:80/ws.rudi/api/tipos-tramite/{}" \
        .format(ambiente, tipo_tramite)
    try:
        response = requests.get(url_tipo_tramite, headers=headers)
        response.raise_for_status()
        return response.status_code
    except requests.ConnectionError as error:
        error_log.error(error.args[0].reason)
        print(error.args[0].reason)

    except requests.HTTPError as error:
        error_log.error(error)
        print(error)


def get_url_new_tramite(data):
    ambiente = data.get("ambiente")
    if ambiente.lower() == "prod":
        ambiente = ""
    url_new_tramite = "http://sgi{}:80/ws.rudi/api/tramites/".format(ambiente)
    data_new_tramite = ('{"pk": {"tipoTramite": "%s"}, "origen": "PC", "observaciones": "%s",'
                        '"imagenesArchivo": {"items": [{"fileName": "%s", "sizeInBytes": "%s",'
                        '"base64Content": "%s" }]}}' % (data.get("tramite"),
                                                        data.get("observation"),
                                                        data.get("fileName"),
                                                        data.get("sizeInBase64"),
                                                        data.get("base64Content")))

    return url_new_tramite, data_new_tramite


def get_url_existing_tramite(data):
    ambiente = data.get("ambiente")
    if ambiente.lower() == "prod":
        ambiente = ""
    url_existing_tramite = "http://sgi{}:80/ws.rudi/api/tramites/{}/{}/archivos" \
        .format(ambiente,
                data.get("tramite"),
                data.get("lastRequest")
                .get("numeroTramite"))

    data_existing_tramite = ('{"fileName":"%s", "sizeInBytes": "%s", "base64Content": "%s"}'
                             % (data.get("fileName"),
                                data.get("sizeInBase64"),
                                data.get("base64Content")))

    return url_existing_tramite, data_existing_tramite


def call_services_rudi(data):
    """Llamada literal a los servicios de RUDI.
    :param data: {"fileName":"", Nombre del archivo a guardar con el trámite.
                    "sizeInBase64":"", Size del archivo en Base64.
                    "base64Content":"", Archivo encoder en Base64.
                    "isNewTramite": True, Boolean que indica si hacemos un nuevo trámite o añadimos al último creado.
                    "lastRequest": {último trámite creado.
                            "directorio":"", último directorio
                            "numeroTramite":"", id último trámite
                            "file_id_list": []}} lista de archivos de un trámite

    :except: Error en la conexión -- requests.ConnectionError.
    :except: Error en la invocación del servicio -- requests.HTTPError.

    """
    try:
        if data.get("isNewTramite"):
            url_new_tramite, data_new_tramite = get_url_new_tramite(data)
            json_data = json.loads(data_new_tramite)
            response = requests.post(url_new_tramite, json=json_data, headers=headers)
            print(response)
            response.raise_for_status()
            id_images_tramite = response.json().get('imagenesArchivo').get('items')[0].get('pk').get('id')
            id_numero_tramite = response.json().get('pk').get('nroTramite')

            print("--------\nOK NEW TRAMITE {} -- {} \nADD NEW IMAGES -- {}\n--------"
                  .format(data.get("tramite"),
                          id_numero_tramite,
                          id_images_tramite))
            ok_log.info(f"----OK---- {data.get('lastRequest').get('directorio')} / {data.get('fileName')}")

            json_generate(id_numero_tramite, id_images_tramite, data)
            csv_generate(id_numero_tramite, id_images_tramite, data)

            return id_numero_tramite, [id_images_tramite], ""

        else:
            url_existing_tramite, data_existing_tramite = get_url_existing_tramite(data)
            json_data = json.loads(data_existing_tramite)
            response = requests.post(url_existing_tramite, json=json_data, headers=headers)
            response.raise_for_status()
            file_id_list = data.get("lastRequest").get("file_id_list")
            last_id_images = response.json().get('pk').get('id')
            file_id_list.append(last_id_images)
            print("OK EXISTING IMAGES TRAMITE {} -- {}\n--------"
                  .format(data.get("tramite"),
                          last_id_images))

            ok_log.info(f"----OK---- {data.get('lastRequest').get('directorio')} / {data.get('fileName')}")
            json_generate(data.get("lastRequest").get("numeroTramite"), last_id_images, data)
            csv_generate(data.get("lastRequest").get("numeroTramite"), last_id_images, data)
            return data.get("lastRequest").get("numeroTramite"), file_id_list

    except requests.ConnectionError as err:
        error_log.error(f"----ERROR---- {data.get('lastRequest').get('directorio')} / {data.get('fileName')}")
        error_log.error(err.args[0].reason, data)
        print(err.args[0].reason)
        file_id_list = data.get("lastRequest").get("file_id_list")
        file_id_list.append(f"error - {data.get('fileName')}")
        return data.get("lastRequest").get("numeroTramite"), file_id_list

    except requests.HTTPError as err:
        error_log.error(f"----ERROR---- {data.get('lastRequest').get('directorio')} / {data.get('fileName')}")
        error_log.error(err, data)
        print(err)
        file_id_list = data.get("lastRequest").get("file_id_list")
        file_id_list.append(f"error - {data.get('fileName')}")
        return data.get("lastRequest").get("numeroTramite"), file_id_list
