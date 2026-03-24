from tkinter import *
from PIL import Image, ImageTk
import os

def diagnostics():
    winDiag = Tk()
    winDiag.title("Diagnostiques")
    winDiag.geometry("800x600")
    winDiag.iconbitmap("sante.ico")

    frame_diagnostique = Frame(winDiag, bg="green")
    frame_diagnostique.pack()

    try:
        # 🔹 Chemin absolu
        chemin_image = os.path.abspath("diag.png")
        print(f"Chargement de l'image depuis : {chemin_image}")

        # 🔹 Chargement et redimensionnement
        openImag = Image.open(chemin_image).convert("RGBA")
        dim = openImag.resize((150, 150))

        # 🔹 Stocker l’image dans une variable globale
        global imageDiag  
        imageDiag = ImageTk.PhotoImage(dim)

        # 🔹 Utiliser Label au lieu de Button pour tester
        label = Label(frame_diagnostique, image=imageDiag)
        label.image = imageDiag  # Garder une référence
        label.pack()

    except Exception as e:
        print(f"Erreur : {e}")
        Label(frame_diagnostique, text=f"Erreur : {e}", fg="red").pack()

    winDiag.mainloop()




