from PIL import Image
import os
import argparse

def eliminar_colores(imagen, colores_a_eliminar, tolerancia=30):
    """
    Reemplaza colores específicos en una imagen con transparencia.
    
    Args:
        imagen (PIL.Image): Imagen a procesar
        colores_a_eliminar (list): Lista de colores en formato RGB a eliminar
        tolerancia (int): Margen de tolerancia para la detección de colores
    
    Returns:
        PIL.Image: Imagen procesada con transparencia
    """
    img = imagen.convert("RGBA")
    pixeles = img.load()
    
    ancho, alto = img.size
    for y in range(alto):
        for x in range(ancho):
            r, g, b, a = pixeles[x, y]
            
            # Verificar si el color actual está cerca de los colores objetivo
            for color_obj in colores_a_eliminar:
                r_obj, g_obj, b_obj = color_obj
                if (abs(r - r_obj) <= tolerancia and
                    abs(g - g_obj) <= tolerancia and
                    abs(b - b_obj) <= tolerancia):
                    # Hacer el píxel completamente transparente
                    pixeles[x, y] = (0, 0, 0, 0)
                    break
    
    return img

def procesar_archivos(ruta, tolerancia=30):
    """
    Procesa todos los archivos de imagen en la ruta especificada
    
    Args:
        ruta (str): Ruta del archivo o directorio
        tolerancia (int): Tolerancia para la detección de colores
    """
    colores_a_eliminar = [
        (130, 208, 238),  # #82d0ee
        (137, 229, 204)   # #89e5cc
    ]
    
    if os.path.isfile(ruta):
        archivos = [ruta]
    elif os.path.isdir(ruta):
        archivos = [os.path.join(ruta, f) for f in os.listdir(ruta) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    else:
        raise ValueError("La ruta especificada no es válida")
    
    for archivo in archivos:
        try:
            with Image.open(archivo) as img:
                img_procesada = eliminar_colores(img, colores_a_eliminar, tolerancia)
                
                # Generar nuevo nombre de archivo
                nombre, extension = os.path.splitext(archivo)
                nuevo_nombre = f"{nombre}RM.png"
                
                # Guardar como PNG para mantener transparencia
                img_procesada.save(nuevo_nombre, "PNG")
                print(f"Imagen procesada: {archivo} -> {nuevo_nombre}")
                
        except Exception as e:
            print(f"Error procesando {archivo}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Elimina colores específicos de imágenes y crea fondo transparente')
    parser.add_argument('ruta', help='Ruta del archivo o directorio con imágenes')
    parser.add_argument('-t', '--tolerancia', type=int, default=30,
                        help='Tolerancia para la detección de colores (0-100)')
    
    args = parser.parse_args()
    
    procesar_archivos(args.ruta, args.tolerancia)