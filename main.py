import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, LEFT, Menu, messagebox, END
import DatosPersonas as crud

v = tk.Tk()
v.title("Ventana Principal")

ancho = 800
alto = 600

x_v = v.winfo_screenwidth() // 2 - ancho // 2
y_v = v.winfo_screenheight() // 2 - alto // 2
v.geometry(f"{ancho}x{alto}+{x_v}+{y_v}")
v.resizable(0, 0)
v.state("zoomed")
v.configure(background="#fff")

txt_id = tk.StringVar()
txt_dni = tk.StringVar()
txt_edad = tk.StringVar()
txt_nombre = tk.StringVar()
txt_apellido = tk.StringVar()
txt_direccion = tk.StringVar()
txt_correo = tk.StringVar()


def salir():
    res = messagebox.askquestion("Salir", "¿Desea salir de la aplicación?")
    if res == "yes":
        v.destroy()

def llenarTabla():
    try:
        tabla.delete(*tabla.get_children())
        res = crud.findAll()
        if res is not None:
            personas = res.get("personas")
            if personas is not None:
                for fila in personas:
                    row = list(fila)
                    row.pop(0)
                    row = tuple(row)
                    tabla.insert("", END, values=row)
            else:
                messagebox.showerror("Error", "No se encontraron personas.")
        else:
            messagebox.showerror("Error", "Error al obtener los datos.")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al llenar la tabla: {e}")


def limpiarCampos():
    txt_edad.set("")
    txt_dni.set("")
    txt_nombre.set("")
    txt_apellido.set("")
    txt_direccion.set("")
    txt_correo.set("")
    e_dni.focus()

def guardar():
    try:
        if txt_edad.get().isnumeric():
            per = {
                "dni": txt_dni.get(),
                "edad": int(txt_edad.get()),
                "nombre": txt_nombre.get(),
                "apellido": txt_apellido.get(),
                "direccion": txt_direccion.get(),
                "correo": txt_correo.get()
            }
            res = crud.save(per)
            print(res)  
            if res is not None and isinstance(res, dict) and "respuesta" in res and "mensaje" in res:
                if res.get("respuesta"):
                    llenarTabla()
                    messagebox.showinfo("OK", res.get("mensaje"))
                    limpiarCampos()
                else:
                    messagebox.showerror("Error", f"Error al guardar: {res.get('mensaje')}")
            else:
                messagebox.showerror("Error", "Respuesta inesperada del servidor.")
        else:
            txt_edad.set("")
            e_edad.focus()
            messagebox.showerror("¡¡¡¡¡Upss", "La edad debe ser numérica!!!!!")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al guardar: {e}")

def consultar():
    if txt_dni.get()!="":
        res = crud.findByDni(txt_dni.get())
        if res.get("respuesta"):
            persona= res.get("persona")
            txt_nombre.set(persona.get("nombre"))
            txt_apellido.set(persona.get("apellido"))
            txt_direccion.set(persona.get("direccion"))
            txt_correo.set(persona.get("correo"))
            txt_edad.set(persona.get("edad"))
        else:
            e_dni.focus() 
            messagebox.showerror("¡¡¡¡¡Upss", "No existe la persona!!!!!")  
    else:
        e_dni.focus() 
        messagebox.showerror("¡¡¡¡¡Upss", "Debe ingresar el dni!!!!!")          

def actualizar():
    try:
        if txt_edad.get().isnumeric():
            per = {
                "dni": txt_dni.get(),
                "edad": int(txt_edad.get()),
                "nombre": txt_nombre.get(),
                "apellido": txt_apellido.get(),
                "direccion": txt_direccion.get(),
                "correo": txt_correo.get()
            }
            res = crud.update(per)
            print(res)  
            if res is not None and isinstance(res, dict) and "respuesta" in res and "mensaje" in res:
                if res.get("respuesta"):
                    llenarTabla()
                    messagebox.showinfo("OK", res.get("mensaje"))
                    limpiarCampos()
                else:
                    messagebox.showerror("Error", f"Error al guardar: {res.get('mensaje')}")
            else:
                messagebox.showerror("Error", "Respuesta inesperada del servidor.")
        else:
            txt_edad.set("")
            e_edad.focus()
            messagebox.showerror("¡¡¡¡¡Upss", "La edad debe ser numérica!!!!!")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al guardar: {e}")

def eliminar():
    try:
        if txt_dni.get() != "":
            res = crud.findByDni(txt_dni.get())
            if res is not None and isinstance(res, dict) and "respuesta" in res and "mensaje" in res:
                if res.get("respuesta"):
                    per = res.get("persona")
                    respuesta = messagebox.askquestion("Confirmar", f"¿Realmente desea eliminar a {per.get('nombre')} {per.get('apellido')}?")
                    if respuesta == "yes":
                        res = crud.delete(per.get("id"))
                        if res.get("respuesta"):
                            llenarTabla()
                            limpiarCampos()
                            messagebox.showinfo("OK", res.get("mensaje"))
                        else:
                            messagebox.showwarning("¡¡¡UPSSSS!!!!", "No se logró eliminar a la persona: " + res.get('mensaje'))
                    else:
                        messagebox.showwarning("¡¡¡UPSSSS!!!!", "Operación cancelada")
                else:
                    messagebox.showwarning("¡¡¡UPSSSS!!!!", "No existe la persona con ese DNI")
            else:
                messagebox.showwarning("¡¡¡UPSSSS!!!!", "No existe la persona con ese DNI")
        else:
            e_dni.focus()
            messagebox.showerror("¡¡¡¡¡Upss", "Debe indicar el DNI")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al eliminar: {e}")


fuente = ("Helvetica", 14)

bg_color_1 = "#ff6347"  # Tomato
bg_color_2 = "#4682b4"  # SteelBlue
font_color = "#ffffff"  # White

label_dni = tk.Label(v, text="DNI: ", anchor="w", justify="left", width=10, bg=bg_color_1, font=fuente, fg=font_color)
label_dni.grid(row=0, column=0, padx=10, pady=5)

label_nombre = tk.Label(v, text="NOMBRE: ", anchor="w", justify="left", width=10, bg=bg_color_2, font=fuente, fg=font_color)
label_nombre.grid(row=1, column=0, padx=10, pady=5)

label_apellido = tk.Label(v, text="APELLIDO: ", anchor="w", justify="left", width=10, bg=bg_color_1, font=fuente, fg=font_color)
label_apellido.grid(row=2, column=0, padx=10, pady=5)

label_direccion = tk.Label(v, text="DIRECCION: ", anchor="w", justify="left", width=10, bg=bg_color_2, font=fuente, fg=font_color)
label_direccion.grid(row=3, column=0, padx=10, pady=5)

label_correo = tk.Label(v, text="CORREO: ", anchor="w", justify="left", width=10, bg=bg_color_2, font=fuente, fg=font_color)
label_correo.grid(row=4, column=0, padx=10, pady=5)

label_edad = tk.Label(v, text="EDAD: ", anchor="w", justify="left", width=10, bg=bg_color_1, font=fuente, fg=font_color)
label_edad.grid(row=5, column=0, padx=10, pady=5)


e_dni = ttk.Entry(v, font=fuente, textvariable=txt_dni)
e_nombre = ttk.Entry(v, font=fuente, textvariable=txt_nombre)
e_apellido = ttk.Entry(v, font=fuente, textvariable=txt_apellido)
e_direccion = ttk.Entry(v, font=fuente, textvariable=txt_direccion)
e_correo = ttk.Entry(v, font=fuente, textvariable=txt_correo)
e_edad = ttk.Entry(v, font=fuente, textvariable=txt_edad)


e_dni.grid(row=0, column=1, padx=10, pady=5)
e_nombre.grid(row=1, column=1, padx=10, pady=5)
e_apellido.grid(row=2, column=1, padx=10, pady=5)
e_direccion.grid(row=3, column=1, padx=10, pady=5)
e_correo.grid(row=4, column=1, padx=10, pady=5)
e_edad.grid(row=5, column=1, padx=10, pady=5)


iconGuardar = PhotoImage(file="Guardar.png")
iconBuscar = PhotoImage(file="Buscar.png")
iconActualizar = PhotoImage(file="Actualizar.png")
iconEliminar = PhotoImage(file="Eliminar.png")

ttk.Button(v, text="Guardar", command=guardar, image=iconGuardar, compound=LEFT).place(x=10, y=220)
ttk.Button(v, text="Consultar", command=consultar, image=iconBuscar, compound=LEFT).place(x=120, y=220)
ttk.Button(v, text="Actualizar", command=actualizar, image=iconActualizar, compound=LEFT).place(x=230, y=220)
ttk.Button(v, text="Eliminar", command=eliminar, image=iconEliminar, compound=LEFT).place(x=340, y=220)

tk.Label(v, text="Lista de Personas", font=("Arial", 16), bg="#fff").place(x=700, y=5)
tabla = ttk.Treeview(v)
tabla.place(x=450, y=40)
tabla["columns"] = ("DNI", "EDAD", "NOMBRE", "APELLIDO", "DIRECCION", "CORREO")


tabla.column("#0", width=0, stretch=tk.NO)
tabla.column("DNI", anchor=tk.W, width=100)
tabla.column("EDAD", anchor=tk.W, width=80)
tabla.column("NOMBRE", anchor=tk.W, width=150)
tabla.column("APELLIDO", anchor=tk.W, width=150)
tabla.column("DIRECCION", anchor=tk.W, width=160)
tabla.column("CORREO", anchor=tk.W, width=160)


tabla.heading("#0", text="")
tabla.heading("DNI", text="Documento")
tabla.heading("EDAD", text="Edad")
tabla.heading("NOMBRE", text="Nombre")
tabla.heading("APELLIDO", text="Apellido")
tabla.heading("DIRECCION", text="Direccion")
tabla.heading("CORREO", text="Correo")


menuTop = Menu(v)
v.config(menu=menuTop)
m_archivo = Menu(menuTop, tearoff=0)
m_archivo.add_command(label="Salir", command=salir)
menuTop.add_cascade(label="Archivo", menu=m_archivo)

m_limpiar = Menu(menuTop, tearoff=0)
m_limpiar.add_command(label="Limpiar Campos",command=limpiarCampos)
menuTop.add_cascade(label="Limpiar", menu=m_limpiar)

m_crud = Menu(menuTop, tearoff=0)
m_crud.add_command(label="Guardar", command=guardar, image=iconGuardar, compound=LEFT)
m_crud.add_command(label="Consultar", command=consultar,image=iconBuscar, compound=LEFT)
m_crud.add_command(label="Actualizar",command=actualizar, image=iconActualizar, compound=LEFT)
m_crud.add_command(label="Borrar",command=eliminar, image=iconEliminar, compound=LEFT)
menuTop.add_cascade(label="Opciones", menu=m_crud)

e_dni.focus()
llenarTabla()
v.mainloop()
