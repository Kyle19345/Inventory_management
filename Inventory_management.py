
from tkinter import *
from tkinter import messagebox,filedialog
import sqlite3
from datetime import date
from tkinter import simpledialog
import os


class Base_de_donne:
    def nouvelle_base(self):
        fichier=filedialog.asksaveasfilename(defaultextension=".db",filetypes=[('fichier SQLite',"*.db")])
        if fichier:
            try:
                self.com=sqlite3.connect(fichier)
                self.cur=self.com.cursor()
                self.cur.execute('''
                         CREATE TABLE IF NOT EXISTS ma_base(
                             ID INTEGER NOT NULL,
                             nom TEXT NOT NULL,
                             categorie TEXT NOT NULL,
                             quantite INTEGER NOT NULL,
                             prix INTEGER NOT NULL,
                             date_ajout TEXT NOT NULL,
                             exp TEXT NOT NULL,
                             fournisseur TEXT NOT NULL,
                             contact INTEGER NOT NULL,
                             description TEXT NOT NULL
                         )
                         ''')
                self.com.commit()
            except Exception as e:
                messagebox.showerror("Erreur",str(e))
        
    def ouvrir_base(self):
        fichier=filedialog.askopenfilename(filetypes=[("Fichier SQLite","*.db")])
        if fichier:
            if os.path.exists(fichier):
                try:
                    self.com=sqlite3.connect(fichier)
                    self.cur=self.com.cursor()
                except Exception as e:
                    messagebox.showerror("Erreur",str(e))
            else:
                messagebox.showerror("Erreur","Fichier introuvable")                
    
    def ajouter_produit(self, ID, nom,categorie,quantite, prix, date_ajout, exp, nom_fournisseur, contact, description):
        self.cur.execute("INSERT INTO ma_base(ID, nom,categorie,quantite,prix, date_ajout, exp, fournisseur, contact, description) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (ID, nom,categorie, quantite, prix, date_ajout, exp, nom_fournisseur, contact, description))
        print('data inserted')
        self.com.commit()


    def ajouter(self,nom,val):
        self.cur.execute('SELECT quantite FROM ma_base WHERE nom = ?', (nom,))
        resultat = self.cur.fetchone()
        if not resultat:
                return "Produit introuvable"
        qt = int(resultat[0])
        self.cur.execute("UPDATE ma_base SET quantite = ? WHERE nom = ?", (qt + val, nom))
        self.com.commit()
        return "OK"
    
    def soustraire(self,nom,val):
        self.cur.execute('SELECT quantite from ma_base WHERE nom = ?',(nom,))
        resultat=self.cur.fetchone()
        if not resultat: 
            return "Produit introuvable"
        qt=int(resultat[0])
        if val > qt:
            return "Quantité insuffisante"
        self.cur.execute("UPDATE ma_base SET quantite = ? WHERE nom = ?",(qt-val,nom))
        self.com.commit()
        return 'OK'
        
    def supprimer(self,nom):
        self.cur.execute("SELECT * FROM ma_base WHERE nom = ?", (nom,))
        resultat = self.cur.fetchone()
        if resultat is None:
            return "Produit introuvable"
        else:
            self.cur.execute("DELETE FROM ma_base WHERE nom = ?", (nom,))
            self.com.commit()
            return "OK"
    
    def trier_par_quantite(self):
        self.cur.execute("SELECT * FROM ma_base ORDER BY quantite ASC")  # ASC = croissant, DESC = décroissant
        return self.cur.fetchall()

    def rechercher_produits(self, texte):
        self.cur.execute("SELECT * FROM ma_base WHERE nom LIKE ? OR categorie LIKE ?", 
                        (f"%{texte}%", f"%{texte}%"))
        return self.cur.fetchall()
    
class Menubar(Frame):
    def __init__(self,boss):
        Frame.__init__(self,bg="#121212",borderwidth=1)
        fileMenu=Menubutton(self,text='Menu',bg="#121212",fg="#e0e0e0",activebackground="#2c2c2c",activeforeground="#e0e0e0")
        fileMenu.grid(row=0,column=1)
        me1=Menu(fileMenu,tearoff=0, bg="#2c2c2c", fg="#e0e0e0",
                     activebackground="#2c2c2c", activeforeground="#e0e0e0")
        me1.add_command(label='Accueil',underline=0,command=boss.homepage)
        me1.add_command(label='Liste produits',underline=0,command=boss.fenliste_produit)
        fileMenu.configure(menu=me1)
        
        fileMenu2=Menubutton(self,text='Fichier',bg="#121212",fg="#e0e0e0",activebackground="#2c2c2c",activeforeground="#e0e0e0")
        fileMenu2.grid(row=0,column=0)
        me2=Menu(fileMenu2,tearoff=0, bg="#2c2c2c", fg="#e0e0e0",
                     activebackground="#2c2c2c", activeforeground="#e0e0e0")
        me2.add_command(label='Ouvrir',command=boss.Inventaire.ouvrir_base)
        me2.add_command(label='Nouveau',command=boss.Inventaire.nouvelle_base)
        fileMenu2.configure(menu=me2)
        
class Interface:
    def __init__(self,master):
        self.Inventaire=Base_de_donne()
        # Thème "Dark Mode Tech"
        self.couleurs = {
            "frame": "#121212",         # fond principal
            "fg": "#e0e0e0",         # texte
            "bg": "#1e1e1e",      # fond des cadres
            "entry": "#2c2c2c",      # fond des entrées
            "button": "#3a3a3a",     # fond des boutons
            "accent": "#00bcd4",     # couleur accent
            "hover": "#4caf50"       # survol bouton
        }
        self.master=master
        self.master.title("Gestion Inventaire")
        
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(2,weight=1)
        
        self.police=("Segoe UI",11)
        
        self.taille_fen=1380
        
        #fen titre
        self.fen_ttr=Frame(self.master,relief="flat",height=100,width=self.taille_fen,bg=self.couleurs["frame"])
        self.text=Label(self.fen_ttr,text="🛒 Inventory Management System",bg=self.couleurs["frame"],fg=self.couleurs['fg'],font=("Segoe UI", 24, "bold"))
        self.text.grid(row=0,column=0,columnspan=3,sticky='ew',padx=30,pady=5)
        self.fen_ttr.grid(row=1,column=0,columnspan=2,sticky='nsew')
        
        #fen principal
        self.fen_ajout=Frame(self.master,relief='groove',bg=self.couleurs["bg"],width=700,height=450)
        self.fen_ajout.grid_propagate(FALSE)
        self.fen_ajout.grid_columnconfigure(0,weight=1)
        
        #fen liste produit
        self.fen_lst=Frame(self.master,width=self.taille_fen,height=400,bg=self.couleurs["bg"])
        self.fen_lst.grid_propagate(FALSE)
        self.fen_lst.grid_columnconfigure(0,weight=1)
     
        
        self.menu=Menubar(self)
        self.menu.grid(row=0,column=0,sticky='ew')
        
        self.page_ajout()
    
    def page_ajout(self):
        #fen principal
        self.fen1=Frame(self.fen_ajout,relief="groove",width=700,height=450,bg=self.couleurs['bg'])
        self.fen1.grid_propagate(FALSE)
        self.fen1.grid_columnconfigure(0,weight=1)
        
        self.txt_ID=Label(self.fen1,text='ID',bg=self.couleurs['bg'],fg=self.couleurs['fg'],font=self.police)
        self.txt_ID.grid(row=0,column=0,pady=(20,0),padx=(150,0),sticky="W")
        self.ID=Entry(self.fen1,width=40,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.ID.grid(row=0,column=1,pady=(20,0),padx=(5,130),sticky="w")
    
        self.txt_categorie=Label(self.fen1,text="Catégorie",bg=self.couleurs['bg'],fg=self.couleurs['fg'],font=self.police)
        self.txt_categorie.grid(row=2,column=0,pady=5,padx=(150,0),sticky="W")
        self.categorie=Entry(self.fen1,width=40,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.categorie.grid(row=2,column=1,pady=5,padx=(5,130),sticky="W")
        
        self.txt_nom=Label(self.fen1,text="Nom",bg=self.couleurs['bg'],fg=self.couleurs['fg'],font=self.police)
        self.txt_nom.grid(row=1,column=0,pady=5,padx=(150,0),sticky="W")
        self.nom=Entry(self.fen1,width=40,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.nom.grid(row=1,column=1,pady=5,padx=(5,130),sticky="W")
        
        self.txt_quantite=Label(self.fen1,text="Quantité",bg=self.couleurs['bg'],fg=self.couleurs['fg'],font=self.police)
        self.txt_quantite.grid(row=3,column=0,pady=5,padx=(150,0),sticky="W")
        self.quantite=Entry(self.fen1,width=40,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.quantite.grid(row=3,column=1,pady=5,padx=(5,130),sticky="W")
        
        self.txt_prix_unitaire=Label(self.fen1,text='Prix unitaire',bg=self.couleurs['bg'],fg=self.couleurs['fg'],font=self.police)
        self.txt_prix_unitaire.grid(row=4,column=0,pady=5,padx=(150,0),sticky="W")
        self.prix_unitaire=Entry(self.fen1,width=40,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.prix_unitaire.grid(row=4,column=1,pady=5,padx=(5,130),sticky="W")
        
        self.txt_date_exp=Label(self.fen1,text="Date d'expiration",bg=self.couleurs['bg'],fg=self.couleurs['fg'],font=self.police)
        self.txt_date_exp.grid(row=5,column=0,pady=5,padx=(150,0),sticky="W")
        self.date_exp=Entry(self.fen1,width=40,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.date_exp.grid(row=5,column=1,pady=5,padx=(5,130),sticky="W")
        
        
        self.txt_nom_fournisseur=Label(self.fen1,text='Fournisseur',bg=self.couleurs['bg'],font=self.police,fg=self.couleurs['fg'])
        self.txt_nom_fournisseur.grid(row=6,column=0,pady=5,padx=(150,0),sticky="W")
        self.nom_fournisseur=Entry(self.fen1,width=40,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.nom_fournisseur.grid(row=6,column=1,pady=5,padx=(5,130),sticky="W")
        
        self.txt_contact_fournisseur=Label(self.fen1,text="Contact",bg=self.couleurs['bg'],fg=self.couleurs['fg'],font=self.police)
        self.txt_contact_fournisseur.grid(row=7,column=0,pady=5,padx=(150,0),sticky="W")
        self.contact=Entry(self.fen1,width=40,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.contact.grid(row=7,column=1,pady=5,padx=(5,130),sticky="W")
        
        self.txt_description=Label(self.fen1,text='Description',bg=self.couleurs['bg'],fg=self.couleurs['fg'],font=self.police)
        self.txt_description.grid(row=8,column=0,pady=(5,30),padx=(150,0),sticky="nw")
        self.description=Text(self.fen1,width=35,height=4,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.description.grid(row=8,column=1,pady=(5,20),padx=(5,130),sticky="W")
        
        self.bouton=Button(self.fen1,text='Ajouter',command=self.ajouter_produit, bg=self.couleurs['accent'], fg=self.couleurs['fg'], font=self.police,
                     relief="flat",width=40)
        self.bouton.grid(row=10,columnspan=2,pady=(0,20))
        self.style_button(self.bouton)

        self.fen1.grid(row=1,column=0)
        
        self.fen_ajout.grid(sticky='nsew')

    
    def fenliste_produit(self):
        #Suppression fen principal et initialisation fen liste produit
        self.fen_ajout.grid_forget()
        #fen recherche
        self.fen_recherche=Frame(self.fen_lst,relief="flat",width=self.taille_fen,height=50,bg=self.couleurs['frame'])#ausii pour modifier la taille
        self.fen_recherche.grid_propagate(FALSE)
        self.fen_recherche.grid_columnconfigure(0,weight=1)
    
        self.fen_recherche.grid(row=1,column=0,sticky="nsew")
       
        
        self.recherche=Entry(self.fen_recherche,width=60,bg=self.couleurs['entry'],fg=self.couleurs['fg'],relief=FLAT,insertbackground=self.couleurs['fg'])
        self.recherche.grid(row=0,columnspan=3,padx=(50,30),pady=(10,20),sticky="news")
        
        self.bouton_recherche=Button(self.fen_recherche,width=13,command=self.rechercher,text="🔍 Rechercher", bg=self.couleurs['accent'], fg=self.couleurs['fg'], font=self.police,
                     relief=FLAT, padx=10, pady=5)
        self.bouton_recherche.grid(row=0,column=3,padx=(0,10),pady=(0,15))
        self.style_button(self.bouton_recherche)
        
        
        self.bouton2=Button(self.fen_recherche,text="Afficher",width=13,command=self.affichage, bg=self.couleurs['accent'], fg=self.couleurs['fg'], font=self.police,
                     relief=FLAT, padx=10, pady=5)
        self.bouton2.grid(row=0,column=5,padx=(470,10),pady=(0,15))
        self.style_button(self.bouton2)
        
        self.bouton3=Button(self.fen_recherche,text='Trier par quantite',width=13,command=self.affichage_par_quantite, bg=self.couleurs['accent'], fg=self.couleurs['fg'], font=self.police,
                     relief=FLAT, padx=10, pady=5)
        self.bouton3.grid(row=0,column=7,padx=(0,30),pady=(0,15))
        self.style_button(self.bouton3)
        
        #fen liste produit
        Frame_container = Frame(self.fen_lst, bg=self.couleurs['bg'])
        Frame_container.grid(row=2, column=0, sticky='nsew')

        # Scrollbar avec couleurs personnalisées
        scrollbar = Scrollbar(
            Frame_container,
            orient=VERTICAL,
            bg=self.couleurs['fg'],               # couleur du curseur (thumb)
            troughcolor=self.couleurs['frame'],  # couleur de la "piste"
            activebackground=self.couleurs['accent'],  # couleur quand hover sur le curseur
            highlightbackground=self.couleurs['bg'],   # bordure autour scrollbar
            relief='flat',
            bd=0,
            width=16
        )
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas = Canvas(
            Frame_container,
            yscrollcommand=scrollbar.set,
            height=350,
            width=800,
            bg=self.couleurs['bg'],
            highlightthickness=0
        )
    
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)

        # Frame réel qui contient les widgets
        self.fen2 = Frame(canvas, bg=self.couleurs["bg"])
        self.fen2.grid_columnconfigure(0,weight=1)

        # Associer le frame au canvas
        canvas.create_window((0, 0), window=self.fen2, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.fen2.bind("<Configure>", on_configure)

        liste = ["ID", "Nom", "Catégorie", "Quantité", "Prix unitaire",
                "Date ajout", "Date expiration", "Fournisseur", "Contact", "Description"]

        for i in range(len(liste)):
            Label(self.fen2, text=liste[i], bg=self.couleurs["bg"], fg=self.couleurs['fg'], font=("Segoe UI",11,"bold")).grid(row=1, column=i, padx=10)
        self.fen_lst.grid(sticky='nsew')
        
    def homepage(self):
        self.fen_lst.grid_forget()
        self.fen_ajout.grid_propagate(FALSE)
        self.fen_ajout.grid_columnconfigure(0,weight=1)
        self.fen_ajout.grid(sticky='nsew')
    
    def ajouter_produit(self):
        try:
            ID=self.ID.get()
            nom=self.nom.get()
            quantite=self.quantite.get()
            prix_unitaire=self.prix_unitaire.get()
            ajout=date.today().strftime("%d/%m/%y")
            exp=self.date_exp.get()
            nom_fournisseur=self.nom_fournisseur.get()
            contact=self.contact.get()
            description=self.description.get("1.0",END)
            categorie=self.categorie.get()
            if ID == '' or nom == '' or quantite == '' or prix_unitaire == "" or nom_fournisseur == "" or contact == '' or categorie == '':
                    messagebox.showerror('ERREUR','Veuillez remplir tous les champs')
                    return

            try:
                    quantite = int(quantite)
                    prix_unitaire = float(prix_unitaire)
            except ValueError:
                    messagebox.showerror("Erreur", "Quantité et prix doivent être numériques.")
                    return

            self.Inventaire.ajouter_produit(ID, nom, categorie, quantite, prix_unitaire, ajout, exp, nom_fournisseur, contact, description)
            self.suppression_champ()
        except:
            messagebox.showerror('Erreur',"Veuillez choisir un fichier")
            

    
    def affichage(self,donnees=None):
        try:
            if donnees is None:
                self.Inventaire.cur.execute("SELECT * FROM ma_base")
                donnees = self.Inventaire.cur.fetchall()

            # Nettoyage
            for widget in self.fen2.winfo_children():
                widget.destroy()

            liste = ["ID", "Nom", "Catégorie", "Quantité", "Prix unitaire", "Date ajout", "Date expiration", "Fournisseur", "Contact", "Description"]
            for i in range(len(liste)):
                Label(self.fen2, text=liste[i],bg=self.couleurs["bg"],fg=self.couleurs['fg'],font=("Segoe UI",11,"bold")).grid(row=0, column=i, padx=15)

            for i, ligne in enumerate(donnees):
                for j, val in enumerate(ligne):
                    Label(self.fen2, text=val, bg=self.couleurs["bg"], fg=self.couleurs['fg'],
        font=self.police, width=12, wraplength=100, anchor='w', justify=LEFT).grid(row=i+1, column=j,padx=10,pady=2.5)

                nom_produit = ligne[1]
                Button(self.fen2, text="➕",font=("Segoe UI", 10, "bold"), width=3,  bg=self.couleurs['accent'], fg=self.couleurs['fg'], relief=FLAT, command=lambda p=nom_produit: self.action_ajouter(p)).grid(row=i+1, column=10,pady=2.5,padx=2)
                Button(self.fen2, text="➖",font=("Segoe UI", 10, "bold"), width=3,bg=self.couleurs['accent'], fg=self.couleurs['fg'], relief=FLAT, command=lambda p=nom_produit: self.action_soustraire(p)).grid(row=i+1, column=11,pady=2.5,padx=2)
                Button(self.fen2, text="🗑",font=("Segoe UI", 10, "bold"), width=3,bg=self.couleurs['accent'], fg=self.couleurs['fg'], relief=FLAT,command=lambda p=nom_produit: self.action_supprimer(p)).grid(row=i+1, column=12,pady=2.5,padx=2)

        except:
            messagebox.showerror('Erreur',"Veuillez Choisir un fichier")
             
    def affichage_par_quantite(self):
        try:
            donnees = self.Inventaire.trier_par_quantite()
            self.affichage(donnees)
        except:
            messagebox.showerror('Erreur',"Veuillez choisir un fichier")
        
    def rechercher(self):
        try:
            texte = self.recherche.get().strip()
            if texte == "":
                messagebox.showwarning("Recherche vide", "Veuillez entrer un mot-clé pour la recherche.")
                return
            resultats = self.Inventaire.rechercher_produits(texte)
            if not resultats:
                messagebox.showinfo("Aucun résultat", f"Aucun produit trouvé pour '{texte}'")
            self.affichage(resultats)
        except:
            messagebox.showerror('Erreur',"Veuillez choisir un fichier")
        


    def suppression_champ(self):
        self.ID.delete(0,END)
        self.nom.delete(0,END)
        self.quantite.delete(0,END)
        self.prix_unitaire.delete(0,END)
        self.date_exp.delete(0,END)
        self.nom_fournisseur.delete(0,END)
        self.contact.delete(0,END)
        self.description.delete("1.0",END)
        self.categorie.delete(0,END)
    
    def action_ajouter(self, nom):
        qte = simpledialog.askinteger("Ajouter", f"Combien ajouter à '{nom}' ?")
        if qte:
            self.Inventaire.ajouter(nom, qte)
            self.affichage()

    def action_soustraire(self, nom):
        qte = simpledialog.askinteger("Soustraire", f"Combien retirer de '{nom}' ?")
        if qte:
            resultat = self.Inventaire.soustraire(nom, qte)
            if resultat != "OK":
                messagebox.showerror("Erreur", resultat)
            self.affichage()

    def action_supprimer(self, nom):
        if messagebox.askyesno("Supprimer", f"Supprimer le produit '{nom}' ?"):
            resultat = self.Inventaire.supprimer(nom)
            if resultat != "OK":
                messagebox.showerror("Erreur", resultat)
            self.affichage()
    def style_button(self, button):
        button.bind("<Enter>", lambda e: button.config(bg=self.couleurs["hover"]))
        button.bind("<Leave>", lambda e: button.config(bg=self.couleurs["accent"]))

    
     
master=Tk()
app=Interface(master)
master.mainloop()
try:
    if hasattr(app.Inventaire, "com"):
        app.Inventaire.com.close()
except:
    pass
