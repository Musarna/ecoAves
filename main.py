import soundfile as sf
from pathlib import Path

def obtener_info_audio(ruta_audio):
    try:
        info = sf.info(str(ruta_audio))
        return {
            "archivo": ruta_audio.name,
            "ruta": str(ruta_audio.resolve()),
            "formato": info.format,
            "subtipo": info.subtype,
            "sample_rate": info.samplerate,
            "canales": info.channels,
            "frames": info.frames,
            "duracion_segundos": round(info.duration, 2)
        }
    except Exception as e:
        return {
            "archivo": ruta_audio.name,
            "error": str(e)
        }

def procesar_carpeta(ruta_carpeta):
    carpeta = Path(ruta_carpeta)

    if not carpeta.exists():
        print(f"Error: la carpeta no existe -> {carpeta}")
        return

    if not carpeta.is_dir():
        print(f"Error: la ruta no es una carpeta -> {carpeta}")
        return

    archivos_wav = list(carpeta.glob("*.wav"))

    if not archivos_wav:
        print("No se encontraron archivos .wav en la carpeta.")
        return

    print(f"Se encontraron {len(archivos_wav)} archivo(s) .wav:\n")

    for archivo in archivos_wav:
        datos = obtener_info_audio(archivo)

        print("=== Información del audio ===")
        print(f"Archivo: {datos.get('archivo')}")

        if "error" in datos:
            print(f"Error al leer el archivo: {datos['error']}")
        else:
            print(f"Ruta completa: {datos['ruta']}")
            print(f"Formato: {datos['formato']}")
            print(f"Subtipo: {datos['subtipo']}")
            print(f"Sample rate: {datos['sample_rate']} Hz")
            print(f"Canales: {datos['canales']}")
            print(f"Frames: {datos['frames']}")
            print(f"Duración: {datos['duracion_segundos']} segundos")

        print()

if __name__ == "__main__":
    ruta_carpeta = input("Ingresa la ruta de la carpeta con audios .wav: ").strip()
    procesar_carpeta(ruta_carpeta)