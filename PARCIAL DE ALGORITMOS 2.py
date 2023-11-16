import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import Scale, Button, Label, Canvas, PhotoImage, StringVar
from PIL import ImageTk, Image

def ajustar_imagen(imagen, brillo, contraste, transparencia):   
    imagen_ajustada = cv2.convertScaleAbs(imagen, alpha=contraste, beta=brillo) 
    imagen_transparente = np.zeros_like(imagen)
    imagen_superpuesta = cv2.addWeighted(imagen_ajustada, transparencia, imagen_transparente, 1 - transparencia, 0)
    return imagen_superpuesta

def seleccionar_imagen():
    root = tk.Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Imagenes seleccionadas", "*.jpg *.png *.jpeg *.bmp *.gif *.tiff")])
    if file_path:
        return cv2.imread(file_path)
    else:
        return None

def ajustar():
    brillo = brillo_slider.get()
    contraste = contraste_slider.get() / 100.0
    transparencia = transparencia_slider.get() / 100.0
    imagen_ajustada = ajustar_imagen(imagen_original, brillo, contraste, transparencia)
    cv2.imshow("En producción", imagen_ajustada)

def aplicar_modificaciones_aleatorias():
    brillo = random.randint(-255, 255)
    contraste = random.uniform(0.1, 3.0)
    transparencia = random.uniform(0.1, 1.0)
    brillo_slider.set(brillo)
    contraste_slider.set(contraste * 100)
    transparencia_slider.set(transparencia * 100)
    ajustar()

def mostrar_10_opciones():
    opciones_especificas = [
        (0, 0, 0),
        (33, 33, 33),
        (66, 66, 66),
        (100, 100, 100),
        (150, 150, 150),
        (200, 200, 200),
        (250, 250, 250),
        (300, 300, 300),
        (350, 350, 350),
        (400, 400, 400),
    ]

    mostrar_opciones(opciones_especificas)

def mostrar_opciones(opciones):
    ventana_opciones = tk.Toplevel()
    ventana_opciones.title("Vista Previa de Opciones")

    for i, opcion in enumerate(opciones):
        brillo, contraste, transparencia = opcion
        imagen_ajustada = ajustar_imagen(imagen_original, brillo, contraste / 100.0, transparencia / 100.0)
        imagen_ajustada = cv2.cvtColor(imagen_ajustada, cv2.COLOR_BGR2RGB)
        imagen_tk = ImageTk.PhotoImage(Image.fromarray(imagen_ajustada).resize((150, 150)))

        label = Label(ventana_opciones, image=imagen_tk)
        label.image = imagen_tk  
        label.grid(row=i // 5, column=i % 5, padx=5, pady=5)

        
        label.bind("<Button-1>", lambda event, o=opcion: seleccionar_opcion(o, ventana_opciones))

    ventana_opciones.mainloop()

def seleccionar_opcion(opcion, ventana_opciones):
    brillo, contraste, transparencia = opcion
    imagen_ajustada = ajustar_imagen(imagen_original, brillo, contraste / 100.0, transparencia / 100.0)
    cv2.imshow("En producción", imagen_ajustada)
    brillo_slider.set(brillo)
    contraste_slider.set(contraste)
    transparencia_slider.set(transparencia)
    ventana_opciones.destroy()

def guardar():
    imagen_ajustada = ajustar_imagen(imagen_original, brillo_slider.get(), contraste_slider.get() / 100.0, transparencia_slider.get() / 100.0)
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if file_path:
        cv2.imwrite(file_path, imagen_ajustada)

def actualizar_imagen(event):
    ajustar()

imagen_original = None

root = tk.Tk()
root.title("Ajuste de Imagen")

imagen_seleccionada = seleccionar_imagen()

if imagen_seleccionada is not None:
    imagen_original = imagen_seleccionada

    brillo_slider = Scale(root, label="Brillo", from_=-255, to=255, orient="horizontal", command=actualizar_imagen)
    brillo_slider.pack()

    contraste_slider = Scale(root, label="Contraste", from_=0, to=300, orient="horizontal", command=actualizar_imagen)
    contraste_slider.pack()

    transparencia_slider = Scale(root, label="Transparencia", from_=0, to=100, orient="horizontal", command=actualizar_imagen)
    transparencia_slider.pack()
    
    boton_modificar_aleatoriamente = tk.Button(root, text="Mod. Aleatorias", command=aplicar_modificaciones_aleatorias)
    boton_modificar_aleatoriamente.pack()

    boton_mostrar_10_modificaciones = tk.Button(root, text="Mostrar 10 Modificaciones", command=mostrar_10_opciones)
    boton_mostrar_10_modificaciones.pack()

    boton_guardar = tk.Button(root, text="Guardar", command=guardar)
    boton_guardar.pack()

    root.mainloop()

