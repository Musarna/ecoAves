import json
import warnings
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from labels import categorizar_sonido

import soundfile as sf
from transformers import pipeline

warnings.filterwarnings("ignore")

ETIQUETAS_AVE = [
    "Bird",
    "Bird vocalization, bird call, bird song",
    "Chirp, tweet",
    "Pigeon, dove",
    "Crow",
    "Owl"
]

CONFIANZA_MINIMA = 15.0


def seleccionar_archivo() -> str:
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


def obtener_info_audio(ruta_audio: Path) -> dict:
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
            "ruta": str(ruta_audio.resolve()),
            "error": str(e)
        }


def detectar_ave(ruta_audio: Path, clasificador) -> dict:
    audio, sample_rate = sf.read(str(ruta_audio))

    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    predicciones = clasificador({
        "array": audio,
        "sampling_rate": sample_rate
    })

    resultados = []
    porcentaje_total_aves = 0.0

    for pred in predicciones:
        score_porcentaje = round(pred["score"] * 100, 2)
        label = pred["label"]

        categoria = categorizar_sonido(label)

        resultados.append({
            "label_original": label,
            "categoria": categoria,
            "score_porcentaje": score_porcentaje
        })

        if categoria == "Ave":
            porcentaje_total_aves += score_porcentaje

    es_ave = porcentaje_total_aves >= CONFIANZA_MINIMA

    return {
        "es_ave": es_ave,
        "confianza_minima_usada": CONFIANZA_MINIMA,
        "porcentaje_total_aves": round(porcentaje_total_aves, 2),
        "predicciones": resultados
    }


def guardar_resultado_json(resultado: dict, carpeta_salida: Path) -> Path:
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    nombre_base = Path(resultado["info_audio"]["archivo"]).stem
    ruta_salida = carpeta_salida / f"{nombre_base}_resultado.json"

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    return ruta_salida


def mostrar_resultado(resultado: dict) -> None:
    info_audio = resultado["info_audio"]
    clasificacion = resultado["clasificacion"]

    print("\n" + "=" * 50)
    print("RESULTADO DEL ANÁLISIS")
    print("=" * 50)

    print("\n[Información del audio]")
    print(f"Archivo: {info_audio['archivo']}")
    print(f"Duración: {info_audio['duracion_segundos']} s")
    print(f"Sample rate: {info_audio['sample_rate']} Hz")
    print(f"Canales: {info_audio['canales']}")

    print("\n[Resumen]")
    print(f"Porcentaje total de aves detectado: {clasificacion['porcentaje_total_aves']:.2f}%")

    print("\n[Resultado final]")
    if clasificacion["es_ave"]:
        print("SÍ se detectó presencia probable de ave.")
    else:
        print("NO se detectó presencia probable de ave.")

    print("=" * 50 + "\n")


def main() -> None:
    print("Cargando modelo de clasificación...")
    clasificador = pipeline(
        "audio-classification",
        model="MIT/ast-finetuned-audioset-10-10-0.4593"
    )

    print("Abriendo ventana para seleccionar archivo...")
    ruta_archivo = seleccionar_archivo()

    if not ruta_archivo:
        print("Operación cancelada. No seleccionaste ningún archivo.")
        return

    ruta_audio = Path(ruta_archivo)

    try:
        info_audio = obtener_info_audio(ruta_audio)

        if "error" in info_audio:
            print(f"Error al leer el audio: {info_audio['error']}")
            return

        clasificacion = detectar_ave(ruta_audio, clasificador)

        resultado = {
            "info_audio": info_audio,
            "clasificacion": clasificacion
        }

        mostrar_resultado(resultado)

        carpeta_salida = Path("resultados")
        ruta_guardado = guardar_resultado_json(resultado, carpeta_salida)
        print(f"Resultado guardado en: {ruta_guardado.resolve()}")

    except Exception as e:
        print(f"Ocurrió un error al procesar el audio. Detalle: {e}")


if __name__ == "__main__":
    main()