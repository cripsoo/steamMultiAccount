import tkinter as tk
import os
import subprocess
import functools
import sys
from tkinter import simpledialog
import webbrowser
import cryptography
from cryptography.fernet import Fernet

program_name = 'steamMultiAccount'
program_version = '2.0'

steam_path = r'C:\Program Files (x86)\Steam'

# Paramètres de base
root = tk.Tk()
root.title(f'{program_name} v{program_version}')
root.iconbitmap('icon.ico')
root.minsize(350,250)
fenetre = tk.Canvas(root, width = 350, height = 0) 
fenetre.pack()

# Fonctions
def connexion(compte,mdp):
	subprocess.call('taskkill /IM "Steam.exe" /F',creationflags=subprocess.CREATE_NO_WINDOW)
	subprocess.Popen(f'cd {steam_path} & start steam.exe -login "{compte}" "{mdp}"',shell=True,creationflags = subprocess.CREATE_NO_WINDOW)

def ajouterCompte():
	user_input = simpledialog.askstring('Ajouter un compte','identifiant:motdepasse')
	if user_input != None:
		if user_input != '' and ':' in user_input:
			nom_fichier = user_input.split(':',1)[0]
			f = open(f'acc-{nom_fichier}.txt',"wb")
			f.write(encrypt(user_input))
			f.close()
			redemarrer_prog()

def supprimerCompte():
	user_input = simpledialog.askstring('Supprimer un compte','Entrer l\'identifiant:')
	if os.path.exists(f"acc-{user_input}.txt"):
  		os.remove(f"acc-{user_input}.txt")
  		redemarrer_prog()

def redemarrer_prog():
    python = sys.executable
    script = os.path.realpath(__file__)
    subprocess.Popen([python, script])
    root.quit()

def about():
	tk.messagebox.showinfo("A propos", "Programme par CRIPSO\nsteamcommunity.com/id/CripsoCS")

def checkForUpdates():
	webbrowser.open('https://github.com/cripsoo/steamMultiAccount/releases')

	#Encryption
def createKey():
	key = Fernet.generate_key()

	file = open('doNotDelete.needed', 'wb')
	file.write(key)
	file.close()

def readKey():
	file = open('doNotDelete.needed','rb')
	key = file.read()
	file.close()
	return key

def encrypt(data):
	data = str.encode(data) #On veut des btyes et non un string
	return Fernet(key).encrypt(data)

def decrypt(file):
	with open(file,'rb') as f:
		data = f.read()

	data = Fernet(key).decrypt(data)

	return data.decode('utf-8')

# Menu bar
menubar = tk.Menu(root)

	#Ajouter/Supprimer compte
menubar.add_command(label = "Ajouter un compte", command=ajouterCompte)
menubar.add_command(label = "Supprimer un compte", command=supprimerCompte)

	# Aide
menu_aide = tk.Menu(menubar, tearoff = 0)
menu_aide.add_command(label="Actualiser",command=redemarrer_prog)
menu_aide.add_command(label="Mise à jour",command=checkForUpdates)
menu_aide.add_command(label="A propos",command=about)
menubar.add_cascade(label="Aide", menu=menu_aide)


root.config(menu=menubar)


# Pour retrouver les comptes existants et créer les buttons
nb_boutons = 0
HAUTEUR = 30
src = ".\\"
files = os.listdir(src)

if 'doNotDelete.needed' not in files:
	createKey()

key = readKey()

for file in files:

	if 'acc-' in file and os.path.splitext(file)[1] == '.txt':
		#On ajoute le bouton du compte
		identifiants = decrypt(file).split(':',1) #on récupère [id,mdp] depuis le fichier texte avec id:mdp
		nom_bouton = os.path.splitext(file)[0].replace('acc-','')

		fenetre.create_window(170, HAUTEUR, window=tk.Button(root, text=nom_bouton, width = 52, activebackground='#b3b2b1', font='Courrier 12 bold',command=functools.partial(connexion,identifiants[0],identifiants[1])).pack())
		nb_boutons += 1
		HAUTEUR += 30

if nb_boutons == 0:
	text_noAccounts = tk.Label(root, height=2, width=30,font='Courrier 12 bold',text='"Aucun compte détecté."')
	text_noAccounts.pack()

root.mainloop()
