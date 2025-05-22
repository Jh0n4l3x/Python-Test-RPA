import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import requests
from io import BytesIO

# Crear base de datos con usuario de prueba
def crear_db():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    username TEXT,
                    password TEXT
                )''')
    c.execute("SELECT * FROM usuarios WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO usuarios VALUES ('admin', '1234')")
    conn.commit()
    conn.close()

# Validar credenciales
def validar_login():
    usuario = entry_usuario.get()
    clave = entry_clave.get()
    
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (usuario, clave))
    resultado = c.fetchone()
    conn.close()

    if resultado:
        mostrar_vista_api()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Mostrar detalles en ventana emergente
def mostrar_detalles_personaje(url):
    try:
        response = requests.get(url)
        data = response.json()

        detalle = tk.Toplevel(ventana)
        detalle.title(data["name"])
        detalle.geometry("400x500")
        detalle.configure(bg="#f9f9f9")

        # Imagen
        img_data = requests.get(data["image"]).content
        img = Image.open(BytesIO(img_data)).resize((150, 150))
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(detalle, image=img_tk, bg="#f9f9f9")
        img_label.image = img_tk
        img_label.pack(pady=10)

        # Texto
        info = [
            f"Nombre: {data['name']}",
            f"Estado: {data['status']}",
            f"Especie: {data['species']}",
            f"Género: {data['gender']}",
            f"Origen: {data['origin']['name']}",
            f"Ubicación actual: {data['location']['name']}",
            f"Apariciones en episodios: {len(data['episode'])}"
        ]

        for line in info:
            tk.Label(detalle, text=line, bg="#f9f9f9", font=("Helvetica", 12)).pack(pady=2)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los detalles:\n{e}")

# Vista principal con grid
def mostrar_vista_api():
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.geometry("850x600")
    ventana.configure(bg="#f0f4f7")

    tk.Label(ventana, text="Rick and Morty - Personajes", font=("Helvetica", 24, "bold"), bg="#f0f4f7", fg="#2d2d2d").pack(pady=20)

    try:
        response = requests.get("https://rickandmortyapi.com/api/character")
        data = response.json()["results"][:6]  # 6 para grid 2 filas de 3

        grid_frame = tk.Frame(ventana, bg="#f0f4f7")
        grid_frame.pack()

        for index, pers in enumerate(data):
            img_url = pers['image']
            img_data = requests.get(img_url).content
            img = Image.open(BytesIO(img_data)).resize((120, 120))
            img_tk = ImageTk.PhotoImage(img)

            card = tk.Frame(grid_frame, bg="#ffffff", padx=10, pady=10, relief="raised", bd=1)
            row = index // 3
            col = index % 3
            card.grid(row=row, column=col, padx=15, pady=15)

            # Imagen clickeable
            img_label = tk.Label(card, image=img_tk, bg="#ffffff", cursor="hand2")
            img_label.image = img_tk
            img_label.pack()
            img_label.bind("<Button-1>", lambda e, url=pers["url"]: mostrar_detalles_personaje(url))

            # Nombre clickeable
            name_lbl = tk.Label(card, text=pers['name'], font=("Helvetica", 12, "bold"), bg="#ffffff", cursor="hand2", fg="#2a74db")
            name_lbl.pack(pady=(8, 2))
            name_lbl.bind("<Button-1>", lambda e, url=pers["url"]: mostrar_detalles_personaje(url))

            tk.Label(card, text=f"{pers['species']} - {pers['status']}", font=("Helvetica", 10), bg="#ffffff", fg="#444").pack()

    except Exception as e:
        tk.Label(ventana, text=f"Error al conectar con la API: {e}", fg="red").pack()

# Interfaz principal (login)
crear_db()
ventana = tk.Tk()
ventana.title("Login - Sistema")
ventana.geometry("500x400")
ventana.configure(bg="#eef2f5")
ventana.resizable(False, False)

tk.Label(ventana, text="Iniciar Sesión", font=("Helvetica", 22, "bold"), bg="#eef2f5", fg="#333").pack(pady=25)

form = tk.Frame(ventana, bg="#eef2f5")
form.pack()

# Usuario
tk.Label(form, text="Usuario", font=("Helvetica", 12), bg="#eef2f5", anchor="w").pack(anchor="w", padx=40)
entry_usuario = tk.Entry(form, font=("Helvetica", 14), width=30, bd=2, relief="groove")
entry_usuario.pack(pady=(0, 15), padx=40)

# Contraseña
tk.Label(form, text="Contraseña", font=("Helvetica", 12), bg="#eef2f5", anchor="w").pack(anchor="w", padx=40)
entry_clave = tk.Entry(form, show="*", font=("Helvetica", 14), width=30, bd=2, relief="groove")
entry_clave.pack(pady=(0, 25), padx=40)

# Botón login
tk.Button(ventana, text="Iniciar sesión", font=("Helvetica", 14), bg="#4CAF50", fg="white", padx=10, pady=5, command=validar_login).pack()

ventana.mainloop()
