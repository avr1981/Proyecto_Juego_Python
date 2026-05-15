from __future__ import annotations

from typing import Any, Dict, Type

from personaje_base import Personaje
from guerrero import Guerrero
from mago import Mago
from arquero import Arquero
from picaro import Picaro
from clerigo import Clerigo
from estados import Estado


CLASES_PERSONAJE: Dict[str, Type[Personaje]] = {
    "guerrero": Guerrero,
    "mago": Mago,
    "arquero": Arquero,
    "pícaro": Picaro,
    "picaro": Picaro,
    "clérigo": Clerigo,
    "clerigo": Clerigo,
}

TIPOS_DISPONIBLES = ["Guerrero", "Mago", "Arquero", "Pícaro", "Clérigo"]

VALORES_DEFECTO = {
    "Guerrero": {"max_vida": 80, "ataque": 13, "defensa": 7},
    "Mago": {"max_vida": 55, "ataque": 15, "defensa": 3},
    "Arquero": {"max_vida": 65, "ataque": 12, "defensa": 4},
    "Pícaro": {"max_vida": 60, "ataque": 14, "defensa": 3},
    "Clérigo": {"max_vida": 70, "ataque": 9, "defensa": 5},
}


def normalizar_tipo(tipo: str) -> str:
    tipo = tipo.strip()
    for tipo_oficial in TIPOS_DISPONIBLES:
        if tipo_oficial.lower().replace("é", "e").replace("í", "i") == tipo.lower().replace("é", "e").replace("í", "i"):
            return tipo_oficial
    raise ValueError(f"Tipo de personaje no válido: {tipo}")


def crear_personaje(
    tipo: str,
    nombre: str,
    max_vida: int | None = None,
    ataque: int | None = None,
    defensa: int | None = None,
) -> Personaje:
    tipo_oficial = normalizar_tipo(tipo)
    valores = VALORES_DEFECTO[tipo_oficial]
    cls = CLASES_PERSONAJE[tipo_oficial.lower().replace("é", "e").replace("í", "i")]

    return cls(
        nombre=nombre.strip(),
        max_vida=max_vida or valores["max_vida"],
        ataque=ataque or valores["ataque"],
        defensa=defensa or valores["defensa"],
    )


def personaje_desde_dict(datos: Dict[str, Any]) -> Personaje:
    datos = datos.copy()
    tipo = normalizar_tipo(datos.get("tipo", "Guerrero"))

    # Compatibilidad con el modelo antiguo: estado + estado_turnos.
    estados = []
    if "estados" in datos and isinstance(datos["estados"], list):
        estados = [Estado.from_dict(estado) for estado in datos["estados"]]
    elif datos.get("estado"):
        from estados import crear_estado

        estados = [crear_estado(str(datos["estado"]), int(datos.get("estado_turnos", 1)))]

    cls = CLASES_PERSONAJE[tipo.lower().replace("é", "e").replace("í", "i")]
    return cls(
        nombre=datos.get("nombre", "Sin nombre"),
        max_vida=int(datos.get("max_vida", VALORES_DEFECTO[tipo]["max_vida"])),
        ataque=int(datos.get("ataque", VALORES_DEFECTO[tipo]["ataque"])),
        defensa=int(datos.get("defensa", VALORES_DEFECTO[tipo]["defensa"])),
        vida=int(datos.get("vida", datos.get("max_vida", VALORES_DEFECTO[tipo]["max_vida"]))),
        cooldown_habilidad=int(datos.get("cooldown_habilidad", 0)),
        estados=estados,
    )
