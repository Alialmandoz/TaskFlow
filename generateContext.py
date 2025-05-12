# generate_context.py
import os
import datetime

# --- Configuración ---
# IMPORTANT: Asegúrate de que project_root_directory sea la ruta correcta
# al directorio raíz de tu proyecto TaskFlow.
# Si guardas este script dentro de esa carpeta, puedes usar os.path.dirname(__file__)
# para obtener la ruta automáticamente, o simplemente '.' si lo ejecutas desde dentro.
# Aquí asumimos la ruta que mencionaste:
project_root_directory = r'D:/trabajo/Propio/IA/programing/TaskFlow' # Usa r'' para rutas de Windows
output_file_name = 'project_structure_and_content.txt'
# --- Fin Configuración ---

output_path = os.path.join(project_root_directory, output_file_name)

print(f"Iniciando recorrido del proyecto en: {project_root_directory}")
print(f"El contenido se guardará en: {output_path}")
print("-" * 40)

try:
    with open(output_path, 'w', encoding='utf-8') as outfile:
        # Escribir una cabecera informativa
        outfile.write(f"--- Contenido completo del proyecto '{os.path.basename(project_root_directory)}' ---\n")
        outfile.write(f"--- Generado el: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n\n")
        outfile.write("=" * 80 + "\n\n")

        # os.walk() genera nombres de directorio dentro de un directorio específico,
        # subdirectorios y nombres de archivo en cada subdirectorio.
        for dirpath, dirnames, filenames in os.walk(project_root_directory):
            # Excluir el directorio del entorno virtual para no incluir sus archivos
            if 'venv' in dirnames:
                dirnames.remove('venv') # Esto evita que os.walk entre en 'venv'

            # Puedes añadir otras carpetas a excluir si lo necesitas, por ejemplo:
            # if '__pycache__' in dirnames:
            #     dirnames.remove('__pycache__')
            # if 'static' in dirnames: # Si tienes muchos archivos estáticos
            #     dirnames.remove('static')
            # if 'media' in dirnames: # Si manejas subidas de usuario
            #    dirnames.remove('media')


            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # Calcular la ruta relativa para que sea más clara en el archivo de salida
                relative_path = os.path.relpath(file_path, project_root_directory)

                # Excluir el propio script y el archivo de salida
                if relative_path == os.path.relpath(__file__, project_root_directory) or \
                   relative_path == output_file_name:
                    continue

                print(f"Procesando: {relative_path}")

                try:
                    # Intentar leer el archivo como texto (UTF-8)
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()

                    # Escribir el nombre del archivo y su contenido en el archivo de salida
                    outfile.write(f"--- START OF FILE {relative_path} ---\n\n")
                    outfile.write(content)
                    outfile.write(f"\n\n--- END OF FILE {relative_path} ---\n\n")
                    outfile.write("=" * 80 + "\n\n") # Separador entre archivos

                except UnicodeDecodeError:
                    # Manejar archivos que no son texto UTF-8 (posiblemente binarios)
                    print(f"  Advertencia: No se pudo leer '{relative_path}' como texto UTF-8. Omitiendo contenido.")
                    outfile.write(f"--- START OF FILE {relative_path} (Binary or Encoding Error) ---\n\n")
                    outfile.write("[Contenido binario o con error de codificación omitido]\n")
                    outfile.write(f"\n\n--- END OF FILE {relative_path} ---\n\n")
                    outfile.write("=" * 80 + "\n\n")
                except Exception as e:
                    # Capturar cualquier otro error durante la lectura del archivo
                    print(f"  Error al procesar '{relative_path}': {e}")
                    outfile.write(f"--- START OF FILE {relative_path} (Error Reading) ---\n\n")
                    outfile.write(f"[Error al leer el archivo: {e}]\n")
                    outfile.write(f"\n\n--- END OF FILE {relative_path} ---\n\n")
                    outfile.write("=" * 80 + "\n\n")


    print(f"\nScript completado. El contenido del proyecto se ha guardado en '{output_file_name}'")

except Exception as e:
    print(f"\nOcurrió un error general durante la ejecución del script: {e}")
    print("Asegúrate de que la ruta 'project_root_directory' sea correcta y tengas permisos de lectura.")