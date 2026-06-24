import warnings
import tkinter as tk
from tkinter import filedialog
from transformers import pipeline

# Suprimir advertencias para mantener la consola limpia
warnings.filterwarnings("ignore")

def detectar_ave(ruta_audio):
    print(f"\nAnalizando el archivo: {ruta_audio}...")
    print("Cargando el modelo...")
    
    # Cargar el pipeline de clasificación de audio
    clasificador = pipeline(
        "audio-classification", 
        model="MIT/ast-finetuned-audioset-10-10-0.4593"
    )
    
    # Realizar la predicción
    predicciones = clasificador(ruta_audio)
    
    # Definir qué etiquetas del modelo consideramos como "Ave"
    etiquetas_ave = [
        "Bird", 
        "Bird vocalization, bird call, bird song", 
        "Chirp, tweet", 
        "Pigeon, dove",
        "Crow",
        "Owl"
    ]
    
    es_ave = False
    confianza_minima = 15.0 # Solo aceptaremos que es un ave si el modelo está más de un 15% seguro
    
    # Mostrar las predicciones
    print("\nTop sonidos detectados:")
    for pred in predicciones:
        score_porcentaje = pred['score'] * 100
        print(f" - {pred['label']}: {score_porcentaje:.2f}%")
        
        # NUEVA LÓGICA: Verificar si es ave Y SI supera nuestra confianza mínima
        for etiqueta in etiquetas_ave:
            if etiqueta.lower() in pred['label'].lower() and score_porcentaje >= confianza_minima:
                es_ave = True
                break

    print("-" * 40)
    # Resultado final
    if es_ave:
        print("🦅 RESULTADO: SÍ es un ave.")
    else:
        print("🚗 RESULTADO: NO es un ave.")
    print("-" * 40 + "\n")

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    
    ruta_seleccionada = filedialog.askopenfilename(
        title="Selecciona un archivo de audio para analizar",
        filetypes=[
            ("Archivos de audio", "*.wav *.mp3"),
            ("Archivos WAV", "*.wav"),
            ("Archivos MP3", "*.mp3"),
            ("Todos los archivos", "*.*")
        ]
    )
    return ruta_seleccionada

if __name__ == "__main__":
    print("Abriendo ventana para seleccionar archivo...")
    archivo = seleccionar_archivo()
    
    if archivo:
        try:
            detectar_ave(archivo)
        except Exception as e:
            print(f"Ocurrió un error al procesar el audio. Detalle: {e}")
    else:
        print("❌ Operación cancelada. No seleccionaste ningún archivo.")