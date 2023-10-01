# Nombre del Proyecto
Alta Masiva RUDI

## Descripción
Este proyecto es una aplicación de Python que genera trámites en RUDI de un tipo de trámite y en un ambiente dado, 
recorriendo de forma recursiva el directorio especificado en los parámetros . Es útil para subir de forma controlada
y ordenada documentacion que no vaya por el flujo normal de la aplicación de SGI.

## Instrucciones
1. Para compilar este código usamos pyinstaller <br>
    sino esta istalado se puede instalar de esta manera:
    pip install pyinstaller<br><br>

2. Luego en la consola ejecutar el siguiente comando:<br>
    pyinstaller --name {NAME} --paths {PATH} --onefile fetch_recursive_util.py<br>
    <br>ejemplo:
     pyinstaller --name Alta_masiva_RUDI --paths C:/Users/espetrizzo/PycharmProjects/FCDP/alta_masiva --onefile fetch_recursive_util.py
    <br><br>el "--name" sera el nombre del ejecutable
    <br>el "--paths" sera la ubicacion donde tenga el fuente
    <br>el "--onefile" es la configuracion necesaria para que quede en un ejecutable
    mas informacion en https://pyinstaller.org/en/stable/ -> 2023-09<br><br>

3. Una vez terminada la compilacion, el archivo .exe quedará en un subdirectorio "dist"
    para ejecutar el programa compilado abrir el cmd y usar este comando:<br>
    Alta_masiva_RUDI.exe ./archivos  --tipo_trm "{TIPO TRAMITE}" --ambiente "{AMBIENTE}" --observation "Prueba"
    <br><br>ejemplo:<br>
    <strong>Alta_masiva_RUDI.exe ./archivos  --tipo_trm "TSTX" --ambiente "QA" --observation "Prueba"<br><br></strong>

   Otro uso que se puede dar, es que en vez de recorrer todas la carpetar del directorio dado por parámetro (raiz),
   solo intente subir los archivo del directorio raiz; para eso indicamos el comportamiento con agregando el argumento <strong>"dirless"</strong>
   <br><br>ejemplo:<br>
   <strong>Alta_masiva_RUDI.exe ./archivos  --tipo_trm "TSTX" --ambiente "QA" --observation "Prueba" --dirless<br><br></strong>
4. Para correr el programa desde el fuente ejecutar el siguiente comando:
    python .\alta_masiva\fetch_recursive_util.py .\alta_masiva\archivos\ --tipo_trm "TSTX" --ambiente "QA" --observation "Prueba"


## Créditos
- Autor: Esteban Petrizzo
