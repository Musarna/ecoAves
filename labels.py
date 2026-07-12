def categorizar_sonido(label: str) -> str:
    label = label.lower()

    etiquetas_ave = [
        "bird",
        "bird vocalization",
        "bird call",
        "bird song",
        "chirp",
        "tweet",
        "pigeon",
        "dove",
        "crow",
        "owl",
        "rooster",
        "duck"
    ]

    etiquetas_otro_animal = [
        "dog",
        "cat",
        "frog",
        "insect",
        "bee",
        "cricket",
        "cow",
        "sheep",
        "goat",
        "horse",
        "pig",
        "animal"
    ]

    etiquetas_anthropico = [
        "speech",
        "conversation",
        "male speech",
        "female speech",
        "vehicle",
        "car",
        "engine",
        "motor",
        "traffic",
        "footsteps",
        "walk",
        "door",
        "music",
        "clap",
        "shout",
        "siren"
    ]

    etiquetas_natural = [
        "wind",
        "rain",
        "water",
        "ocean",
        "waves",
        "thunder",
        "stream",
        "rustling leaves"
    ]

    for etiqueta in etiquetas_ave:
        if etiqueta in label:
            return "Ave"

    for etiqueta in etiquetas_otro_animal:
        if etiqueta in label:
            return "Otro animal"

    for etiqueta in etiquetas_anthropico:
        if etiqueta in label:
            return "Ruido antrópico"

    for etiqueta in etiquetas_natural:
        if etiqueta in label:
            return "Ruido natural"

    return "Otro / no clasificado"