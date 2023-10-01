"""
@author: Esteban Petrizzo
Available Functions:\n
- EncodeToBase64: LLeva a cabo el encoding de los archivos a Base64. \n
- CalculateFileSize: Calcula el size de los archivos encoded. \n

"""
import base64


def encode_to_base64(file):
    """LLeva a cabo el encode de los archivos a Base64.

    :param file: Archivo a encoding a Base64.
    :return: retorna el str del archivo en Base64.
    """
    with open(file, "rb") as data:
        encoded = base64.b64encode(data.read())
    return encoded.decode('utf-8')


def calculate_file_size(b64string):
    """Calcula el size de los archivos encoded.

    :param b64string: Cadena de string a calcular.
    :return: Retorna un entero resultante del cálculo.
    """
    return int((len(b64string) * 3) / 4 - b64string.count('=', -2))
