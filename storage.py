from __future__ import annotations

import json
from pathlib import Path
from typing import List

from personaje_base import Personaje
from factory import personaje_desde_dict

RUTA_DEFECTO = Path("personajes.json")


def guardar_personajes(personajes: List[Personaje], ruta: str | Path = RUTA_DEFECTO) -> None:
    ruta = Path(ruta)
    datos = [personaje.to_dict() for personaje in personajes]
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")


def cargar_personajes(ruta: str | Path = RUTA_DEFECTO) -> List[Personaje]:
    ruta = Path(ruta)
    if not ruta.exists():
        return []

    contenido = ruta.read_text(encoding="utf-8").strip()
    if not contenido:
        return []

    datos = json.loads(contenido)
    return [personaje_desde_dict(item) for item in datos]
