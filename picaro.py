from __future__ import annotations

from personaje_base import Personaje
from estados import crear_estado


class Picaro(Personaje):
    def __init__(
        self,
        nombre: str,
        tipo: str = "Pícaro",
        max_vida: int = 60,
        ataque: int = 14,
        defensa: int = 3,
        vida: int | None = None,
        cooldown_habilidad: int = 0,
        estados=None,
    ) -> None:
        super().__init__(nombre, tipo, max_vida, ataque, defensa, vida, cooldown_habilidad, estados or [])

    def usar_habilidad(self, objetivo: Personaje) -> str:
        if self.cooldown_habilidad > 0:
            return f"{self.nombre} no puede usar Corte Sombrío. Recarga: {self.cooldown_habilidad} turno(s)."

        self.cooldown_habilidad = 3
        danio = objetivo.recibir_danio(self.ataque_actual() + 5)
        mensaje_estado = objetivo.aplicar_estado(crear_estado("sangrado", 3))
        return (
            f"{self.nombre} usa Corte Sombrío contra {objetivo.nombre} y causa {danio} de daño. "
            f"{mensaje_estado}"
        )
