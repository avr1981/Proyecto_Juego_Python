from __future__ import annotations

import copy

from personajes import Personaje, crear_personaje, TIPOS_DISPONIBLES, VALORES_DEFECTO
from combate import combate
from storage import guardar_personajes, cargar_personajes


def crear_demo() -> list[Personaje]:
    return [
        crear_personaje("Guerrero", "Tamara"),
        crear_personaje("Mago", "Roberto"),
        crear_personaje("Arquero", "Marta"),
        crear_personaje("Guerrero", "Alejandro", max_vida=82, ataque=12, defensa=8),
    ]


def pedir_entero(texto: str, defecto: int) -> int:
    valor = input(f"{texto} [{defecto}]: ").strip()
    if valor == "":
        return defecto
    try:
        numero = int(valor)
        if numero <= 0:
            print("Debe ser un número positivo. Se usa el valor por defecto.")
            return defecto
        return numero
    except ValueError:
        print("Valor no válido. Se usa el valor por defecto.")
        return defecto


def crear_personaje_menu(personajes: list[Personaje]) -> None:
    print("\nCREAR PERSONAJE")
    for i, tipo in enumerate(TIPOS_DISPONIBLES, 1):
        valores = VALORES_DEFECTO[tipo]
        print(
            f"{i}) {tipo} - vida {valores['max_vida']}, "
            f"ataque {valores['ataque']}, defensa {valores['defensa']}"
        )

    opcion = input("Elige tipo: ").strip()
    try:
        tipo = TIPOS_DISPONIBLES[int(opcion) - 1]
    except (ValueError, IndexError):
        print("Tipo no válido.")
        return

    nombre = input("Nombre del personaje: ").strip()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return

    valores = VALORES_DEFECTO[tipo]
    print("Pulsa ENTER para usar los valores por defecto.")
    max_vida = pedir_entero("Vida máxima", valores["max_vida"])
    ataque = pedir_entero("Ataque", valores["ataque"])
    defensa = pedir_entero("Defensa", valores["defensa"])

    personaje = crear_personaje(tipo, nombre, max_vida=max_vida, ataque=ataque, defensa=defensa)
    personajes.append(personaje)
    print(f"Personaje creado: {personaje.resumen()}")


def listar(personajes: list[Personaje]) -> None:
    print("\nPERSONAJES")
    if not personajes:
        print("No hay personajes creados.")
        return

    for i, personaje in enumerate(personajes, 1):
        print(f"{i}) {personaje.resumen()}")


def elegir_personaje(personajes: list[Personaje], texto: str) -> int | None:
    listar(personajes)
    if not personajes:
        return None

    opcion = input(texto).strip()
    try:
        indice = int(opcion) - 1
        if 0 <= indice < len(personajes):
            return indice
    except ValueError:
        pass

    print("Selección no válida.")
    return None


def combatir_menu(personajes: list[Personaje]) -> None:
    if len(personajes) < 2:
        print("Necesitas al menos 2 personajes para combatir.")
        return

    indice_1 = elegir_personaje(personajes, "Elige el primer personaje: ")
    if indice_1 is None:
        return

    indice_2 = elegir_personaje(personajes, "Elige el segundo personaje: ")
    if indice_2 is None:
        return

    if indice_1 == indice_2:
        print("No puedes enfrentar un personaje contra sí mismo.")
        return

    p1 = copy.deepcopy(personajes[indice_1])
    p2 = copy.deepcopy(personajes[indice_2])
    log = combate(p1, p2)
    print("\n".join(log))


def menu() -> None:
    personajes = crear_demo()

    while True:
        print("\nMENÚ PRINCIPAL")
        print("1) Crear personaje")
        print("2) Listar personajes")
        print("3) Combatir")
        print("4) Guardar personajes en JSON")
        print("5) Cargar personajes desde JSON")
        print("6) Abrir interfaz Tkinter")
        print("7) Reiniciar personajes de demo")
        print("0) Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            crear_personaje_menu(personajes)
        elif opcion == "2":
            listar(personajes)
        elif opcion == "3":
            combatir_menu(personajes)
        elif opcion == "4":
            guardar_personajes(personajes)
            print("Personajes guardados en personajes.json")
        elif opcion == "5":
            personajes = cargar_personajes()
            print(f"Se han cargado {len(personajes)} personaje(s) desde personajes.json")
        elif opcion == "6":
            from gui import lanzar_gui

            lanzar_gui(personajes)
        elif opcion == "7":
            personajes = crear_demo()
            print("Personajes de demo reiniciados.")
        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
