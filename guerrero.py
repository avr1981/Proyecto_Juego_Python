from __future__ import annotations

from personaje_base import Personaje
from estados import crear_estado


class Guerrero(Personaje):
    def __init__(
        self,
        nombre: str,
        tipo: str = "Guerrero",
        max_vida: int = 80,
        ataque: int = 13,
        defensa: int = 7,
        vida: int | None = None,
        cooldown_habilidad: int = 0,
        estados=None,
    ) -> None:
        super().__init__(nombre, tipo, max_vida, ataque, defensa, vida, cooldown_habilidad, estados or [])

    def usar_habilidad(self, objetivo: Personaje) -> str:
        if self.cooldown_habilidad > 0:
            return f"{self.nombre} no puede usar Golpe Fuerte. Recarga: {self.cooldown_habilidad} turno(s)."

        self.cooldown_habilidad = 3
        danio = objetivo.recibir_danio(self.ataque_actual() + 10)
        mensaje_estado = self.aplicar_estado(crear_estado("escudo", 2))
        return (
            f"{self.nombre} usa Golpe Fuerte contra {objetivo.nombre} y causa {danio} de daño. "
            f"Además se protege. {mensaje_estado}"
        )
