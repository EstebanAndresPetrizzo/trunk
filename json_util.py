import json

json_filename = "data.json"


def json_generate(id_numero_tramite, id_images_tramite, data):
    log_data = []
    try:
        with open(json_filename, "r") as json_file:
            log_data = json.load(json_file)
    except FileNotFoundError:
        pass

    log_entry = {
        "id": id_numero_tramite,
        "id_imagen": id_images_tramite,
        "nombre_archivo": data.get('fileName')
    }
    log_data.append(log_entry)
    with open(json_filename, "w") as json_file:
        json.dump(log_data, json_file, indent=4)
