from datetime import datetime
import webbrowser
from tkinter import *
import tkcalendar.dateentry
from tkinter import ttk,messagebox,simpledialog
from PIL import Image, ImageTk
import mysql.connector
import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
maladie_id = 0

class PlaceholderEntry(Entry):
    def __init__(self, master=None, placeholder="Enter text...", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _clear_placeholder(self, e):
        if self['fg'] == self.placeholder_color:
            self.delete(0, "end")
            self['fg'] = self.default_fg_color

    def _add_placeholder(self, e=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color



########################## les infos de connexion #######################################
host = "127.0.0.1"
user = "root"
password = "ghizlane2004"
database = "hopital"

    

def clear(ecrirenom,ecrireprenom,ecrirecin,ecriredate,myoptions,ecriretele,ecriremail,ecrirepw,ecrirAdrisse):
    ecrirenom.delete(0,"end")
    ecrireprenom.delete(0,"end")
    ecrirecin.delete(0,"end")
    ecriredate.delete(0,"end")
    myoptions.set(None)
    ecriretele.delete(0,"end")
    ecriremail.delete(1.0,"end")
    ecrirepw.delete(0,"end")
    ecrirAdrisse.delete(1.0,"end")
   
    
    
###############################"


def Enregestrer (ecrirenom,ecrireprenom,ecrirecin,ecriredate,myoptions,ecriretele,ecriremail,email_message,ecrirepw,ecrirAdrisse):
    
    nom=ecrirenom.get()
    prenom=ecrireprenom.get()
    cin=ecrirecin.get()
    date_naissance = ecriredate.get_date()
    date_formatee = date_naissance.strftime("%Y-%m-%d")
    sexe=myoptions.get()
    tele=ecriretele.get()
    motdepasse=ecrirepw.get()
    adresse=ecrirAdrisse.get("1.0","end-1c").strip()
    email = ecriremail.get("1.0", "end-1c").strip()
    pattern_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern_email,email):
        email_message.config(text="*Email invalide")
        return
    else:
        email_message.config(text="")  # Nettoyer le message si tout est bon
    
    

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        sql_infos = "INSERT INTO patients (nom,prenom,cin,date_naissance,gender,adresse,telephone,adress_Email,mot_de_passe) VALUES (%s, %s,%s, %s, %s, %s, %s, %s,%s)"
        valeurs_infos = (nom, prenom,cin, date_formatee, sexe, adresse, tele, email,motdepasse)
        cursor.execute(sql_infos, valeurs_infos)
        #cin = cursor.lastrowid

    
        conn.commit()

        messagebox.showinfo( "succes","Patient ajouté avec succès.")

        clear(ecrirenom,ecrireprenom,ecrirecin,ecriredate,myoptions,ecriretele,ecriremail,ecrirepw,ecrirAdrisse)

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur lors de l'ajout du patient : {err}")

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
       
    


def allerAjouter():
    winAj=Toplevel()
    winAj.geometry("2005x1000")
    winAj.title("l'ajout d'un patient")
    winAj.iconbitmap("C:/Users/user/OneDrive/Desktop/prjt gestion de maladie/sante.ico")
    winAj.config(bg="#A4D3EE")

    cadreAjouter=Frame(winAj, bg="#A4D3EE", relief=RAISED, bd=3 ,width=100)
    cadreAjouter.grid(row=0,column=0,columnspan=3,padx=80)

    cadreTitre=Frame(cadreAjouter,bg="#87CEFA" , relief=RAISED, bd=3 ,width=100)
    cadreTitre.grid(row=0,column=2,columnspan=4 )

    titre=Label(cadreTitre,text=" Ajouter les informations personnel de patient---------------------------------------------------",bg="#87CEFA",fg="black",font="Helvatica 20 bold")
    titre.grid( row=0,column=1)

    try:
        ouvrir_image = Image.open("lajout.png")
        nouvelle_taille = (60, 55)
        image_redimensionnee = ouvrir_image.resize(nouvelle_taille) # Redimensionner l'objet Image
        image = ImageTk.PhotoImage(image_redimensionnee) # Convertir en PhotoImage
    except FileNotFoundError:
        print("Fichier image non trouvé.")
        image = None

    if image:
        Bajouter = Label(cadreTitre, image=image, bg="#87CEFA")
        Bajouter.image = image # Garder une référence
        Bajouter.grid(row=0, column=0,padx=5)

        def focus_next_widget(event):
            event.widget.tk_focusNext().focus()
            return "break"

    # Champ Nom
    champ_nom = Label(cadreAjouter, text="Nom : ", bg="#A4D3EE", font="Helvatica 10 bold")
    champ_nom.grid(row=1, column=1, columnspan=2, padx=20, pady=20)
    ecrirenom = Entry(cadreAjouter, width=40)
    ecrirenom.grid(row=1, column=3)
    ecrirenom.bind("<Return>", focus_next_widget)

    # Champ Prénom
    champ_prenom = Label(cadreAjouter, text="Prenom : ", bg="#A4D3EE", font="Helvatica 10 bold")
    champ_prenom.grid(row=2, column=1, columnspan=2, padx=20, pady=20)
    ecrireprenom = Entry(cadreAjouter, width=40)
    ecrireprenom.grid(row=2, column=3)
    ecrireprenom.bind("<Return>", focus_next_widget)

    # Champ CIN
    champ_cin = Label(cadreAjouter, text="CIN : ", bg="#A4D3EE", font="Helvatica 10 bold")
    champ_cin.grid(row=3, column=1, columnspan=2, padx=20, pady=20)
    ecrirecin = Entry(cadreAjouter, width=40)
    ecrirecin.grid(row=3, column=3)
    ecrirecin.bind("<Return>", focus_next_widget)

    # Date de naissance
    champDate = Label(cadreAjouter, text="Date de naissance : ", bg="#A4D3EE", font="Helvatica 10 bold")
    champDate.grid(row=4, column=1, columnspan=2, padx=20, pady=20)
    ecriredate = tkcalendar.DateEntry(cadreAjouter, width=40)
    ecriredate.grid(row=4, column=3)
    ecriredate.bind("<Return>", focus_next_widget)

    # Sexe
    champSexe = Label(cadreAjouter, text="sexe : ", bg="#A4D3EE", font="Helvatica 10 bold")
    champSexe.grid(row=5, column=1, columnspan=2, padx=20, pady=20)
    myoptions = StringVar()
    op1 = ttk.Radiobutton(cadreAjouter, text="féminin", variable=myoptions, value="féminin")
    op2 = ttk.Radiobutton(cadreAjouter, text="masculin", variable=myoptions, value="masculin")
    op1.grid(row=5, column=3)
    op2.grid(row=5, column=4)

    # Téléphone
    tel = Label(cadreAjouter, text=" Numéro téléphone : ", bg="#A4D3EE", font="Helvatica 10 bold")
    tel.grid(row=6, column=1, columnspan=2, pady=20)
    ecriretele = Entry(cadreAjouter, width=40)
    ecriretele.grid(row=6, column=3)
    ecriretele.bind("<Return>", focus_next_widget)

    # Email
    email = Label(cadreAjouter, text=" Adress Email : ", bg="#A4D3EE", font="Helvatica 10 bold")
    email.grid(row=7, column=1, columnspan=2, pady=20)
    ecriremail = Text(cadreAjouter, width=40, height=2)
    ecriremail.grid(row=7, column=3)
    email_message = Label(cadreAjouter, text="", fg="red", bg="#A4D3EE", font="Helvetica 12 italic")
    email_message.grid(row=8, column=3,columnspan=2,sticky="w") 
    # Pour Text widget : utilise Tab (Entrée déclenche juste un saut de ligne)
    ecriremail.bind("<Tab>", focus_next_widget)

    # Mot de passe
    pw = Label(cadreAjouter, text=" mot de passe : ", bg="#A4D3EE", font="Helvatica 10 bold")
    pw.grid(row=9, column=1, columnspan=2, pady=20)
    ecrirepw = Entry(cadreAjouter, width=40, show="*")
    ecrirepw.grid(row=9, column=3)
    ecrirepw.bind("<Return>", focus_next_widget)

    # Adresse
    adress = Label(cadreAjouter, text=" Adress : ", bg="#A4D3EE", font="Helvatica 10 bold")
    adress.grid(row=10, column=1, columnspan=2, pady=20)
    ecrirAdrisse = Text(cadreAjouter, width=40, height=2)
    ecrirAdrisse.grid(row=10, column=3, sticky="we")
    ecrirAdrisse.bind("<Tab>", focus_next_widget)


  
    
   
    ##################### button ############################

    save=Button(winAj,text="Enregestrer",bg="#87CEFA",fg="black",font="Helvatica 12 bold",command= lambda:Enregestrer (ecrirenom,ecrireprenom,ecrirecin,ecriredate,myoptions,ecriretele,ecriremail,email_message,ecrirepw,ecrirAdrisse))
    annuler=Button(winAj,text="Annuler",bg="red",fg="black",font="Helvatica 12 bold",command= lambda:clear (ecrirenom,ecrireprenom,ecrirecin,ecriredate,myoptions,ecriretele,ecriremail,ecrirepw,ecrirAdrisse))
    close=Button(winAj,text="retour",bg="#87CEFA",fg="black",font="Helvatica 12 bold",width=20 ,command=winAj.destroy)
    save.grid(row= 80,column=1, ipady=10,padx=5,columnspan=1,sticky="E")
    annuler.grid(row= 80,column=2,ipadx=15,columnspan=1,padx=5,ipady=10,sticky="W")
    close.grid(row=80,column=0, pady=10, ipadx=10,ipady=10,sticky="Sw")

    winAj.mainloop()


fenetre=Tk()
fenetre.title("gestion des patients")
fenetre.geometry("2005x1000")
fenetre.iconbitmap("C:/Users/user/OneDrive/Desktop/prjt gestion de maladie/sante.ico")
fenetre.config(bg="#FFFFFF")
from tkinter import font

# Police personnalisée
ouvrir_image=Image.open("mmm.jpg")
newDim=(190,60)
newphoto=ouvrir_image.resize(newDim)
image=  ImageTk.PhotoImage(newphoto)
police_bienvenue = font.Font(family="Helvetica", size=18, weight="bold")
cadreWelcome = Frame(fenetre, bg="Black", relief=RAISED, bd=3) # Vert mer, relief
cadreWelcome.grid(row=0, column=0, columnspan=15, sticky="EW", pady=10)
######################################### fram bienvennue#################
welcome =Label(cadreWelcome, text="Bienvenue dans l'application de gestion des Maladies!",
                   fg="white", anchor="center", font=police_bienvenue, bg="black") # Couleur de fond identique au cadre
welcome.grid(row=0, column=10, columnspan=4, sticky="EW", padx=300, pady=10)


###################################### button pour acceder  a web site ####################
def ouvrir_lien():
    webbrowser.open_new("http://localhost/projetPHP/pgPrincipale.php") 
try:
    ouvrir_image = Image.open("parametre.png")
    nouvelle_taille = (40, 50)
    image_redimensionnee = ouvrir_image.resize(nouvelle_taille) # Redimensionner l'objet Image
    icone_parametre= ImageTk.PhotoImage(image_redimensionnee) # Convertir en PhotoImage
except FileNotFoundError:
    print("Fichier image non trouvé.")
    image = None

if image:
   bouton_lien = Button(cadreWelcome, text="Tester le site", image=icone_parametre,compound="left", fg="black",font="Hevatica 10 bold" , bg="white",cursor="hand2", command=ouvrir_lien)
   bouton_lien.image = image # Garder une référence
   bouton_lien.grid(row=0, column=18)
    
   



for i in range(20):
    fenetre.grid_columnconfigure(i, weight=1)
################## image ajouter #################
ajouter = Frame(fenetre, bg="#7EC0EE", relief=RIDGE, bd=3)
ajouter.grid(row=1, column=0, columnspan=4, padx=60,ipadx=40, pady=20)

try:
    ouvrir_image = Image.open("patient.png")
    nouvelle_taille = (150, 150)
    image_redimensionnee = ouvrir_image.resize(nouvelle_taille) # Redimensionner l'objet Image
    image = ImageTk.PhotoImage(image_redimensionnee) # Convertir en PhotoImage
except FileNotFoundError:
    print("Fichier image non trouvé.")
    image = None

if image:
    Bajouter = Button(ajouter, image=image, bg="#7EC0EE",relief=FLAT, command=allerAjouter)
    Bajouter.image = image # Garder une référence
    Bajouter.grid(row=0, column=1, padx=20)
TXT= Label(ajouter,text="   ajouter un patient   ",fg="black",font="Hevatica 20 bold",bg="#7EC0EE") 
TXT.grid(row=1,column=1,padx=20, pady=20) 
###################""############### tableau des patients##########################
def tableauxPatient(window):
    tree = ttk.Treeview(window, columns=("CIN", "Nom", "Prénom", "Date de naissance","nom_maladie","etat patient", "Sexe", "Adresse", "Téléphone", "Email"), show="headings")
# Création du style pour les en-têtes
    style = ttk.Style(window)
    style.configure("Treeview.Heading",  font=("Helvetica", 11, "bold"), foreground="#0F0F0F")
    style.configure("Treeview", rowheight=20, borderwidth=5, relief="solid")  # Ajout de bordures et de hauteur de ligne

    # Définition des en-têtes de colonnes
    tree.heading("CIN", text="CIN")
    tree.heading("Nom", text="Nom")
    tree.heading("Prénom", text="Prénom")
    tree.heading("Date de naissance", text="Date de naissance")
    tree.heading("nom_maladie", text="maladie")
    tree.heading("etat patient", text="l'état du patient")
    tree.heading("Sexe", text="Sexe")
    tree.heading("Adresse", text="Adresse")
    tree.heading("Téléphone", text="Téléphone")
    tree.heading("Email", text="Email")

    tree.column("CIN", width=1)
    tree.column("Nom", width=10)
    tree.column("Prénom", width=10)
    tree.column("nom_maladie", width=15)
    tree.column("etat patient",width=15)
    tree.column("Date de naissance", width=10)
    tree.column("Sexe", width=10)
    tree.column("Adresse", width=30)
    tree.column("Téléphone", width=20)
    tree.column("Email", width=30)    

    # Utilisation de grid() pour placer le Treeview
    tree.grid(row=1, column=0, sticky="nsew")

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        sql_infos = "SELECT patients.cin, patients.nom, patients.prenom, patients.date_naissance, maladie.nom_maladie,diagnostiques.Évolution_Diagnostic_etat_patient, patients.gender, patients.adresse, patients.telephone, patients.adress_Email FROM patients, maladie,diagnostiques where patients.cin = maladie.patient_id and patients.cin=diagnostiques.id_patient;"
        
        cursor.execute(sql_infos)
        patients = cursor.fetchall()

        # Insertion des données dans le Treeview
        for patient in patients:
            # Ajout de la ligne de séparation
            tree.insert("", "end", values=("__________________________", "__________________________", "__________________________", "__________________________", "__________________________", "__________________________", "______________________________", "__________________________","__________________________","__________________________" ))
            tree.insert("", "end", values=patient)  
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des patients : {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()  
    return tree        

################## affiche liste #################
def liste_patients():
    winList = Toplevel()
    winList.title("Liste des patients")
    winList.geometry("2005x1000")  # Ajustez la taille selon vos besoins
    winList.iconbitmap("C:/Users/user/OneDrive/Desktop/prjt gestion de maladie/sante.ico")
     
        # Configuration des poids des lignes et des colonnes de la fenêtre principale
    winList.rowconfigure(0, weight=0)  # Le titre ne s'étire pas verticalement
    winList.rowconfigure(1, weight=1)  # Le Treeview s'étire verticalement
    winList.columnconfigure(0, weight=1)
    

    # Création du Frame pour le titre
    titre_frame = Frame(winList,bg="Black",relief=RAISED,bd=3)
    titre_frame.grid(row=0, column=0, sticky="ew",pady=10)

    titre = Label(titre_frame, text="Liste des Patients", font=("Helvetica", 24, "bold"), bg="Black", fg="white")
    titre.grid(row=0, column=0,padx=20,pady=10)
    

    recherche = PlaceholderEntry(titre_frame, placeholder="rechercher un patient", font=("Segoe UI", 14), width=30)
    recherche.grid(row=0,column=2,ipadx=12,ipady=8, sticky="E")
######################## rechercher un patient ##################
    def rechercher_patient():
        terme_recherche = recherche.get().lower()
        trouve = False
        for IDligne in tree.get_children():# recuperee l'identifiants de chaque ligne
            values = tree.item(IDligne, 'values')
            if any(terme_recherche in str(val).lower() for val in values):
                tree.selection_set(IDligne)
                tree.see(IDligne)
                trouve = True
                break
        if not trouve:
            messagebox.showerror("Erreur", "Patient non trouvé.")
    try:
        ouvrirImag=Image.open("rechercher.png")
        dim=ouvrirImag.resize((50,32))
        myImg=ImageTk.PhotoImage(dim)
    except FileNotFoundError:
           print("image rechecher n'existe pas")
           b = Button(titre_frame, text="rechercher", font="helvatica 10 bold", bg="#1E90FF",fg="white", command=rechercher_patient)
           b.grid(row=0, column=1, ipadx=5, ipady=4, sticky="E")
    if myImg:

        bimage=Button(titre_frame, image=myImg , command=rechercher_patient)
        bimage.image=myImg
        bimage.grid(row=0, column=1, ipadx=5, ipady=4, sticky="E")
    recherche.bind("<Return>",lambda event :rechercher_patient())

    try:
        ouvrirImage=Image.open("supDossier.png")
        dimen=ouvrirImage.resize((50,28))
        myImge=ImageTk.PhotoImage(dimen)
    except FileNotFoundError:
           print("image supdossier n'existe pas")
           bs = Button(titre_frame, text="supprimer",font="helvatica 10 bold",  bg="rouge",fg="white", command=rechercher_patient)
           bs.grid(row=0, column=3, ipadx=12, ipady=12, sticky="E", padx=5)
    if myImge:
        BSUPR = Button(titre_frame, image=myImge, bg="red", command=supprimer_patients)
        BSUPR.image=myImge
        BSUPR.grid(row=0, column=3, ipadx=12, ipady=5,padx=15, sticky="E")

    try:
        ouvrImage=Image.open("retour.png")
        dimension=ouvrImage.resize((50,28))
        myImage=ImageTk.PhotoImage(dimension)
    except FileNotFoundError:
           print("image retour n'existe pas")
           br = Button(titre_frame, text="retour",font="helvatica 10 bold",  bg="rouge",fg="white", command=rechercher_patient)
           br.grid(row=0, column=4, ipadx=12,ipady=5, sticky="E")
    if myImage:
        Bretour = Button(titre_frame, image=myImage,bg="#A4D3EE",command=winList.destroy)
        Bretour.image=myImage
        Bretour.grid(row=0, column=4, ipadx=12,ipady=5, sticky="E")
        
    titre_frame.columnconfigure(1, weight=1)

    tree = tableauxPatient(winList)
    

    # Création du Treeview (tableau)

   
list = Frame(fenetre, bg="#7EC0EE", relief=RIDGE, bd=3)
list.grid(row=2, column=4, columnspan=4, padx=20,ipadx=40, pady=20)

try:
    ouvrir_image = Image.open("consulter.png")
    nouvelle_taille = (150, 150)
    image_redimensionnee = ouvrir_image.resize(nouvelle_taille) # Redimensionner l'objet Image
    image = ImageTk.PhotoImage(image_redimensionnee) # Convertir en PhotoImage
except FileNotFoundError:
    print("Fichier image non trouvé.")
    image = None

if image:
    BListe = Button(list, image=image,bg="#7EC0EE",relief=FLAT,command=liste_patients)
    BListe.image = image # Garder une référence
    BListe.grid(row=0, column=1, padx=20)
TXT= Label(list,text="consulter les patients",fg="black",font="Hevatica 20 bold",bg="#7EC0EE") 
TXT.grid(row=1,column=1,padx=20, pady=20) 


####################   fct supprimer  ################################
 
def supprimer_patients():
    winSupp = Tk()
    winSupp.title("Suppression de patient")
    winSupp.geometry("400x200")  # Taille de fenêtre plus raisonnable
    winSupp.iconbitmap("sante.ico")  # Assurez-vous que le chemin est correct
    winSupp.config(bg="#A4D3EE")


    id_label = Label(winSupp, text="Entrez CIN du patient à supprimer  :",bg="#A4D3EE", font="Helvetica 10 bold")
    id_label.grid(row=0, column=0, padx=10, pady=20)
    id_entry = Entry(winSupp)
    id_entry.grid(row=0, column=1, padx=10, pady=20)

    def confirmer_suppression():
        patient_id = id_entry.get()

        if not patient_id:
            messagebox.showerror("Erreur", "Veuillez entrer le CIN de patient.")
            return

        try:
            con = mysql.connector.connect(host=host, user=user, password=password, database=database) 
            cursor = con.cursor()

            # Vérifier si le patient existe
            requete_verification = "SELECT nom, prenom FROM patients WHERE cin = %s"
            cursor.execute(requete_verification, (patient_id,))
            patient = cursor.fetchone()

            if not patient:
                messagebox.showerror("Erreur", "Patient non trouvé.")
                return

            nom_patient, prenom_patient = patient
            confirmation = messagebox.askokcancel("Confirmer", f"Êtes-vous sûr de vouloir supprimer le dossier de {nom_patient} {prenom_patient} ?")

            if confirmation:
                # Supprimer les enregistrements liés dans les autres tables (avec précautions)

                cursor.execute("DELETE FROM traitements WHERE id_diagnostique IN (SELECT id_diagnostique FROM diagnostiques WHERE id_patient = %s)", (patient_id,))
                cursor.execute("DELETE FROM maladie WHERE patient_id = %s", (patient_id,))
                cursor.execute("DELETE FROM diagnostiques WHERE id_patient = %s", (patient_id,))
                
                cursor.execute("DELETE FROM symptômes WHERE patient_id = %s", (patient_id,))
                cursor.execute("DELETE FROM suivi_medical WHERE id_patient = %s", (patient_id,))
                cursor.execute("DELETE FROM patients WHERE cin = %s", (patient_id,))
                

                con.commit()
                messagebox.showinfo("Succès", "Dossier patient supprimé avec succès.")
            else:
                messagebox.showinfo("Information", "Suppression annulée.")

        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {err}")

        finally:
            if con.is_connected():
                cursor.close()
                con.close()

    supprimer_button = Button(winSupp, text="Supprimer",bg="red" , font="Helvatica 11 bold",command=confirmer_suppression)
    supprimer_button.grid(row=1, column=1, columnspan=2, pady=5)

    winSupp.mainloop() 

#################" fct enregistrer diagnostique #########################
def enregestrer_Diag(entryCin,entrydataDiag,entrytest,entryresultat,entryMaladie,entryetatPateint): 
    cinP=entryCin.get()
    dateDiag=entrydataDiag.get_date()
    dateFormatee=dateDiag.strftime("%Y-%m-%d")
    test=entrytest.get()
    res=entryresultat.get()
    Maladie=entryMaladie.get()
    etat=entryetatPateint.get()
    try:

        conn=mysql.connector.connect(host=host,user=user,password=password,database=database)
        CURSOR=conn.cursor()
        CURSOR.execute("SELECT id_symptomes FROM symptômes WHERE patient_id=%s ",(cinP,))
        id_symptomes=CURSOR.fetchall()
        if id_symptomes:
            id_symptomes=id_symptomes[0][0]
            sqlDiag="insert into diagnostiques(id_patient,date,Évolution_Diagnostic_etat_patient,type_de_test,resultat_de_test,id_symptomes ) values(%s,%s,%s,%s,%s,%s)"
            valeurs=(cinP,dateFormatee,etat,test,res ,id_symptomes)
            CURSOR.execute(sqlDiag,valeurs)
            id_diagnostique=CURSOR.lastrowid

            sqlMladie="INSERT INTO maladie(nom_maladie,patient_id,id_symptomes,id_diagnostique)values(%s,%s,%s,%s)"
            vals=(Maladie,cinP,id_symptomes,id_diagnostique)
            CURSOR.execute(sqlMladie,vals)
            conn.commit()
            messagebox.showinfo( "succes","diagnostique et maladie ajouté avec succès.")
        else:
            messagebox.showerror("error","veuillez d'abord d'enregistrer les symptomes!")    

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur lors de l'ajout du diagnostique : {err}")

    finally:
        if conn and conn.is_connected():
            CURSOR.close()
            conn.close()
       ############################## button supprimer #################"
def buttonSuppr(entreId):
    idDiag=entreId.get() 
    if not idDiag:
       messagebox.showerror("erreur","veuillez entrez l'id de diagnostgique")
    try:
        conn=mysql.connector.connect(host=host,user=user,password=password,database=database)
        CURSOR=conn.cursor()
        
        confirmation=messagebox.askokcancel("confirmer","Êtes-vous sûr de vouloir supprimer cette diagnostique")
        if confirmation:
         
           CURSOR.execute("DELETE FROM traitements where id_diagnostique=%s",(idDiag,))
          
           CURSOR.execute("DELETE FROM maladie where id_diagnostique=%s",(idDiag,))
           CURSOR.execute("DELETE FROM diagnostiques where id_diagnostique=%s",(idDiag,))
           conn.commit()
           messagebox.showinfo( "succes","diagnostique supprimer avec succès.")

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur lors de supprission de diagnostique : {err}")

    finally:
        if conn and conn.is_connected():
            CURSOR.close()
            conn.close()

######################### consulter diagnostique ###########################


def consulterDiag():
    winConsulter = Toplevel()
    winConsulter.title("Consulter Diagnostique")
    winConsulter.geometry("2005x800")
    winConsulter.iconbitmap("sante.ico") 
    winConsulter.config(bg="#A4D3EE")

    # ==== Canvas pour tout le contenu ====
    main_canvas = Canvas(winConsulter, bg="#A4D3EE", highlightthickness=0)
    main_scrollbar = Scrollbar(winConsulter, orient=VERTICAL, command=main_canvas.yview)
    main_canvas.configure(yscrollcommand=main_scrollbar.set)

    main_scrollbar.pack(side=RIGHT, fill=Y)
    main_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # ==== Frame contenant tout ====
    container = Frame(main_canvas, bg="#A4D3EE")
    main_canvas.create_window((0, 0), window=container, anchor="nw")

    def on_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))

    container.bind("<Configure>", on_configure)

    def on_mousewheel(event):
        main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    main_canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ==== Widgets ====
    Label(container, text="Entrez le CIN du patient :", bg="#A4D3EE", font="Helvetica 12 bold").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entreCin = Entry(container, width=30)
    entreCin.grid(row=0, column=1, padx=10, pady=20, sticky="w")

    global choix_consultation
    choix_consultation = StringVar(value="dernier")

    FrameChoix = Frame(container, bg="#A4D3EE")
    FrameChoix.grid(row=1, column=0, columnspan=2,pady=10, sticky="w", padx=10)
    Label(FrameChoix, text="Choix de consultation :", font="Helvetica 11 bold", bg="#A4D3EE").grid(row=0, column=0, sticky="w")
    Radiobutton(FrameChoix, text="Dernier diagnostique", variable=choix_consultation, value="dernier", bg="#A4D3EE").grid(row=0, column=1, sticky="w", padx=10)
    Radiobutton(FrameChoix, text="Tous les diagnostiques", variable=choix_consultation, value="tous", bg="#A4D3EE").grid(row=0, column=2, sticky="w", padx=10)

    global framDiag
    framDiag = Frame(container, bg="#A4D3EE", bd=3, relief=GROOVE)
    framDiag.grid(row=3, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

    def infoDiag():
        for widget in framDiag.winfo_children():
            widget.destroy()

        try:
            con = mysql.connector.connect(host=host, user=user, password=password, database=database)
            cursor = con.cursor()
            cin_patient = entreCin.get()

            cursor.execute("SELECT nom, prenom FROM patients WHERE cin=%s", (cin_patient,))
            info = cursor.fetchone()

            if info:
                nom, prenom = info

                if choix_consultation.get() == "dernier":
                    cursor.execute("SELECT * FROM diagnostiques WHERE id_patient = %s ORDER BY date DESC LIMIT 1", (cin_patient,))
                    diagnostics = [cursor.fetchone()]
                else:
                    cursor.execute("SELECT * FROM diagnostiques WHERE id_patient = %s ORDER BY date DESC", (cin_patient,))
                    diagnostics = cursor.fetchall()

                if diagnostics and diagnostics[0]:
                    Label(framDiag, text=f"👤 Patient : {nom} {prenom} (CIN : {cin_patient})", bg="#E0FFFF", fg="#003366", font="Helvetica 14 bold").grid(row=0, column=0, columnspan=2, pady=(10, 30))

                    for index, diagnostique in enumerate(diagnostics):
                        idDiag, idPatient, date, etatPatient, typeTeste, resTest, idsymtomes = diagnostique

                        cursor.execute("SELECT nom_maladie FROM maladie WHERE id_diagnostique=%s", (idDiag,))
                        nomMaladie = cursor.fetchone()

                        cursor.execute("SELECT symptômes_descriptions FROM symptômes WHERE id_symptomes=%s", (idsymtomes,))
                        symptomes = cursor.fetchone()

                        base_row = index * 10 + 2

                        Label(framDiag, text=f" Diagnostique #{index+1}", fg="#003366", bg="#A4D3EE", font="Helvetica 13 bold underline").grid(row=base_row, column=0, columnspan=2, pady=(5, 0))

                        # Définir une fonction pour afficher les infos avec titre + valeur
                        def ligne_info(row, titre, valeur, fond="#A4D3EE"):
                            ligne = Frame(framDiag, bg=fond)
                            ligne.grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=2)
                            Label(ligne, text=f"{titre} ", bg=fond, fg="#00008B", font="Helvetica 12 bold").pack(side="left")
                            Label(ligne, text=f"{valeur}", bg=fond, font="Helvetica 12").pack(side="left")

                        # Affichage des infos avec fonction
                        ligne_info(base_row+1, "Date :", date)
                        ligne_info(base_row+2, "Maladie :", nomMaladie[0] if nomMaladie else "Non trouvée")
                        ligne_info(base_row+3, "Symptômes :", symptomes[0] if symptomes else "Non trouvés")
                        ligne_info(base_row+4, "État :", etatPatient)
                        ligne_info(base_row+5, "Test :", typeTeste)
                        ligne_info(base_row+6, "Résultat :", resTest)

                        Label(framDiag, text="─" * 100, bg="#A4D3EE", fg="gray").grid(row=base_row+7, column=0, columnspan=2, pady=10)

                else:
                    messagebox.showinfo("Information", "Aucun diagnostique trouvé.")
            else:
                messagebox.showinfo("Information", "Aucun patient trouvé.")
        except mysql.connector.Error as err:
            messagebox.showinfo("Erreur", f"Erreur de connexion : {err}")
        finally:
            if 'con' in locals() and con.is_connected():
                cursor.close()
                con.close()

    Button(container, text="Consulter", font="Helvetica 14 bold", bg="blue", fg="white", command=infoDiag).grid(row=2, column=0, columnspan=2, pady=10)





################### fct supprimer un diagnostic##########################
def suppDiag():
    winSuppr=Toplevel()
    winSuppr.title("supprission d'un diagnostique")
    winSuppr.geometry("2005x1000")
    winSuppr.configure(bg="#A4D3EE")
    winSuppr.iconbitmap("sante.ico")

    winSuppr.grid_rowconfigure(1, weight=1)
    winSuppr.grid_columnconfigure(0, weight=1)
    winSuppr.grid_columnconfigure(1, weight=1)
    winSuppr.grid_columnconfigure(2, weight=1)


    l=Label(winSuppr,text="Entrez ID de diagnostique à supprimer :",bg="#A4D3EE",font="Helvatica 12 bold")
    l.grid(row=0,column=0 ,pady=20,sticky="w")

    entreId=Entry(winSuppr,width=30)
    entreId.grid(row=0,column=1,sticky="w")

    b=Button(winSuppr,text="supprimer",bg="red",font="Helvatica 12 bold",command= lambda:buttonSuppr(entreId))
    b.grid(row=0,column=3,sticky="w")
    
      
    tree = ttk.Treeview(winSuppr, columns=("ID diag", "id patient", "Date de diagnostique","etat patient","type de test","resultat de test","ID symptomes"), show="headings")
# Création du style pour les en-têtes
    style = ttk.Style(winSuppr)
    style.configure("Treeview.Heading",  font=("Helvetica", 11, "bold"), foreground="#0F0F0F")
    style.configure("Treeview", rowheight=20, borderwidth=5, relief="solid")  # Ajout de bordures et de hauteur de ligne

    # Définition des en-têtes de colonnes
    tree.heading("ID diag", text="ID diagnostic")
    tree.heading("id patient", text="id patient")
    tree.heading("Date de diagnostique", text="Date de diagnostique")
    tree.heading("etat patient", text="etat patient")
    tree.heading("type de test", text="type de test")
    tree.heading("resultat de test", text="resultat de test")
    tree.heading("ID symptomes", text="ID symptomes")
    
    

    # Utilisation de grid() pour placer le Treeview
    tree.grid(row=1, column=0,columnspan=4,pady=40, sticky="nsew")

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        sql_infos = "SELECT * from diagnostiques;"
        
        cursor.execute(sql_infos)
        daigs = cursor.fetchall()

        # Insertion des données dans le Treeview
        for diag in daigs:
            # Ajout de la ligne de séparation
            tree.insert("", "end", values=("__________________________", "__________________________", "__________________________", "__________________________", "__________________________", "__________________________", "______________________________", "__________________________","__________________________","__________________________" ))
            tree.insert("", "end", values=diag)  
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération des diagnostique : {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close() 

    winSuppr.mainloop()


################## planifie un suivi #######################

def palnifie():
        root = Tk()
        root.title("Planification de Suivi Médical")
        root.geometry("2005x1000")
        root.config(bg="#A4D3EE")
        root.iconbitmap("sante.ico")

       
        
        fram=Frame(root,bg="blue",relief=RAISED,bd=3)
        fram.grid(row=0,column=0,columnspan=6,sticky="ew",ipady=5)
        titre=Label(fram,text="                Mettre en place le prochain suivi",bg="blue",fg="white",font="helvatica 20 bold")
        titre.grid(row=0,column=1,columnspan=4,padx=200,pady=6)
      
     

        
# Formulaire pour entrer les informations du suivi
        Label(root, text=" CIN de Patient:",bg="#A4D3EE",font="helvatica 12 bold").grid(row=1, column=0,pady=20,columnspan=2)
        entry_patient = Entry(root,width=40)
        entry_patient.grid(row=1, column=1,pady=20)

        Label(root, text="Date du prochain suivi:",bg="#A4D3EE",font="helvatica 12 bold").grid(row=2, column=0,pady=20,columnspan=2)
        entry_date = tkcalendar.DateEntry(root,width=40)
        entry_date.grid(row=2, column=1)

        Label(root, text="Heure (HH:MM):",bg="#A4D3EE",font="helvatica 12 bold").grid(row=3, column=0,pady=20,padx=20,columnspan=2)
        entry_heure = ttk.Entry(root,width=40)
        entry_heure.grid(row=3, column=1)

        Label(root, text="Objet du suivi:",bg="#A4D3EE",font="helvatica 12 bold").grid(row=4, column=0,pady=20,padx=20,columnspan=2)
        entry_objet = Entry(root,width=40)
        entry_objet.grid(row=4, column=1)

        Label(root, text="Médecin:",bg="#A4D3EE",font="helvatica 12 bold").grid(row=5, column=0,pady=20,padx=20,columnspan=2)
        entry_medecin = Entry(root,width=40)
        entry_medecin.grid(row=5, column=1)
        

# Tableau pour afficher les suivis planifiés
        columns = ("id suivi"," CIN ", "Date", "Heure", "Objet", "Médecin","statut")
        suivi_table = ttk.Treeview(root, columns=columns, show="headings")
        suivi_table.grid(row=8, column=0, columnspan=2,pady=50,ipady=30)

        style = ttk.Style(root)
        style.configure("Treeview.Heading",  font=("Helvetica", 11, "bold"), foreground="Blue")
        style.configure("Treeview", rowheight=20, borderwidth=5, relief="solid")
        for col in columns:
          suivi_table.heading(col, text=col)

        try:
             # Connexion à la base de données MySQL
              db = mysql.connector.connect(host=host,user=user,password=password,database=database)
              cursor = db.cursor()

        # Requête SQL pour insérer les données
              sql="select * from suivi_medical;"
              cursor.execute(sql)
              suivi=cursor.fetchall()
              for s in suivi:
                suivi_table.insert("","end",values=("__________________________", "__________________________", "__________________________", "__________________________", "__________________________", "__________________________", "______________________________"))
                suivi_table.insert("","end",values=s)
              db.commit()
        except mysql.connector.Error as err:
              messagebox.showerror("Erreur", f"Erreur lors de l'extraction des donnees : {err}")
        

        def ajouter_suivi(): 
            patient = entry_patient.get()
            date_suivi = entry_date.get_date()
            dateForma=date_suivi.strftime("%Y-%m-%d")
            heure = entry_heure.get()
            objet = entry_objet.get()
            medecin = entry_medecin.get()

        # Validation des champs
            if not (patient and date_suivi and heure and objet and medecin):
              messagebox.showwarning("Champs manquants", "Tous les champs doivent être remplis.")
              return

            try:
              db = mysql.connector.connect(host=host,user=user,password=password,database=database)
              cursor = db.cursor()
              query = "INSERT INTO suivi_medical (id_patient, date_suivi, heure, objet, medecin) VALUES (%s, %s, %s, %s, %s)"
              values = (patient, dateForma, heure, objet, medecin)
              cursor.execute(query, values)

              db.commit()  # Confirmer la transaction
              messagebox.showinfo("Succès", "Suivi ajouté avec succès !")
               # Ajouter dans le tableau
              last_id = cursor.lastrowid
              suivi_table.insert("", "end", values=(last_id, patient, dateForma, heure, objet, medecin, "Prévu"))

              
        # Réinitialiser les champs
              entry_patient.delete(0, END)
              entry_date.delete(0, END)
              entry_heure.delete(0, END)
              entry_objet.delete(0, END)
              entry_medecin.delete(0, END)

            except mysql.connector.Error as err:
              messagebox.showerror("Erreur", f"Erreur lors de l'ajout du suivi : {err}")
            finally:
        # Fermer correctement ici
               if 'cursor' in locals():
                  cursor.close()
               if 'db' in locals() and db.is_connected():
                   db.close()
         
        btn_ajouter = Button(root, text="Ajouter un suivi",bg="blue",fg="white",font="helvatica 12 bold",command=ajouter_suivi)
        btn_ajouter.grid(row=7, column=1)

        def modifier_statut():
                selected = suivi_table.selection()
                if not selected:
                     messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un suivi.")
                     return

                selected_id = selected[0]  # ID interne de l'élément sélectionné dans le Treeview
                ligne = suivi_table.item(selected_id)
                valeurs = ligne['values']
                id_suivi = valeurs[0]

                statut_popup = Toplevel(root)
                statut_popup.title("Modifier le statut")
                statut_popup.geometry("300x300")
                statut_popup.config(bg="#A4D3EE")
                statut_popup.grab_set()

                Label(statut_popup, text="Nouveau statut :",bg="#A4D3EE", font="Helvetica 12 bold").pack(pady=10)

                statuts = ["prévu", "effectué", "annulé", "reporté"]
                combo_statut = ttk.Combobox(statut_popup, values=statuts, state="readonly")
                combo_statut.pack(pady=5)
                combo_statut.current(0)

                date_label = Label(statut_popup, text="Nouvelle date :", bg="#A4D3EE", font="Helvetica 12 bold")
                date_picker = tkcalendar.DateEntry(statut_popup, width=20)
                def on_statut_change(event):
                    if combo_statut.get() == "reporté":
                         date_label.pack(pady=5)
                         date_picker.pack()
                    else:
                        date_label.pack_forget()
                        date_picker.pack_forget()

                combo_statut.bind("<<ComboboxSelected>>", on_statut_change)
     

                def valider_statut():
                     nouveau_statut = combo_statut.get()
                     try:
                           db = mysql.connector.connect(host=host, user=user, password=password, database=database)
                           cursor = db.cursor()

                           if nouveau_statut == "reporté":
                            nouvelle_date = date_picker.get_date().strftime("%Y-%m-%d")
                            update_query = "UPDATE suivi_medical SET statut = %s, date_suivi = %s WHERE id_suivi = %s"
                            cursor.execute(update_query, (nouveau_statut, nouvelle_date, id_suivi))
                            valeurs[2] = nouvelle_date  # Mettre à jour la colonne "date" (supposée colonne 2)
                           else:
                             update_query = "UPDATE suivi_medical SET statut = %s WHERE id_suivi = %s"
                             cursor.execute(update_query, (nouveau_statut, id_suivi))

                             valeurs[6] = nouveau_statut  # Mettre à jour la colonne "statut"
                             suivi_table.item(selected_id, values=valeurs)

                           db.commit()
                           messagebox.showinfo("Succès", "Statut modifié avec succès.")
                           statut_popup.destroy()

                     except mysql.connector.Error as err:
                          messagebox.showerror("Erreur", f"Erreur MySQL : {err}")
                     finally:
                          if 'cursor' in locals():
                              cursor.close()
                          if 'db' in locals() and db.is_connected():
                              db.close()

                Button(statut_popup, text="Valider", command=valider_statut, bg="blue", fg="white", font="Helvetica 10 bold").pack(pady=15)

        btn_modifier_statut = Button(fram, text="Modifier Statut", bg="white", fg="blue", font="helvatica 10 bold",command=modifier_statut)
        btn_modifier_statut.grid(row=0, column=500, padx=250)
       

# Lancer l'interface
        root.mainloop()

################### daignostique ##########################

def diagnostics():
    winDiag = Toplevel()  # 🔹 Utilise Toplevel() pour créer une nouvelle fenêtre Tkinter
    winDiag.title("Diagnostiques")
    winDiag.geometry("2005x1000")
    winDiag.iconbitmap("sante.ico")
   # winDiag.configure(bg="#B0E2FF")

    frame_diagnostique = Frame(winDiag)
    frame_diagnostique.grid(row=0,column=0)

    framPrincipale=Frame(winDiag,bg="#A4D3EE")
    framPrincipale.grid(row=0,column=1,sticky="n",columnspan=4,padx=10)

    Frame_save_diag=Frame(framPrincipale,bg="#87CEFA",relief=RAISED,bd=3)
    Frame_save_diag.grid(row=0,column=1,sticky="n",columnspan=4,padx=10)
    Frame_save_diag.rowconfigure(0,weight=1)
    titre=Label(Frame_save_diag,text="        Enregistrer les dianostique d'un patient                         ",font="Helvatica 20 bold",bg="#87CEFA")
    titre.grid(row=0,column=1,padx=10,pady=10)
    
    def focus_next_widget(event):
            event.widget.tk_focusNext().focus()
            return "break"

    # CIN
    cin = Label(framPrincipale, text="CIN de patient :", font="Helvatica 10 bold", bg="#A4D3EE")
    cin.grid(row=2, column=1, pady=10)
    entryCin = Entry(framPrincipale, width=40)
    entryCin.grid(row=2, column=2, pady=10)
    entryCin.bind("<Return>", focus_next_widget)

    # Date de diagnostic
    dataDiag = Label(framPrincipale, text="date de diagnostic :", font="Helvatica 10 bold", bg="#A4D3EE")
    dataDiag.grid(row=4, column=1, pady=10)
    entrydataDiag = tkcalendar.DateEntry(framPrincipale, width=40)
    entrydataDiag.grid(row=4, column=2, pady=10)
    entrydataDiag.bind("<Return>", focus_next_widget)

    # Test diagnostique
    test = Label(framPrincipale, text="Catégories de tests diagnostiques :", font="Helvatica 10 bold", bg="#A4D3EE")
    test.grid(row=5, column=1, pady=10)
    entrytest = ttk.Combobox(framPrincipale, width=40, values=[
        "test simple", "Radiographie (rayons X)", "Échographie ", "Tests de diagnostic cardiaque",
        "Tests de diagnostic pulmonaire", "Tests de diagnostic gastro-intestinal ",
        "Tests génétiques ", "Tests sanguins", "Analyse d'urine "
    ])
    entrytest.grid(row=5, column=2, pady=10)
    entrytest.bind("<Return>", focus_next_widget)

    # Résultat
    resultat = Label(framPrincipale, text="résultat de test :", font="Helvatica 10 bold", bg="#A4D3EE")
    resultat.grid(row=6, column=1, pady=10)
    entryresultat = Entry(framPrincipale, width=40)
    entryresultat.grid(row=6, column=2, pady=10)
    entryresultat.bind("<Return>", focus_next_widget)

    # Maladie diagnostiquée
    nomMaladi = Label(framPrincipale, text="maladie diagnostiquée :", font="Helvatica 10 bold", bg="#A4D3EE")
    nomMaladi.grid(row=7, column=1, pady=10)
    entryMaladie = Entry(framPrincipale, width=40)
    entryMaladie.grid(row=7, column=2, pady=10)
    entryMaladie.bind("<Return>", focus_next_widget)

    # État du patient
    etatPateint = Label(framPrincipale, text="Évaluation de l'état du patient :", font="Helvatica 10 bold", bg="#A4D3EE")
    etatPateint.grid(row=8, column=1, pady=10)
    entryetatPateint = ttk.Combobox(framPrincipale, width=40, values=["urgent", "stable", "amélioration"])
    entryetatPateint.grid(row=8, column=2, pady=10)
    entryetatPateint.bind("<Return>", focus_next_widget)


    save=Button(framPrincipale,text="Enregistrer",bg="#1E90FF",font="Helvatica 10 bold",command= lambda:enregestrer_Diag(entryCin,entrydataDiag,entrytest,entryresultat,entryMaladie,entryetatPateint))
    save.grid(row=9,column=1,columnspan=2,pady=20,padx=20,ipadx=13,ipady=10)

    framConsultergrp = Frame(framPrincipale, bg="#EE3B3B", relief=RAISED, bd=3)
    framConsultergrp.grid(row=15, column=1, pady=50, sticky="wE")

    try:
       ouvrir_image=Image.open("supprimer.png")
       newDim=ouvrir_image.resize((150,150))
       nvimage=ImageTk.PhotoImage(newDim)
    except FileNotFoundError:
       print("image supprimer n'existe pas")
       nvimage=None
    if nvimage:
       bConsulter1=Button(framConsultergrp,image=nvimage,bg="#EE3B3B",relief=FLAT,command=suppDiag )
       bConsulter1.image=nvimage
       bConsulter1.grid(row=0, column=1)
    
    LConsulter1 = Label(framConsultergrp, text="supprimer \nun diagnostique ", 
                    font="Helvetica 15 bold", bg="#EE3B3B", fg="Black", padx=10, pady=10)
    LConsulter1.grid(row=1, column=1,padx=15,pady=10)
##################################################################
    framConsulter1 = Frame(framPrincipale, bg="#AEEEEE", relief=RAISED, bd=3)
    framConsulter1.grid(row=15, column=2, pady=50, sticky="wE")

    try:
       ouvrir_image=Image.open("voir.png")
       newDim=ouvrir_image.resize((180,150))
       nvimage=ImageTk.PhotoImage(newDim)
    except FileNotFoundError:
       print("image consulter n'existe pas")
       nvimage=None
    if nvimage:
       bConsulter1=Button(framConsulter1,image=nvimage,bg="#AEEEEE",relief=FLAT,command=consulterDiag )
       bConsulter1.image=nvimage
       bConsulter1.grid(row=0, column=1, padx=10)
    
    LConsulter1 = Label(framConsulter1, text=" Consulter \n un diagnostique", 
                    font="Helvetica 15 bold", bg="#AEEEEE", fg="Black", padx=10, pady=10)
    LConsulter1.grid(row=1, column=1,padx=10,pady=10)

    #################################################
    framePlanifi= Frame(framPrincipale, bg="#EEE8AA", relief=RAISED, bd=3)
    framePlanifi.grid(row=15, column=3,  pady=50, sticky="wE")

    try:
       ouvrir=Image.open("planifie.png")
       Dim=ouvrir.resize((190,150))
       image=ImageTk.PhotoImage(Dim)
    except FileNotFoundError:
       print("image planifie n'existe pas")
       image=None
    if image:
       b=Button(framePlanifi,image=image,bg="#EEE8AA",relief=FLAT ,command=palnifie)
       b.image=image
       b.grid(row=0, column=1, padx=15)
    
    L= Label(framePlanifi, text="Planifier \nun suivi", 
                    font="Helvetica 15 bold", bg="#EEE8AA", fg="Black", padx=10, pady=10)
    L.grid(row=1, column=1,pady=10)


    try:
        chemin_image = os.path.abspath("diag.png")
        print(f"🔹 Chargement de l'image depuis : {chemin_image}")

        openImag = Image.open(chemin_image).convert("RGBA")
        dim = openImag.resize((500, 800))

        # 🔹 Stocke l’image dans la nouvelle fenêtre
        winDiag.imageDiag = ImageTk.PhotoImage(dim)

        B = Button(frame_diagnostique, image=winDiag.imageDiag)
        B.image = winDiag.imageDiag  # 🔹 Stocker une référence pour éviter la suppression
        B.grid(row=0,column=0)

    except Exception as e:
        print(f"❌ Erreur : {e}")
        Label(frame_diagnostique, text=f"Erreur : {e}", fg="red").grid()

    winDiag.mainloop()

diag=Frame(fenetre,bg="#7EC0EE", relief=RIDGE, bd=3)
diag.grid(row=1, column=4, columnspan=4, padx=20,ipadx=40 ,pady=20)
try:
  ouvrir_imgSup=Image.open("diagnostic.png")
  newdim=ouvrir_imgSup.resize((150,150))
  newimage=ImageTk.PhotoImage(newdim)
except FileNotFoundError:
    print("image diagnostic n'existe pas")
    newimage=None
if newimage:
    Bdiag = Button(diag, image=newimage,bg="#7EC0EE",relief=FLAT,command=diagnostics)
    Bdiag.image = newimage # Garder une référence
    Bdiag.grid(row=0, column=1, padx=20)
TXT= Label(diag,text="     diagnostiques     ",fg="black",font="Hevatica 20 bold",bg="#7EC0EE") 
TXT.grid(row=1,column=1,padx=20, pady=20) 



###############" symptomes ##################################
def enrgSymptomes(ecrireCIN,ecrireSymptomes,ecriredate):
    cin=ecrireCIN.get()
    symptome=ecrireSymptomes.get("1.0","end-1c").strip()
    date=ecriredate.get_date()
    dateForma=date.strftime("%Y-%m-%d")

    try:
       con=mysql.connector.connect(host=host,user=user,password=password,database=database)
       cursor=con.cursor()
       cursor.execute("SELECT cin FROM patients where cin=%s ",(cin,))
       resultat=cursor.fetchone()
       if resultat:
           requete="INSERT INTO symptômes(symptômes_descriptions,patient_id,date)values(%s,%s,%s)"
           valeurs=(symptome,cin,dateForma)
           cursor.execute(requete,valeurs)
           con.commit()
           messagebox.showinfo( "succes","symptomes ajouté avec succès.")

           
       else:
         messagebox.showerror("error","Veuillez d'abord  ajouter le patient")

    except mysql.connector.Error as err:
         messagebox.showerror("Erreur", f"Erreur lors de l'ajout du symptomes : {err}")

    finally:
        if con and con.is_connected():
            cursor.close()
            con.close()
       

def ajouterSymptomes():
    winSymptomes=Toplevel()
    winSymptomes.geometry("2005x1000")
    winSymptomes.config(bg="#A4D3EE")

    

    cadretitre=Frame( winSymptomes,bg="#87CEFA" , relief=RAISED, bd=3 ,width=100)
    cadretitre.grid(row=0,column=0,columnspan=6 ,sticky="we")
    
    titre=Label(cadretitre,text="----------------------------------------------------------- Enregistrer les symptomes----------------------------------------------------",bg="#87CEFA",fg="black",font="Helvatica 20 bold")
    titre.grid(row=0,column=1,columnspan=4)

    try:
        ouvrir_image=Image.open("ImgSymp.png")
        newDim=ouvrir_image.resize((350,600))
        nvimage=ImageTk.PhotoImage(newDim)
    except FileNotFoundError:
          print("image symptomes n'existe pas")
          nvimage=None
    if nvimage:
           Bmodify=Label(winSymptomes,image=nvimage,bg="#A4D3EE" )
           Bmodify.image=nvimage
           Bmodify.grid(row=1, column=0,rowspan=4, padx=5)

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_from_text(event):
        ecriredate.focus()
        return "break"

    CIN = Label(winSymptomes, text="CIN :     ", bg="#A4D3EE", font="Helvatica 12 bold")
    CIN.grid(row=1, column=1, columnspan=4)

    ecrireCIN = Entry(winSymptomes, width=35)
    ecrireCIN.grid(row=1, column=3, ipady=6, ipadx=15, columnspan=4)
    ecrireCIN.bind("<Return>", focus_next_widget)

    symptomes = Label(winSymptomes, text="Les symptômes : ", bg="#A4D3EE", font="Helvatica 12 bold")
    symptomes.grid(row=2, column=1, columnspan=4)

    ecrireSymptomes = Text(winSymptomes, width=30, height=2)
    ecrireSymptomes.grid(row=2, column=3, padx=5, columnspan=4)
    ecrireSymptomes.bind("<Return>", focus_from_text)

    date = Label(winSymptomes, text="Date : ", bg="#A4D3EE", font="Helvatica 12 bold")
    date.grid(row=3, column=1, columnspan=4)

    ecriredate = tkcalendar.DateEntry(winSymptomes, width=35)
    ecriredate.grid(row=3, column=3, padx=5, columnspan=4)
    ecriredate.bind("<Return>", focus_next_widget)


    Benrg=Button(winSymptomes,text="enregistrer",font="hevatica 12 bold",bg="blue",fg="white",command=lambda:enrgSymptomes(ecrireCIN,ecrireSymptomes,ecriredate))
    Benrg.grid(row=4,column=2,columnspan=4,ipadx=8)

modify=Frame(fenetre,bg="#7EC0EE", relief=RIDGE, bd=3)
modify.grid(row=2, column=0, columnspan=4, padx=20,ipadx=40, pady=20)
try:
    ouvrir_image=Image.open("symptomes.png")
    newDim=ouvrir_image.resize((150,150))
    nvimage=ImageTk.PhotoImage(newDim)
except FileNotFoundError:
    print("image symptomes n'existe pas")
    nvimage=None
if nvimage:
    Bmodify=Button(modify,image=nvimage,bg="#7EC0EE",relief=FLAT,command=ajouterSymptomes )
    Bmodify.image=nvimage
    Bmodify.grid(row=0, column=1, padx=20)
TXT=Label(modify,text="     les symptômes    ",bg="#7EC0EE",font="hevatica 20 bold") 
TXT.grid(row=1,column=1,padx=20, pady=20)

##################### traitement ##############################

def enregistrerTraitement(entryCin,entrymedicament,entrydose,entryfrequence,entryEffets_Secondaires,entryduree,entrydate_debut):
    cin=entryCin.get()
    medicament=entrymedicament.get()
    dose=entrydose.get()
    frequence=entryfrequence.get()
    Effets_Secondaires=entryEffets_Secondaires.get()
    duree=entryduree.get()
    date_debut=entrydate_debut.get_date()

    try:
        conn=mysql.connector.connect(host=host,user=user,password=password,database=database)
        cursor=conn.cursor()
        recuperer_idDiag= """
                SELECT id_diagnostique 
                FROM diagnostiques 
                WHERE id_patient = %s 
                ORDER BY id_diagnostique DESC 
                LIMIT 1
                 """
        cursor.execute(recuperer_idDiag,(cin,))
        idDiag=cursor.fetchone()
        if idDiag:
            inser="INSERT INTO traitements(ID_Diagnostique,nom_médicament,Durée,Effets_Secondaires,cin,dose,fréquence,date_debut)values(%s,%s,%s,%s,%s,%s,%s,%s)"
            valeurs=(idDiag[0],medicament,duree,Effets_Secondaires,cin,dose,frequence,date_debut)
            cursor.execute(inser,valeurs)
        else:
            messagebox.showerror("error","veuillez d'abord enregisrer les diagnostiques de ce patient")

        conn.commit()

        messagebox.showinfo( "succes","Traitement ajouté avec succès.")

        
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur lors de l'ajout du Traitement: {err}")

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
def ajouter_traitement():
    winTraitement=Toplevel()
    winTraitement.title("Traitement")
    winTraitement.geometry("2005x1000")
    winTraitement.iconbitmap("sante.ico")
    winTraitement.config(bg="#A4D3EE")

    framTrait=Frame(winTraitement,bg="#A4D3EE",relief="raised",bd=3)
    framTrait.grid(row=0,column=1,columnspan=6,rowspan=6,padx=50,pady=10,ipadx=80, sticky="nswe")

    framTitre=Frame(framTrait,bg="#87CEFA" ,relief=RAISED,bd=3)
    framTitre.grid(row=0,column=0, columnspan=6, sticky="we")
    titre=Label(framTitre,text="  Ajouter un traitement-------------------------------------------------------------------------------------------------------",bg="#87CEFA",font="helvatica 20 bold")
    titre.grid(row=0 ,column=1)
    try:
        ouvrImgT=Image.open("iconTraitement.png")
        dim=ouvrImgT.resize((50,50))
        monImg=ImageTk.PhotoImage(dim)
    except FileNotFoundError:
        print("image traitement n'existe pas")
        monImg=None
    if monImg:
        photo=Label(framTitre,image=monImg,bg="#87CEFA")
        photo.image=monImg
        photo.grid(row=0,column=0,padx=10)

    def focus_next(event):
        event.widget.tk_focusNext().focus()
        return "break"

    cin = Label(framTrait, text="CIN de patient   :", bg="#A4D3EE", font="helvatica 12 bold")
    cin.grid(row=1, column=1, pady=40)
    entryCin = Entry(framTrait, width=40)
    entryCin.grid(row=1, column=2, pady=20)
    entryCin.bind("<Return>", focus_next)

    medicament = Label(framTrait, text="Nom du médicament  :", bg="#A4D3EE", font="helvatica 12 bold")
    medicament.grid(row=2, column=1, pady=20)
    entrymedicament = Entry(framTrait, width=40)
    entrymedicament.grid(row=2, column=2, pady=20)
    entrymedicament.bind("<Return>", focus_next)

    dose = Label(framTrait, text="La dose  :", bg="#A4D3EE", font="helvatica 12 bold")
    dose.grid(row=3, column=1, pady=20)
    entrydose = Entry(framTrait, width=40)
    entrydose.grid(row=3, column=2, pady=20)
    entrydose.bind("<Return>", focus_next)

    frequence = Label(framTrait, text="Fréquence  :", bg="#A4D3EE", font="helvatica 12 bold")
    frequence.grid(row=4, column=1, pady=20)
    entryfrequence = Entry(framTrait, width=40)
    entryfrequence.grid(row=4, column=2, pady=20)
    entryfrequence.bind("<Return>", focus_next)

    Effets_Secondaires = Label(framTrait, text="Les effets secondaires  :", bg="#A4D3EE", font="helvatica 12 bold")
    Effets_Secondaires.grid(row=5, column=1, pady=20)
    entryEffets_Secondaires = Entry(framTrait, width=40)
    entryEffets_Secondaires.grid(row=5, column=2, pady=20)
    entryEffets_Secondaires.bind("<Return>", focus_next)

    duree = Label(framTrait, text="Durée de traitement  :", bg="#A4D3EE", font="helvatica 12 bold")
    duree.grid(row=6, column=1, pady=20)
    entryduree = Entry(framTrait, width=40)
    entryduree.grid(row=6, column=2, pady=20)
    entryduree.bind("<Return>", focus_next)

    date_debut = Label(framTrait, text="Date début  :", bg="#A4D3EE", font="helvatica 12 bold")
    date_debut.grid(row=7, column=1, pady=20)
    entrydate_debut = tkcalendar.DateEntry(framTrait, width=40)
    entrydate_debut.grid(row=7, column=2, pady=20)
    entrydate_debut.bind("<Return>", focus_next)


    enregestrerTraitement= Button(framTrait ,text="Enregistrer",font="helvatica 12 bold ",bg="#007FFF",command= lambda:enregistrerTraitement(entryCin,entrymedicament,entrydose,entryfrequence,entryEffets_Secondaires,entryduree,entrydate_debut))
    enregestrerTraitement.grid(row=9,column=0 ,columnspan=3 ,ipadx=10 , padx=10,pady=40 )



    try:
        ouvrImgM=Image.open("C.webp")
        dim=ouvrImgM.resize((100,80))
        monImag=ImageTk.PhotoImage(dim)
    except FileNotFoundError:
        print("image traitement n'existe pas")
        monImag=None
    if monImag:
        photo=Label(framTrait,image=monImag,bg="#A4D3EE")
        photo.image=monImag
        photo.grid(row=1,column=4,padx=100)

    try:
        ouvrImgM=Image.open("C.webp")
        dim=ouvrImgM.resize((100,80))
        monImag=ImageTk.PhotoImage(dim)
    except FileNotFoundError:
        print("image traitement n'existe pas")
        monImag=None
    if monImag:
        photo=Label(framTrait,image=monImag,bg="#A4D3EE")
        photo.image=monImag
        photo.grid(row=6,column=4,padx=100)

    try:
        ouvrImgM=Image.open("TRAIT.png")
        dim=ouvrImgM.resize((100,90))
        monImag=ImageTk.PhotoImage(dim)
    except FileNotFoundError:
        print("image traitement n'existe pas")
        monImag=None
    if monImag:
        photo=Label(framTrait,image=monImag,bg="#A4D3EE")
        photo.image=monImag
        photo.grid(row=3,column=4,padx=100)

   

    winTraitement.mainloop()

trait=Frame(fenetre,bg="#7EC0EE", relief=RIDGE, bd=3)
trait.grid(row=1, column=8, columnspan=4, padx=50,ipadx=40, pady=20)
try:
    ouvrir=Image.open("traitement.png")
    newDim=ouvrir.resize((150,150))
    image=ImageTk.PhotoImage(newDim)
except FileNotFoundError:
    print("image traitement n'existe pas")
    image=None
if image:
    Btrait=Button(trait,image=image,bg="#7EC0EE",relief=FLAT,command=ajouter_traitement )
    Btrait.image=image
    Btrait.grid(row=0, column=1, padx=20)
TXT=Label(trait,text="        traitement          ",bg="#7EC0EE",font="hevatica 20 bold") 
TXT.grid(row=1,column=1,padx=20, pady=20)

##################### statistique ##############################
def statistique_med():
    """
    Affiche une nouvelle fenêtre avec des statistiques médicales :
    - Un graphique à barres du nombre de patients par maladie.
    - Un grand graphique circulaire de la répartition de l'âge par maladie.
    - Un grand graphique circulaire de la répartition du sexe par maladie.
    """
    winStatistique = Toplevel()
    winStatistique.geometry("2005x1000")  # Ajuster la largeur de la fenêtre
    winStatistique.title("Statistiques Médicales")
    try:
        winStatistique.iconbitmap("sante.ico")
    except:
        print("Le fichier 'sante.ico' est introuvable.")
    winStatistique.config(bg="#A4D3EE")
    # --- Section 1: Nombre de patients par maladie (affichant seulement les maladies avec des patients) ---
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)

        # Requête SQL
        query_maladie = """
            SELECT nom_maladie, COUNT(DISTINCT patient_id) AS Nombre_Patients
            FROM maladie
            GROUP BY nom_maladie
            HAVING COUNT(DISTINCT patient_id) > 0
        """
        df_maladie = pd.read_sql(query_maladie, conn)

        if not df_maladie.empty:
            # Création du graphique à barres (amélioré)
            fig_maladie, ax_maladie = plt.subplots(figsize=(10, 5))  # Agrandir la figure
            ax_maladie.bar(df_maladie['nom_maladie'], df_maladie['Nombre_Patients'], color='skyblue')
            ax_maladie.set_xlabel("Maladie", fontsize=14)
            ax_maladie.set_ylabel("Nombre de Patients", fontsize=14)
            ax_maladie.set_title("Nombre de Patients par Maladie", fontsize=16, fontweight='bold')
            plt.xticks(rotation=45, ha="right", fontsize=10)  # Ajuster la taille de la police
            plt.tight_layout()

            # Frame pour le graphique principal (nombre de patients par maladie)
            frame_stats_principal = Frame(winStatistique, bg="#EEE5DE", bd=2, relief=SOLID)
            frame_stats_principal.grid(row=0, column=0,columnspan=2, pady=5,ipady=120,ipadx=20, sticky="nsew")

            # Intégration du graphique principal dans Tkinter
            canvas_principal = FigureCanvasTkAgg(fig_maladie, master=frame_stats_principal)
            canvas_principal.draw()
            widget_principal = canvas_principal.get_tk_widget()
            widget_principal.grid(row=0, column=0, sticky="nsew")

            # Rendre le frame principal extensible
            frame_stats_principal.grid_rowconfigure(0, weight=1)
            frame_stats_principal.grid_columnconfigure(0, weight=1)
        else:
            label_pas_de_maladie = Label(winStatistique, text="Aucune maladie avec des patients à afficher.", font=("Helvetica", 12), bg="#A4D3EE")
            label_pas_de_maladie.grid(row=0, column=0, padx=20, pady=20)

    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données: {err}")
        erreur_label = Label(winStatistique, text="Erreur de connexion à la base de données.", fg="red")
        erreur_label.grid(row=0, column=0, padx=20, pady=20)
        return
    except Exception as e:
        print(f"Une erreur est survenue lors de la création du graphique principal: {e}")
        erreur_label = Label(winStatistique, text="Erreur lors de la création du graphique principal.", fg="red")
        erreur_label.grid(row=0, column=0, padx=20, pady=20)
        return

    # --- Section 2: Répartition de l'âge par maladie (un seul camembert) ---
    try:
        # Nouvelle connexion à la base de données
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)

        # Requête SQL pour récupérer l'âge et la maladie de tous les patients
        query_age_par_maladie = """
            SELECT p.date_naissance, m.nom_maladie
            FROM patients p
            JOIN maladie m ON p.cin = m.patient_id
        """
        df_age_par_maladie = pd.read_sql(query_age_par_maladie, conn)
        conn.close()

        # Nettoyage et conversion des données
        df_age_par_maladie['date_naissance'] = pd.to_datetime(df_age_par_maladie['date_naissance'], errors='coerce')
        df_age_par_maladie['nom_maladie'] = df_age_par_maladie['nom_maladie'].astype(str)
        df_age_par_maladie.dropna(subset=['date_naissance', 'nom_maladie'], inplace=True)
        df_age_par_maladie = df_age_par_maladie[df_age_par_maladie['date_naissance'].notna()]

        # Calcul de l'âge
        today = datetime.today()
        df_age_par_maladie['âge'] = df_age_par_maladie['date_naissance'].apply(
            lambda d: today.year - d.year - ((today.month, today.day) < (d.month, d.day))
        )

        # Tranches d’âge
        bins = [1, 18, 35, 50, 65, 100]
        labels_age = ['1-18', '19-35', '36-50', '51-65', '66+']
        df_age_par_maladie['tranche_age'] = pd.cut(df_age_par_maladie['âge'], bins=bins, labels=labels_age, right=False).astype(str)

        # Combinaison de la maladie et de la tranche d'âge pour les étiquettes
        df_age_par_maladie['maladie_age'] = df_age_par_maladie['nom_maladie'] + ' - ' + df_age_par_maladie['tranche_age']

        # Comptage des patients par combinaison maladie-âge
        age_par_maladie_counts = df_age_par_maladie['maladie_age'].value_counts().fillna(0)

        # Création du graphique circulaire pour la répartition de l'âge par maladie
        fig_age_par_maladie, ax_age_par_maladie = plt.subplots(figsize=(8, 8))
        ax_age_par_maladie.pie(age_par_maladie_counts.values, labels=age_par_maladie_counts.index, autopct='%1.1f%%', startangle=90)
        ax_age_par_maladie.set_title("Répartition de l'Âge par Maladie", fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Frame pour le graphique de la répartition de l'âge par maladie
        frame_age_par_maladie = Frame(winStatistique, bg="white", bd=2, relief=SOLID)
        frame_age_par_maladie.grid(row=1, column=0, padx=20, pady=20,ipady=20, sticky="nsew")

        # Intégration du graphique de l'âge par maladie dans Tkinter
        canvas_age_par_maladie = FigureCanvasTkAgg(fig_age_par_maladie, master=frame_age_par_maladie)
        canvas_age_par_maladie.draw()
        widget_age_par_maladie = canvas_age_par_maladie.get_tk_widget()
        widget_age_par_maladie.grid(row=0, column=0, sticky="nsew")

        # Rendre le frame de l'âge par maladie extensible
        frame_age_par_maladie.grid_rowconfigure(0, weight=1)
        frame_age_par_maladie.grid_columnconfigure(0, weight=1)

    except mysql.connector.Error as err:
        print(f"Une erreur de connexion à la base de données (âge par maladie) est survenue: {err}")
        erreur_label = Label(winStatistique, text=f"Erreur de connexion à la base de données (âge par maladie): {err}", fg="red")
        erreur_label.grid(row=1, column=0, padx=20, pady=20)
    except Exception as e:
        print(f"Une erreur est survenue lors de la création du graphique de l'âge par maladie: {e}")
        erreur_label = Label(winStatistique, text=f"Erreur lors de la création du graphique de l'âge par maladie: {e}", fg="red")
        erreur_label.grid(row=1, column=0, padx=20, pady=20)

    # --- Section 3: Répartition du sexe par maladie (un seul camembert) ---
    try:
        # Nouvelle connexion à la base de données
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)

        # Requête SQL pour récupérer le sexe et la maladie de tous les patients
        query_sexe_par_maladie = """
            SELECT p.gender, m.nom_maladie
            FROM patients p
            JOIN maladie m ON p.cin = m.patient_id
        """
        df_sexe_par_maladie = pd.read_sql(query_sexe_par_maladie, conn)
        conn.close()

        # Nettoyage et conversion des données
        df_sexe_par_maladie['gender'] = df_sexe_par_maladie['gender'].astype(str)
        df_sexe_par_maladie['nom_maladie'] = df_sexe_par_maladie['nom_maladie'].astype(str)
        df_sexe_par_maladie.dropna(subset=['gender', 'nom_maladie'], inplace=True)
        df_sexe_par_maladie = df_sexe_par_maladie[df_sexe_par_maladie['gender'].notna() & (df_sexe_par_maladie['gender'] != '')]

        # Combinaison de la maladie et du sexe pour les étiquettes
        df_sexe_par_maladie['maladie_sexe'] = df_sexe_par_maladie['nom_maladie'] + ' - ' + df_sexe_par_maladie['gender']

        # Comptage des patients par combinaison maladie-sexe
        sexe_par_maladie_counts = df_sexe_par_maladie['maladie_sexe'].value_counts().fillna(0)

        # Création du graphique circulaire pour la répartition du sexe par maladie
        fig_sexe_par_maladie, ax_sexe_par_maladie = plt.subplots(figsize=(8, 8))
        ax_sexe_par_maladie.pie(sexe_par_maladie_counts.values, labels=sexe_par_maladie_counts.index, autopct='%1.1f%%', colors=["lightblue", "lightpink"], startangle=90)
        ax_sexe_par_maladie.set_title("Répartition du Sexe par Maladie", fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Frame pour le graphique de la répartition du sexe par maladie
        frame_sexe_par_maladie = Frame(winStatistique, bg="white", bd=2, relief=SOLID)
        frame_sexe_par_maladie.grid(row=1, column=1, padx=20, pady=20,ipady=40, sticky="nsew")

        # Intégration du graphique du sexe par maladie dans Tkinter
        canvas_sexe_par_maladie = FigureCanvasTkAgg(fig_sexe_par_maladie, master=frame_sexe_par_maladie)
        canvas_sexe_par_maladie.draw()
        widget_sexe_par_maladie = canvas_sexe_par_maladie.get_tk_widget()
        widget_sexe_par_maladie.grid(row=0, column=0, sticky="nsew")

        # Rendre le frame du sexe par maladie extensible
        frame_sexe_par_maladie.grid_rowconfigure(0, weight=1)
        frame_sexe_par_maladie.grid_columnconfigure(0, weight=1)

    except mysql.connector.Error as err:
        print(f"Une erreur de connexion à la base de données (sexe par maladie) est survenue: {err}")
        erreur_label = Label(winStatistique, text=f"Erreur de connexion à la base de données (sexe par maladie): {err}", fg="red")
        erreur_label.grid(row=1, column=1, padx=20, pady=20)
    except Exception as e:
        print(f"Une erreur est survenue lors de la création du graphique du sexe par maladie: {e}")
        erreur_label = Label(winStatistique, text=f"Erreur lors de la création du graphique du sexe par maladie: {e}", fg="red")
        erreur_label.grid(row=1, column=1, padx=20, pady=20)

    winStatistique.grid_rowconfigure(0, weight=1)
    winStatistique.grid_columnconfigure(0, weight=1)
    winStatistique.grid_columnconfigure(1, weight=1)
    winStatistique.grid_rowconfigure(1, weight=1)
    winStatistique.mainloop()

statistique=Frame(fenetre,bg="#7EC0EE", relief=RIDGE, bd=3)
statistique.grid(row=2, column=8, columnspan=4, padx=50,ipadx=40, pady=20)
try:
    ouvrir=Image.open("sta.png")
    newDim=ouvrir.resize((150,150))
    image=ImageTk.PhotoImage(newDim)
except FileNotFoundError:
    print("image statistique n'existe pas")
    image=None
if image:
    Bstat=Button(statistique,image=image,bg="#7EC0EE",relief=FLAT ,command=statistique_med)
    Bstat.image=image
    Bstat.grid(row=0, column=1, padx=20)
TXT=Label(statistique,text="  voir les statistique   ",bg="#7EC0EE",font="hevatica 20 bold") 
TXT.grid(row=1,column=1,padx=20, pady=20)





fenetre.mainloop()
