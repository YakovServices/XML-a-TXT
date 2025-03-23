import xml.etree.ElementTree as ET
import os

def procesar_cfdis_desde_archivo(nombre_archivo_lista, nombre_archivo_salida):
    """
    Procesa múltiples archivos XML de CFDI cuyos nombres están en un archivo de texto,
    y guarda los resultados en un único archivo de texto.

    Args:
        nombre_archivo_lista (str): Nombre del archivo de texto con la lista de archivos XML.
        nombre_archivo_salida (str): Nombre del archivo de texto de salida.
    """

    try:
        with open(nombre_archivo_lista, 'r', encoding='utf-8') as f:
            nombres_archivos_xml = [line.strip() for line in f]
    except FileNotFoundError:
        print(f'Error: No se encontró el archivo {nombre_archivo_lista}.')
        return

    resultados = []
    sumatorias_rfc = {}
    contador_rfc = {}
    lineas_unicas = []

    for nombre_archivo_xml in nombres_archivos_xml:
        try:
            ruta_archivo_xml = os.path.join(os.getcwd(), nombre_archivo_xml)
            tree = ET.parse(ruta_archivo_xml)
            root = tree.getroot()

            ns = {'cfdi': 'http://www.sat.gob.mx/cfd/4', 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}

            # Extraer datos específicos del CFDI
            rfc_emisor = root.find('cfdi:Emisor', ns).attrib.get('Rfc') or ''
            total = root.attrib.get('Total') or ''
            iva = root.find('cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', ns).attrib.get('Importe') or ''

            # Redondear el total y el IVA usando la regla estándar
            total_redondeado = round(float(total)) if total else 0
            iva_redondeado = round(float(iva)) if iva else 0

            # Crear cadena con formato fijo
            cadena_resultado = f"04|85|{rfc_emisor}|||||||||{total_redondeado}||||||||||{iva_redondeado}||||||||||||||||||||||||||||||||01"

            resultados.append(cadena_resultado)

            # Actualizar sumatorias y contador por RFC
            if rfc_emisor:
                if rfc_emisor not in contador_rfc:
                    contador_rfc[rfc_emisor] = 0
                contador_rfc[rfc_emisor] += 1

                if rfc_emisor not in sumatorias_rfc:
                    sumatorias_rfc[rfc_emisor] = {'total': 0, 'iva': 0}
                sumatorias_rfc[rfc_emisor]['total'] += total_redondeado
                sumatorias_rfc[rfc_emisor]['iva'] += iva_redondeado

        except FileNotFoundError:
            resultados.append(f'Error: El archivo {nombre_archivo_xml} no se encontró.')
        except ET.ParseError:
            resultados.append(f'Error: El archivo {nombre_archivo_xml} no es un CFDI válido.')
        except Exception as e:
            resultados.append(f'Ocurrió un error con {nombre_archivo_xml}: {e}')

    # Agregar líneas de RFCs únicos
    for linea in resultados:
        partes = linea.split('|')
        if len(partes) >= 3: #se agrega validacion a la linea.
            rfc = partes[2]
            if contador_rfc.get(rfc, 0) == 1:
                lineas_unicas.append(linea)

    # Agregar línea de texto antes de las sumatorias
    resultados.append("Sumatorias de proveedores")

    # Agregar sumatorias al final del archivo (solo para RFCs con múltiples apariciones)
    for rfc, sumatorias in sumatorias_rfc.items():
        if contador_rfc[rfc] > 1:
            linea_sumatoria = f"04|85|{rfc}|||||||||{sumatorias['total']}||||||||||{sumatorias['iva']}||||||||||||||||||||||||||||||||01"
            resultados.append(linea_sumatoria)

    # Agregar líneas de RFCs únicos al final
    resultados.extend(lineas_unicas)

    # Guardar todos los resultados en un único archivo de texto
    ruta_archivo_salida = os.path.join(os.getcwd(), nombre_archivo_salida)
    with open(ruta_archivo_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(resultados))

    print(f'Resultados de los CFDI guardados en {nombre_archivo_salida}')

# Ejemplo de uso
nombre_archivo_lista = "nobres-de-los-xml.txt"
nombre_archivo_salida = input('Ingrese el nombre del archivo de texto de salida: ')
procesar_cfdis_desde_archivo(nombre_archivo_lista, nombre_archivo_salida)
