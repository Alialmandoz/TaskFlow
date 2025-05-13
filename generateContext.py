# generate_context.py
import os
import datetime
import re

# --- Configuración ---
project_root_directory = r'D:/trabajo/Propio/IA/programing/TaskFlow'
output_file_basename = 'project_structure_and_content_tree.md'
# --- Fin Configuración ---

output_path_absolute = os.path.abspath(os.path.join(project_root_directory, output_file_basename))

try:
    generator_script_absolute_path = os.path.abspath(__file__)
except NameError:
    import sys
    if sys.argv[0] and os.path.exists(sys.argv[0]):
        generator_script_absolute_path = os.path.abspath(sys.argv[0])
    else:
        generator_script_absolute_path = None
    if generator_script_absolute_path: # Solo imprimir si se pudo determinar
        print(f"Advertencia: No se pudo determinar la ruta del script generador vía __file__. Usando: {generator_script_absolute_path}")
    else:
        print("Advertencia: No se pudo determinar la ruta del script generador.")


FILES_TO_EXCLUDE_BY_BASENAME = [
    '.env', 'db.sqlite3', 'db.sqlite3-journal',
    'update_templates.py', 'update_dynamic_dom.py', 'Documento de Proyecto TaskFlow .txt',
    'system_prompt.txt', '.gitignore',
    # Excluir también el archivo de salida anterior si existe
    'project_structure_and_content_markdown.md',
    'project_structure_and_content_optimized.txt',
]

DIRS_TO_EXCLUDE = [
    'venv', 'env', 'ENV', '.venv', 'node_modules',
    '.git', '__pycache__', '.vscode', '.idea',
]

SENSITIVE_PATTERNS = [
    (re.compile(r"""
        ( \b(?:API_KEY|SECRET_KEY|ACCESS_KEY|CLIENT_SECRET|PASSWORD|TOKEN|AUTH_TOKEN|SESSION_KEY|DB_PASSWORD|DATABASE_URL)\b \s*[:=]\s* (['"]) )
        (.*?) (\2)
        """, re.IGNORECASE | re.VERBOSE),
     r"\1[REDACTED_CREDENTIAL]\4"),
    (re.compile(r"(AIzaSy[A-Za-z0-9\-_]{33})"), r"[REDACTED_GOOGLE_API_KEY]"),
    (re.compile(r"""(\w+:\/\/\w+:)(.*?)@"""),  r"\1[REDACTED_PASSWORD]@"),
]

omitted_files_paths = []
file_paths_for_tree = [] # Cambiado el nombre para claridad

print(f"Iniciando recorrido del proyecto en: {project_root_directory}")
print(f"El contenido se guardará en: {output_path_absolute}")
print("-" * 40)

def get_language_for_extension(filename):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext == '.py': return 'python'
    if ext == '.js': return 'javascript'
    if ext == '.html': return 'html'
    if ext == '.css': return 'css'
    if ext == '.json': return 'json'
    if ext == '.yaml' or ext == '.yml': return 'yaml'
    if ext == '.xml': return 'xml'
    if ext == '.md': return 'markdown'
    if ext == '.txt': return 'text'
    return ''

def redact_sensitive_info(content):
    redacted_content = content
    for pattern, replacement in SENSITIVE_PATTERNS:
        redacted_content = pattern.sub(replacement, redacted_content)
    return redacted_content

def generate_tree_structure_markdown(file_paths, root_display_name="."):
    """Genera una representación de árbol en formato Markdown."""
    tree_lines = ["```text", root_display_name] # Iniciar bloque de código y añadir nombre raíz
    
    # Construir una estructura jerárquica a partir de las rutas de archivo
    path_map = {}
    for p in sorted(file_paths):
        parts = p.split('/') # Asumimos rutas normalizadas con '/'
        current_level = path_map
        for i, part in enumerate(parts):
            is_last_part = (i == len(parts) - 1)
            # Si es la última parte, es un archivo. Si no, es un directorio.
            # Para el árbol, tratamos todo como nodos que pueden o no tener hijos.
            if part not in current_level:
                current_level[part] = {} # Crear un nuevo nodo (puede ser archivo o dir)
            current_level = current_level[part]

    def build_lines_recursive(current_level_map, prefix=""):
        entries = sorted(current_level_map.keys())
        for i, entry_name in enumerate(entries):
            is_last_entry_in_level = (i == len(entries) - 1)
            connector = "└── " if is_last_entry_in_level else "├── "
            tree_lines.append(f"{prefix}{connector}{entry_name}")
            
            # Si este 'entry_name' tiene un diccionario no vacío como valor, es un directorio.
            if isinstance(current_level_map[entry_name], dict) and current_level_map[entry_name]:
                new_prefix = prefix + ("    " if is_last_entry_in_level else "│   ")
                build_lines_recursive(current_level_map[entry_name], new_prefix)
    
    build_lines_recursive(path_map)
    tree_lines.append("```")
    return "\n".join(tree_lines)

try:
    # --- Primera pasada: Recopilar rutas de archivos que se procesarán ---
    print("Recopilando estructura de archivos...")
    for dirpath, dirnames, filenames in os.walk(project_root_directory, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in DIRS_TO_EXCLUDE and not d.endswith('.egg-info')]
        
        for filename in filenames:
            file_path_current_iteration = os.path.abspath(os.path.join(dirpath, filename))
            is_excluded = False
            if generator_script_absolute_path and os.path.samefile(file_path_current_iteration, generator_script_absolute_path):
                is_excluded = True
            # Comparamos el nombre base del archivo de salida con el nombre base del archivo actual.
            # Esto asegura que si el script se ejecuta desde un dir diferente a project_root_directory,
            # y output_file_basename es solo un nombre de archivo, aún se excluya correctamente si está en la raíz.
            if os.path.basename(file_path_current_iteration) == output_file_basename:
                 is_excluded = True
            if os.path.basename(filename) in FILES_TO_EXCLUDE_BY_BASENAME:
                is_excluded = True
            
            if not is_excluded:
                relative_file_path = os.path.relpath(file_path_current_iteration, project_root_directory)
                file_paths_for_tree.append(relative_file_path.replace(os.sep, '/')) # Normalizar separadores

    file_paths_for_tree = sorted(list(set(file_paths_for_tree))) # Únicos y ordenados

    # --- Escribir el archivo de salida ---
    with open(output_path_absolute, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# Contenido del Proyecto: {os.path.basename(project_root_directory)}\n\n")
        outfile.write(f"**Generado el:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        outfile.write("## Estructura del Proyecto\n\n")
        if file_paths_for_tree: # Solo generar árbol si hay archivos
            tree_representation = generate_tree_structure_markdown(file_paths_for_tree, os.path.basename(project_root_directory))
            outfile.write(tree_representation)
        else:
            outfile.write("```text\n(No se encontraron archivos para mostrar en la estructura después de las exclusiones)\n```")
        outfile.write("\n\n---\n\n")

        print("\nEscribiendo contenido de archivos...")
        # Iterar sobre las rutas de archivo ya filtradas y ordenadas para la consistencia
        for relative_path_normalized in file_paths_for_tree:
            # Convertir la ruta normalizada de vuelta a la específica del OS para abrir el archivo
            file_path_os_specific = os.path.join(project_root_directory, relative_path_normalized.replace('/', os.sep))
            filename_base = os.path.basename(relative_path_normalized) # Solo para get_language_for_extension

            print(f"Procesando contenido de: {relative_path_normalized}")
            outfile.write(f"## Archivo: `{relative_path_normalized}`\n\n")

            try:
                with open(file_path_os_specific, 'r', encoding='utf-8', errors='strict') as infile:
                    content = infile.read()
                redacted_content = redact_sensitive_info(content)
                language = get_language_for_extension(filename_base) # Usar filename_base aquí
                outfile.write(f"```{language}\n{redacted_content}\n```\n\n")
                outfile.write("---\n\n")
            except (UnicodeDecodeError, IOError, OSError) as e:
                omitted_files_paths.append(relative_path_normalized) # Usar la ruta normalizada
                print(f"  ADVERTENCIA: Omitiendo contenido de '{relative_path_normalized}' ({type(e).__name__})")
                outfile.write(f"```text\n[Contenido de '{relative_path_normalized}' omitido (Binario, error de codificación/lectura)]\n```\n\n")
                outfile.write("---\n\n")
            except Exception as e:
                omitted_files_paths.append(f"{relative_path_normalized} (Error inesperado: {type(e).__name__})")
                print(f"  Error inesperado al procesar '{relative_path_normalized}': {e}")
                outfile.write(f"```text\n[Error inesperado al procesar '{relative_path_normalized}': {e}]\n```\n\n")
                outfile.write("---\n\n")

        if omitted_files_paths:
            outfile.write("## Lista de Archivos con Contenido Omitido\n\n")
            outfile.write("*(Binarios, errores de codificación/lectura, o errores inesperados durante el procesamiento)*\n\n")
            unique_omitted_paths = sorted(list(set(omitted_files_paths)))
            for omitted_path in unique_omitted_paths:
                outfile.write(f"- `{omitted_path}`\n")
            outfile.write("\n\n")

    print(f"\nScript completado. El contenido del proyecto se ha guardado en '{output_file_basename}' (Formato Markdown con árbol de estructura)")

except Exception as e:
    print(f"\nOcurrió un error general durante la ejecución del script: {e}")