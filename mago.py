from __future__ import annotations

from personaje_base import Personaje
from estados import crear_estado


class Mago(Personaje):
    def __init__(
        self,
        nombre: str,
        tipo: str = "Mago",
        max_vida: int = 55,
        ataque: int = 15,
        defensa: int = 3,
        vida: int | None = None,
        cooldown_habilidad: int = 0,
        estados=None,
    ) -> None:
        super().__init__(nombre, tipo, max_vida, ataque, defensa, vida, cooldown_habilidad, estados or [])

    def usar_habilidad(self, objetivo: Personaje) -> str:
        if self.cooldown_habilidad > 0:
            return f"{self.nombre} no puede lanzar Bola de Fuego. Recarga: {self.cooldown_habilidad} turno(s)."

        self.cooldown_habilidad = 4
        danio = objetivo.recibir_danio(self.ataque_actual() + 6)
        mensaje_estado = objetivo.aplicar_estado(crear_estado("quemadura", 2))
        return (
            f"{self.nombre} lanza Bola de Fuego a {objetivo.nombre} y causa {danio} de daño. "
            f"{mensaje_estado}"
        )
