import os
import subprocess

def ejecutar_comando(comando):
    """Ejecuta un comando en la terminal."""
    try:
        resultado = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True)
        print(resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        print(e.stderr)

def iniciar_xml_a_txt():
    """Ejecuta el script xml-a-txt-completo.py y captura la entrada/salida."""
    print("Iniciando xml-a-txt-completo.py...")
    try:
        resultado = subprocess.run(["python3", "xml-a-txt-completo.py"], check=True, capture_output=True, text=True, input=input("Ingrese el nombre del archivo de texto de salida: ") + "\n")
        print(resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar xml-a-txt-completo.py: {e}")
        print(e.stderr)
    print("xml-a-txt-completo.py finalizado.")

def mostrar_ayuda():
    """Muestra la lista de comandos disponibles."""
    print("Comandos disponibles:")
    print("  ayuda: Muestra esta lista de comandos.")
    print("  iniciar: Ejecuta el script xml-a-txt-completo.py.")
    print("  inspeccionar: Detecta archivos .xml y añade sus nombres a nobres-de-los-xml.txt.")
    print("  salir: Termina el programa.")
    print("  [otros comandos]: Ejecuta comandos de la terminal.")

def inspeccionar_xml():
    """Detecta archivos .xml y añade sus nombres a nombres-de-los-xml.txt."""
    ruta = input("Ingrese la ruta para inspeccionar archivos .xml: ")
    try:
        archivos_xml = [archivo for archivo in os.listdir(ruta) if archivo.endswith(".xml")]
        with open("nobres-de-los-xml.txt", "a") as f:  # Nombre del archivo modificado
            for archivo in archivos_xml:
                f.write(archivo + "\n")
        print(f"Se encontraron {len(archivos_xml)} archivos .xml y se añadieron a nobres-de-los-xml.txt.")
    except FileNotFoundError:
        print(f"Error: La ruta '{ruta}' no existe.")

def main():
    print("Bienvenido al transformador de XML a TXT")
    print("Para consultar todos los comandos, ingrese 'ayuda'.")
    while True:
        comando = input("Ingrese un comando (o 'salir' para terminar): ")
        if comando.lower() == "salir":
            break
        elif comando.lower() == "iniciar":
            iniciar_xml_a_txt()
        elif comando.lower() == "ayuda":
            mostrar_ayuda()
        elif comando.lower() == "inspeccionar":
            inspeccionar_xml()
        else:
            ejecutar_comando(comando)

if __name__ == "__main__":
    main()
    
