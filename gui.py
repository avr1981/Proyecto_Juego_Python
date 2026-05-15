from __future__ import annotations

import copy
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext

from combate import combate
from personajes import crear_personaje, TIPOS_DISPONIBLES, VALORES_DEFECTO
from storage import guardar_personajes, cargar_personajes


def lanzar_gui(personajes):
    root = tk.Tk()
    root.title("Juego de combate por turnos")
    root.geometry("980x640")

    contenedor = ttk.Frame(root, padding=10)
    contenedor.pack(fill=tk.BOTH, expand=True)

    # -------------------- Formulario de creación --------------------
    frame_form = ttk.LabelFrame(contenedor, text="Crear personaje", padding=10)
    frame_form.pack(fill=tk.X)

    ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
    entrada_nombre = ttk.Entry(frame_form, width=24)
    entrada_nombre.grid(row=0, column=1, sticky="w", padx=4, pady=4)

    ttk.Label(frame_form, text="Tipo:").grid(row=0, column=2, sticky="w", padx=4, pady=4)
    combo_tipo = ttk.Combobox(frame_form, values=TIPOS_DISPONIBLES, state="readonly", width=16)
    combo_tipo.set(TIPOS_DISPONIBLES[0])
    combo_tipo.grid(row=0, column=3, sticky="w", padx=4, pady=4)

    ttk.Label(frame_form, text="Vida:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
    entrada_vida = ttk.Entry(frame_form, width=8)
    entrada_vida.grid(row=1, column=1, sticky="w", padx=4, pady=4)

    ttk.Label(frame_form, text="Ataque:").grid(row=1, column=2, sticky="w", padx=4, pady=4)
    entrada_ataque = ttk.Entry(frame_form, width=8)
    entrada_ataque.grid(row=1, column=3, sticky="w", padx=4, pady=4)

    ttk.Label(frame_form, text="Defensa:").grid(row=1, column=4, sticky="w", padx=4, pady=4)
    entrada_defensa = ttk.Entry(frame_form, width=8)
    entrada_defensa.grid(row=1, column=5, sticky="w", padx=4, pady=4)

    def poner_valores_defecto(event=None):
        tipo = combo_tipo.get()
        valores = VALORES_DEFECTO[tipo]
        entrada_vida.delete(0, tk.END)
        entrada_vida.insert(0, str(valores["max_vida"]))
        entrada_ataque.delete(0, tk.END)
        entrada_ataque.insert(0, str(valores["ataque"]))
        entrada_defensa.delete(0, tk.END)
        entrada_defensa.insert(0, str(valores["defensa"]))

    combo_tipo.bind("<<ComboboxSelected>>", poner_valores_defecto)
    poner_valores_defecto()

    # -------------------- Tabla de personajes --------------------
    frame_tabla = ttk.LabelFrame(contenedor, text="Personajes creados", padding=10)
    frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)

    columnas = ("tipo", "nombre", "vida", "ataque", "defensa", "estados")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="extended", height=9)
    tabla.heading("tipo", text="Tipo")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("vida", text="Vida")
    tabla.heading("ataque", text="Ataque")
    tabla.heading("defensa", text="Defensa")
    tabla.heading("estados", text="Estados")

    tabla.column("tipo", width=100, anchor="center")
    tabla.column("nombre", width=150)
    tabla.column("vida", width=100, anchor="center")
    tabla.column("ataque", width=90, anchor="center")
    tabla.column("defensa", width=90, anchor="center")
    tabla.column("estados", width=260)
    tabla.pack(fill=tk.BOTH, expand=True)

    # -------------------- Log de combate --------------------
    frame_log = ttk.LabelFrame(contenedor, text="Registro del combate", padding=10)
    frame_log.pack(fill=tk.BOTH, expand=True)

    texto_log = scrolledtext.ScrolledText(frame_log, height=12, wrap=tk.WORD)
    texto_log.pack(fill=tk.BOTH, expand=True)

    def escribir_log(texto: str):
        texto_log.delete("1.0", tk.END)
        texto_log.insert(tk.END, texto)

    def refrescar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

        for indice, personaje in enumerate(personajes):
            tabla.insert(
                "",
                tk.END,
                iid=str(indice),
                values=(
                    personaje.tipo,
                    personaje.nombre,
                    f"{personaje.vida}/{personaje.max_vida}",
                    personaje.ataque_actual(),
                    personaje.defensa_actual(),
                    personaje.texto_estados(),
                ),
            )

    def leer_entero(campo: ttk.Entry, nombre_campo: str) -> int | None:
        try:
            valor = int(campo.get().strip())
            if valor <= 0:
                raise ValueError
            return valor
        except ValueError:
            messagebox.showerror("Dato no válido", f"El campo {nombre_campo} debe ser un número positivo.")
            return None

    def crear_desde_gui():
        nombre = entrada_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Falta nombre", "Escribe el nombre del personaje.")
            return

        vida = leer_entero(entrada_vida, "vida")
        ataque = leer_entero(entrada_ataque, "ataque")
        defensa = leer_entero(entrada_defensa, "defensa")
        if vida is None or ataque is None or defensa is None:
            return

        personaje = crear_personaje(combo_tipo.get(), nombre, vida, ataque, defensa)
        personajes.append(personaje)
        entrada_nombre.delete(0, tk.END)
        refrescar_tabla()
        escribir_log(f"Personaje creado correctamente:\n{personaje.resumen()}")

    def eliminar_seleccionados():
        seleccion = sorted((int(item) for item in tabla.selection()), reverse=True)
        if not seleccion:
            messagebox.showinfo("Selecciona personaje", "Selecciona al menos un personaje para eliminar.")
            return

        for indice in seleccion:
            personajes.pop(indice)
        refrescar_tabla()
        escribir_log("Personaje(s) eliminado(s).")

    def combatir_seleccionados():
        seleccion = [int(item) for item in tabla.selection()]
        if len(seleccion) != 2:
            messagebox.showinfo("Combate", "Selecciona exactamente 2 personajes en la tabla.")
            return

        p1 = copy.deepcopy(personajes[seleccion[0]])
        p2 = copy.deepcopy(personajes[seleccion[1]])
        log = combate(p1, p2)
        escribir_log("\n".join(log))

    def guardar_desde_gui():
        guardar_personajes(personajes)
        escribir_log("Personajes guardados en personajes.json")
        messagebox.showinfo("Guardado", "Personajes guardados en personajes.json")

    def cargar_desde_gui():
        personajes.clear()
        personajes.extend(cargar_personajes())
        refrescar_tabla()
        escribir_log(f"Se han cargado {len(personajes)} personaje(s) desde personajes.json")

    frame_botones = ttk.Frame(frame_form)
    frame_botones.grid(row=2, column=0, columnspan=6, sticky="w", pady=(8, 0))

    ttk.Button(frame_botones, text="Crear personaje", command=crear_desde_gui).pack(side=tk.LEFT, padx=4)
    ttk.Button(frame_botones, text="Eliminar seleccionado", command=eliminar_seleccionados).pack(side=tk.LEFT, padx=4)
    ttk.Button(frame_botones, text="Combatir seleccionados", command=combatir_seleccionados).pack(side=tk.LEFT, padx=4)
    ttk.Button(frame_botones, text="Guardar JSON", command=guardar_desde_gui).pack(side=tk.LEFT, padx=4)
    ttk.Button(frame_botones, text="Cargar JSON", command=cargar_desde_gui).pack(side=tk.LEFT, padx=4)

    refrescar_tabla()
    escribir_log("Selecciona dos personajes y pulsa 'Combatir seleccionados'.")
    root.mainloop()
