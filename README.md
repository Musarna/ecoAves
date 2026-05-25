# EcoLab

Proyecto piloto de monitoreo acústico orientado al análisis de audio ambiental en humedales de la Región de Coquimbo.

En esta primera etapa, el sistema permite cargar archivos de audio en formato WAV y extraer metadatos básicos como duración, frecuencia de muestreo, número de canales, cantidad de frames y formato.

## Estado del proyecto
Fase inicial de desarrollo del piloto técnico.

Actualmente el sistema:
- recibe un archivo de audio WAV,
- lee sus metadatos básicos,
- y muestra la información por consola.

## Estructura del proyecto
- `main.py`: punto de entrada del programa
- `data/raw/`: audios originales de prueba
- `requirements.txt`: dependencias del proyecto

## Requisitos
- Python 3.10+
- Librerías incluidas en `requirements.txt`

## Instalación
```bash
pip install -r requirements.txt