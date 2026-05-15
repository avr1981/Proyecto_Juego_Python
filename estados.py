from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class Estado:
    """Representa un estado alterado activo sobre un personaje."""

    nombre: str
    turnos: int
    danio_por_turno: int = 0
    cura_por_turno: int = 0
    modificador_ataque: int = 0
    modificador_defensa: int = 0
    impide_actuar: bool = False
    descripcion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(datos: Dict[str, Any]) -> "Estado":
        return Estado(**datos)


def crear_estado(nombre: str, turnos: int | None = None) -> Estado:
    """Crea estados predefinidos para usarlos en las habilidades."""

    clave = nombre.strip().lower()

    if clave == "veneno":
        return Estado(
            nombre="Veneno",
            turnos=turnos or 3,
            danio_por_turno=4,
            descripcion="Pierde vida al inicio de su turno.",
        )

    if clave == "quemadura":
        return Estado(
            nombre="Quemadura",
            turnos=turnos or 2,
            danio_por_turno=5,
            modificador_ataque=-2,
            descripcion="Pierde vida y baja su ataque mientras dura.",
        )

    if clave == "sangrado":
        return Estado(
            nombre="Sangrado",
            turnos=turnos or 3,
            danio_por_turno=3,
            descripcion="Daño continuo por heridas abiertas.",
        )

    if clave == "aturdido":
        return Estado(
            nombre="Aturdido",
            turnos=turnos or 1,
            impide_actuar=True,
            descripcion="Pierde la acción de su turno.",
        )

    if clave == "escudo":
        return Estado(
            nombre="Escudo",
            turnos=turnos or 2,
            modificador_defensa=4,
            descripcion="Aumenta la defensa temporalmente.",
        )

    if clave == "regeneracion":
        return Estado(
            nombre="Regeneración",
            turnos=turnos or 2,
            cura_por_turno=4,
            descripcion="Recupera vida al inicio del turno.",
        )

    raise ValueError(f"Estado no reconocido: {nombre}")
