from __future__ import annotations

from personaje_base import Personaje
from estados import crear_estado


class Arquero(Personaje):
    def __init__(
        self,
        nombre: str,
        tipo: str = "Arquero",
        max_vida: int = 65,
        ataque: int = 12,
        defensa: int = 4,
        vida: int | None = None,
        cooldown_habilidad: int = 0,
        estados=None,
    ) -> None:
        super().__init__(nombre, tipo, max_vida, ataque, defensa, vida, cooldown_habilidad, estados or [])

    def usar_habilidad(self, objetivo: Personaje) -> str:
        if self.cooldown_habilidad > 0:
            return f"{self.nombre} no puede usar Flecha Tóxica. Recarga: {self.cooldown_habilidad} turno(s)."

        self.cooldown_habilidad = 3
        danio = objetivo.recibir_danio(self.ataque_actual() + 4)
        mensaje_estado = objetivo.aplicar_estado(crear_estado("veneno", 3))
        return (
            f"{self.nombre} dispara Flecha Tóxica a {objetivo.nombre} y causa {danio} de daño. "
            f"{mensaje_estado}"
        )
