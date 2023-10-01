import csv

csv_filename = "data.csv"
fieldnames = ["id", "id_imagen", "nombre_archivo"]


def csv_generate(id_numero_tramite, id_images_tramite, data):
    log_data = []

    try:
        with open(csv_filename, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            log_data = list(reader)

    except FileNotFoundError:
        pass

    log_entry = {
        "id": id_numero_tramite,
        "id_imagen": id_images_tramite,
        "nombre_archivo": data.get('fileName')
    }

    log_data.append(log_entry)

    with open(csv_filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not csv_file.tell():
            writer.writeheader()

        writer.writerows(log_data)
