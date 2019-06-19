"""
                                                Projet programmation SI4 fin de semestre
                                                             Clicker game
"""

"""
________________________________________________________Imporation des modules___________________________________________________________________

"""

import os                         # Module permettant de tester l'intégralité d'un fichier sur le système
from math import exp, floor       # Module permettant d'utiliser l'exponentielle et la troncature
from tkinter import *             # Module gérant l'interface graphique
from tkinter.messagebox import *  # Module tkinter pour afficher des popups
from typing import List           # Module pour clarifier la code en definissant les listes

"""
________________________________________________________Définition des variables___________________________________________________________________
                                
"""

balance: List[int] = [200]                 # Balance accessible dans n'importe quelle procédure (liste étant globale)
level: List[int] = [1]                     # Level du joueur qui augmente avec les clics (globale)
amelioration_cout: List[int] = []          # Liste stockant le cout des améliorations
ameliorations_possedees: List[int] = []    # Liste stockant les améliorations détenues par le jooueur
amelioration_slot: List[int] = []          # Liste contenant le nombre de slot possible pour chaque améliorations
ameliorations_gains: List[int] = []        # Stocke les gains offert par les améliorations
bloc_compte: List[str] = [""]              # Liste stockant les comptes du fichier sauvegarde
compte_actuel: List[str] = [""]            # Compte actuellement connecté (globale)
boucle_id: List[int] = [0]                 # Stocke l'ID permettant de stopper la boucle de gains
gains_cumules: List[int] = [0]             # Stocke gains cumulés de toutes les améliorations
levels_gains: List[int] = [1]              # Stocke les gains par cliques selon le level
levels_experiences: List[int] = [0]        # Stocke l'expérience requise pour monter en level
experience: List[int] = [0]                # Stocke l'experience du joueur

"""
________________________________________________________Création des procédures___________________________________________________________________

"""


def maj_gains():
    """ Calcul des gains par secondes par rapport à toutes les améliorations """

    gains_cumules[0] = 0
    for rang in range(15):  # Parcours les 15 améliorations
        gains_cumules[0] += ameliorations_gains[rang] * ameliorations_possedees[rang]  # Gains par rapport aux améliorations
    texte_gain_actuel: str = "Gains automatiques : " + str(gains_cumules[0]) + " / s"       # Texte concaténé
    canvas_usine.itemconfig(gains_automatiques_label, text=texte_gain_actuel)          # Maj du texte indicant les gains actuels


def gains_automatiques():
    """ Gains automatiques par secondes """

    maj_gains()                                             # Mise à jour de la variable et du texte des gains cumulés
    maj_balance(gains_cumules[0])                           # Mise à jour de la balance avec la valeur des gains cumulés
    maj_historique(gains_cumules[0], "Gain automatique", "automatique")
    boucle_id[0] = fenetre.after(1000, gains_automatiques)  # Boucle qui s'éxecute tout les 1000MS (1seconde), avec l'ID stocké dans boucle_id[0]


def inscription():
    """" Inscription d'un compte """

    for rang in bloc_compte:                           # Pour tous les comptes inscrits
        if entrer_pseudo.get() == rang.split(";")[0]:  # Vérification si possibilité de créer compte (doublon impossible)
            showerror("Erreur", "Le pseudo " + entrer_pseudo.get() + " est déjà utilisé.")
            break  # Casse la boucle en attente d'une nouvelle tentative
    else:
        ligne_compte = entrer_pseudo.get() + ";" + entrer_mot_de_passe.get() + ";200;1;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0"  # Inscription avec les stats de bases
        file = open("sauvegarde.txt", "a")  # Ouverture du fichier sauvegarde
        file.write("\n" + ligne_compte)     # Ecriture du nouveau compte dans le fichier sauvegarde
        file.close()                        # Fermeture du fichier
        bloc_compte.append(ligne_compte)    # Ajout du compte dans la variable regroupant tous les comptes
        showinfo("Succès", "Votre compte a bien été créée, vous pouvez maintenant vous connecter.")


def connexion():
    """ Connexion d'un compte """

    recuperation_donnees()               # Mise à jour des comptes au cas où+
    if boucle_id[0] != 0:                # Si il y a une boucle qui nous fait gagner de l'argent
        fenetre.after_cancel(boucle_id)  # On la stop pour éviter les problèmes
    if entrer_pseudo.get() == compte_actuel[0].split(";")[0]:  # Verification si déjà connecté
        showerror("Erreur", "Vous êtes déjà connecté avec ce compte")
        gains_automatiques()  # On continu la boucle de gain si on est déjà connecté
    else:
        for account in bloc_compte:
            compte_actuel[0] = account  # Compte actuel sous forme : ["user;password;level;balance;amelioration*15"]
            if (entrer_pseudo.get() == account.split(";")[0]) and (entrer_mot_de_passe.get() == account.split(";")[1]):  # Si le compte existe
                bouton_gain_manuel.config(state="normal")              # On active le bouton de gain
                historique.delete(1.0,END)                             # Effaçage de l'historique
                balance[0] = int(account.split(";")[2])                # Récuperation balance
                canvas_info.itemconfig(balance_text, text=balance[0])  # Mise à jour de l'affichage de la balance
                aff_pseudo.config(text=entrer_pseudo.get())            # Mise à jour de l'affichage du pseudo
                experience[0] = int(account.split(";")[3])             # Récupération de l'experience
                level[0] = 1                                           # Mise à 1 du level avant calcul
                for rang in range(4, 19):                              # Récupération et mise à jour des 15 améliorations
                    maj_level(0)  # Mise à jour du vrai level en fonction de l'experience
                    ameliorations_possedees[rang - 4] = int(account.split(";")[rang])
                    # On met un lambda pour pouvoir utiliser une fonction avec argument sur les bouttons
                    boutton_achat[rang - 4].config(command=lambda call_button=rang: achats_ameliorations(call_button - 4))
                maj_ameliorations()   # On met a jour les textes affichant le nombre d'améliorations
                maj_gains()           # Mise à jour de la variable et du texte des gains cumulés
                gains_automatiques()  # On lance la boucle de gains automatiques
                break
        else:
            showerror("Erreur", "Pseudo ou mot de passe incorrect")


def maj_ameliorations():
    """ Mise à jour des textes sur le nombre d'amélioration que nous avons """

    for rang in range(15):  # Mise à jour du texte des améliorations
        nouveau_texte: str = str(ameliorations_possedees[rang]) + " / " + str(amelioration_slot[rang])
        panneau_informations.itemconfig(amelioration_slot_label[rang], text=nouveau_texte)


def recuperation_donnees():
    """ Récuperation des données dans le fichier sauvegarde """

    bloc_compte[:] = []  # Suppression de toutes les valeurs dans la liste
    file = open("sauvegarde.txt", "r")  # Ouverture du fichier sauvegarde en mode lecture
    lines = file.read().splitlines()    # Lecture du fichier lignes par lignes
    for accounts in lines:              # Selection lignes par lignes
        bloc_compte.append(accounts)    # On rentre les comptes 1 par 1 dans la variable bloc_compte
    file.close()


def maj_historique(gain, type, tag):
    historique.insert(END, "( " + type + " ) : " + str(gain) + " coins\n", tag)
    historique.see(END)
    historique.bind()
    historique.bind("<1>",  "break")


def maj_balance(gain):
    """ Mise à jour de la balance """

    balance[0] += gain                                                       # Mise à jour de la variable balance
    partie_balance = "{0:,}".format(balance[0]) + " / 100.000.000"           # Formattage avec des "," aux milliers
    canvas_info.itemconfig(balance_text, text=partie_balance)                # Mise à jour graphique de la balance
    sauvegarde()                                                             # Enregistrement des données (prévention contre crash)
    maj_couleurs()
    maj_objectifs()


def maj_couleurs():
    """ Procédure pour changer les couleurs"""

    def changements_couleurs(color, increment, state):
        """ Sous-procédure pour changer les couleurs"""

        boutton_achat[increment].config(bg=color, state=state)                           # Couleur du bouton et etat (disabled ou normal)
        panneau_informations.itemconfig(amelioration_rang_label[increment], fill=color)  # Couleur du texte : numéro amelioration
        panneau_informations.itemconfig(amelioration_slot_label[increment], fill=color)  # Couleur du texte : slot amelioration
        panneau_informations.itemconfig(amelioration_gain[increment], fill=color)        # Couleur du texte : gain amelioration
    num_amelioration: int = 0
    for cout_amelioration_x in amelioration_cout:
        if amelioration_slot[num_amelioration] == ameliorations_possedees[num_amelioration]:  # Si nous n'avons plus de slots diponibles
            changements_couleurs("#FFE066", num_amelioration, "disabled")                     # Couleur jaune et état désactivé
        else:
            if balance[0] >= cout_amelioration_x:                                             # Si on peut acheter un amélioration
                changements_couleurs("#6ED8AC", num_amelioration, "normal")                   # Couleur vert et état normal
            else:
                changements_couleurs("#F25F5C", num_amelioration, "normal")                   # Couleur rouge et état normal
        num_amelioration += 1


def gains_manuels():
    """ Définition du gain par clic """

    if level[0] < 15:
        maj_level(1)                             # Mise à jour du level si c'est possible
        maj_balance(levels_gains[level[0]-1])    # Mise à jour de la balance
        maj_historique(levels_gains[level[0]-1], "Gain manuel", "manuel")  # Mise à jour de l'historique
    else:
        maj_level(0)                    # Gain experience +0 car on est déjà level max et 13 pour le rang des listes
        maj_balance(levels_gains[14])            # 13 pour le rang des listes
        maj_historique(levels_gains[14], "Gain manuel", "manuel")  # Mise à jour de l'historique


def maj_level(xp):
    """ Mise à jour du level en fonction de l'experience """

    experience[0] += xp  # Gain de "xp" experience
    if level[0] <= 14:
        lvl = level[0]
    else:
        lvl = 14
    if experience[0] < levels_experiences[lvl]:  # Si on a pas l'experience pour level-up, on gagne juste de l'experience
        texte_experience = str(experience[0]) + " / " + str(levels_experiences[lvl])                # Texte concaténé
        texte_gain_actuel: str = "Gains manuels  : " + str(levels_gains[level[0]-1]) + " / clique"  # Texte concaténé
    elif experience[0] >= levels_experiences[lvl] and level[0] < 15:
        texte_experience = str(experience[0]) + " / " + str(levels_experiences[level[0]])         # Texte concaténé
        texte_gain_actuel: str = "Gains manuels  : " + str(levels_gains[level[0]]) + " / clique"  # Texte concaténé
        level[0] += 1
    else:
        texte_experience = str(experience[0]) + " / " + str(levels_experiences[lvl])         # Texte concaténé
        texte_gain_actuel: str = "Gains manuels  : " + str(levels_gains[lvl]) + " / clique"  # Texte concaténé
    aff_experience.config(text=texte_experience)                          # Maj de l'affichage de l'experience
    canvas_usine.itemconfig(gains_manuels_label, text=texte_gain_actuel)  # Maj de l'affichage des gains manuel
    aff_level.config(text=level[0])                                       # Maj de l'affichage des levels
    maj_objectifs()                                                       # Maj des objectifs


def maj_objectifs():
    """ Mise à jour des objectifs en fonction de leur avancé"""

    if level[0] == 15:                     # Si on est level max
        objectif_level.config(fg="GREEN")  # Objectif level en vert
    if balance[0] >= 100000000:            # Si on est balance max ou plus
        objectif_coin.config(fg="GREEN")   # Objectif coin en vert
    objectif_coin_texte: str = "Objectif coins : {0}  /  100.000.000 ( {1} % )".format("{0:,}".format(balance[0]), floor((balance[0] * 100) / 100000000)) # Affichage avancé coin avec pourcentage
    objectif_coin.config(text=objectif_coin_texte)
    objectif_level_texte: str = "Objectif levels : {0}  /  15 ( {1} % )".format(level[0], floor((level[0] * 100) / 15))  # Affichage avancé level avec pourcentage
    objectif_level.config(text=objectif_level_texte)


def sauvegarde():
    """ Sauvegarde des données des joueurs """

    partie_ameliorations: str = str(ameliorations_possedees[0])  # Texte contenant l'amélioration n° 1
    for rang in range(1, 15):
        partie_ameliorations += ";{0}".format(ameliorations_possedees[rang])  # Ajout de l'amélioration 2,3,4,5,6,7,8,9,10,11,12,13,14,15 avec des ";"
    compte_connecte: str = "{0};{1};{2};{3};{4}".format(  # String étendu pour visibilité contenant les informations du joueur connecté
        compte_actuel[0].split(";")[0],                   # Pseudo
        compte_actuel[0].split(";")[1],                   # Mot de passe
        balance[0],                                       # Balance
        experience[0],                                    # Experience
        partie_ameliorations)                             # Améliorations
    increment = 0
    for rang in bloc_compte:  # Boucle servant à mettre à jour les données sur compte actuel dans la variable de tous les comptes
        if compte_actuel[0].split(";")[0] in rang.split(";")[0]:  # Recherche du compte non à jour
            bloc_compte[increment] = compte_connecte              # Mise à jour
        else:
            increment += 1
    file = open("sauvegarde.txt", "w")
    for rang in bloc_compte:  # Ecriture des comptes mis à jour dans le fichier sauvegarde
        file.write(rang + "\n")


def achats_ameliorations(num_amelioration):
    """  Procédure : gestion de l'achat d'une améloration """

    if amelioration_slot[num_amelioration] > ameliorations_possedees[num_amelioration]:  # Si il nous reste des slots disponible
        if balance[0] >= amelioration_cout[num_amelioration]:                            # Si on à l'argent pour acheter l'amélioration
            ameliorations_possedees[num_amelioration] += 1        # Ajout de 1 amélioration
            maj_balance(-amelioration_cout[num_amelioration])     # Retrait du coût de l'amélioration
            maj_historique(-amelioration_cout[num_amelioration], "Achat amélioration", "amelioration")  # Mise à jour de l'historique
            maj_couleurs()       # Mise à jour des couleurs
            maj_gains()          # Mise à jour des gains / s
            maj_ameliorations()  # Mise à jour des textes des améliorations
        else:
            showerror("Erreur", "Vous n'avez pas assez d'argent")
    sauvegarde()


def informations():
    showinfo("Informations",
             """
            But du jeu : 
            - Atteindre 100.000.000 de coins 
            - Posséder toutes les améliorations 
            - Atteindre le niveau 10 \n
            Aide : 
            - Acheter des améliorations
            - Appuyez sur le boutton \n
            Crédits :
            - TARDY Willy
            - FORGIT Théo
            """
             )



"""
__________________________________________________Execution au démarrage de l'application_________________________________________________________

"""

if __name__ == "__main__":
    """ Execution au démarrage de l'application """

    for i in range(0, 15):
        amelioration_cout.append(2 ** (i+9))  # Cout améliorations
    for i in range(1, 15):
        levels_gains.append(2 ** (i+1))                   # Gains par cliques en fonction du level
        levels_experiences.append(5*(floor(exp(i / 2))))  # Experience nécessaire pour les levels
    if os.path.exists("sauvegarde.txt"):  # Si il y a déjà un fichier de sauvegarde
        recuperation_donnees()            # On récupere les données

"""
________________________________________________________Création affichage Tkinter________________________________________________________________

"""

#___________________Instance tkinter____________________#
fenetre = Tk()
fenetre.title("Industrial clicker")
#_______________________________________________________#

# ____________________________________________________Panneau de connexion_______________________________________________________________________
cadre_connexion = Canvas(fenetre, width=800, height=50, bg="#F25F5C")
# ####  Création des éléments pour la connexion ( Dans la cadre panneau_connexion )
# #  Création élément 1 ( Label : "Pseudo")
label_pseudo = Label(cadre_connexion, text="Pseudo : ", font="Arial 17 bold", bg="#F25F5C")
label_pseudo_w = cadre_connexion.create_window(60, 25, window=label_pseudo)
# # Création de lélément 2 ( Entrée : entrée du pseudo )
entrer_pseudo = Entry(cadre_connexion)
entrer_pseudo_w = cadre_connexion.create_window(175, 25, window=entrer_pseudo)
# # Création de l'élément 3 ( Label : "Mot de passe" )
label_mot_de_passe = Label(cadre_connexion, text="Mot de passe : ", font="Arial 17 bold", bg="#F25F5C")
label_mot_de_passe_w = cadre_connexion.create_window(340, 25, window=label_mot_de_passe)
# # Création de l'élément 4 ( Entrée : entrée du mot de passe )
entrer_mot_de_passe = Entry(cadre_connexion, show="*")
entrer_mot_de_passe_w = cadre_connexion.create_window(485, 25, window=entrer_mot_de_passe)
# # Création de l'élément 5 ( Boutton : Connexion)
bouton_connexion = Button(cadre_connexion, text="Connexion", font="Arial 10 bold", command=connexion)
bouton_connexion_w = cadre_connexion.create_window(600, 25, window=bouton_connexion)
# # Création de l'élément 6 ( Boutton : Inscription)
bouton_inscription = Button(cadre_connexion, text="Inscription", font="Arial 10 bold", command=inscription)
bouton_inscription_w = cadre_connexion.create_window(690, 25, window=bouton_inscription)
# #Création de l'élément 7 ( Boutton : Informations )
bouton_informations = Button(cadre_connexion, text="Infos", font="Arial 10 bold", command=informations)
bouton_informations_w = cadre_connexion.create_window(760, 25, window=bouton_informations)
# #### Fin de la création des élements pour la connexion ( Dans la cadre cadre_connexion )
cadre_connexion.grid(columnspan=8, sticky="W")
#_____________________________________________________Fin du panneau de connexion________________________________________________________________



#__________________________________________________________Panneau profil________________________________________________________________________
canvas_avatar = Canvas(fenetre, width=280, height=200, bg="#6ED8AC")
# ####  Création des éléments pour l'affichage de l'avatar, du pseudo et du level
# # Création de l'élément 1 ( Label : "Joueur connecté :" )
joueur_co = Label(canvas_avatar, text="Joueur connecté : ", font="Arial 11 bold", bg="#6ED8AC")
joueur_co_w = canvas_avatar.create_window(200, 30, window=joueur_co)
# # Création de l'élément 2 ( Label : pseudo )
aff_pseudo = Label(canvas_avatar, text="?", font="Arial 11 bold", bg="#6ED8AC")
aff_pseudo_w = canvas_avatar.create_window(200, 60, window=aff_pseudo)
# # Création de l'élément 3 (Label : "Niveau : " )
joueur_level = Label(canvas_avatar, text="Niveau : ", font="Arial 11 bold", bg="#6ED8AC")
joueur_level_w = canvas_avatar.create_window(200, 90, window=joueur_level)
# # Création de  l'élément 4 (Label : level )
aff_level = Label(canvas_avatar, text="?", font="Arial 11 bold", bg="#6ED8AC")
aff_level_w = canvas_avatar.create_window(200, 120, window=aff_level)
# # Creation élément 5 ( Image : avatar )
img = PhotoImage(file="avatar.png")
canvas_avatar.create_image(20, 40, image=img, anchor="nw")
# # Création élément 5 ( Label : Experience : )
joueur_experience = Label(canvas_avatar, text="Experience : ", font="Arial 11 bold", bg="#6ED8AC")
joueur_experience_w = canvas_avatar.create_window(200, 150, window=joueur_experience)
# #Créatio élément 6 ( Label : experience )
aff_experience = Label(canvas_avatar, text="? / ? ", font="Arial 11 bold", bg="#6ED8AC")
aff_experience_w = canvas_avatar.create_window(200, 180, window=aff_experience)
# #### Fin de la création des éléments pour l'affichage de l'avatar, du pseudo et du level
canvas_avatar.grid(row=1, column=0, sticky="W")
#__________________________________________________________Fin du panneau profil_________________________________________________________________



#__________________________________________________________Panneau gain manuel____________________________________________________________________

canvas_usine = Canvas(fenetre, width=518, height=694, bg="#247BA0")
# ####  Création des éléments pour l'affichage de l'usine et du bouton de gain manuel
# # Création de l'élément 1 ( Image de l'usine )
image_usine = PhotoImage(file="coin.png")
canvas_usine.create_image(20, 40, image=image_usine)
# # Création de l'élément 2 ( Bouton pour gagner de l'argent de façon manuel)
bouton_gain_manuel = Button(canvas_usine, text="GAIN", font="Arial 20 bold", command=gains_manuels, state="disabled")
bouton_gain_manuel_w = canvas_usine.create_window(259, 550, window=bouton_gain_manuel)
# # Création de l'élément 3 ( Affichage des gains cumulés par seconde )
gains_automatiques_label = canvas_usine.create_text(259, 100, text="Gains automatiques : ? / s", font="Arial 11 bold")
# # Création de l'élément 4 ( Affichage des gains par clique )
gains_manuels_label  = canvas_usine.create_text(259, 140, text="Gain manuels : ? / clique",  font="Arial 11 bold")
# # Création de l'élément 5 ( Text affichant l'historique )
historique = Text(canvas_usine, height=20, width=50)
historique_w = canvas_usine.create_window(259, 330, window=historique)
# # Création des 3tags servants à changer la couleur dans l'historique
historique.tag_config("automatique", foreground="BLUE")  # Bleu pour un gain automatque
historique.tag_config("manuel", foreground="GREEN")      # Vert pour un gain manuel
historique.tag_config("amelioration", foreground="RED")  # Rouge pour l'achat d'une amélioration
# # Création de l'élément 6 ( Object 100.000.000 )
objectif_coin = Label(canvas_usine, text="Objectif coins : ? coins  /  100.000.000 coins", font="Arial 11 bold", bg="#247BA0")
objectif_coin_w = canvas_usine.create_window(259, 625, window=objectif_coin)
objectif_level = Label(canvas_usine, text="Objectif levels : ? level  /  15 level", font="Arial 11 bold", bg="#247BA0")
objectif_level_w = canvas_usine.create_window(259, 650, window=objectif_level)

# #### Fin de la création des éléments pour l'affichage de l'usine et du bouton de gain manuel
canvas_usine.grid(row=1, column=2, columnspan=4, rowspan=4, sticky="NEW")
#__________________________________________________________Fin du panneau gain manuel_____________________________________________________________



#__________________________________________________________Panneau affichage balance_______________________________________________________________
canvas_info = Canvas(fenetre, width=518, height=70, bg="#50514F")
# ####  Création des éléments pour la création du bandeau d'informations ( Balance et Level )
# #  Création élément 1 ( Label : balance + "/50 000 000" )
balance_text = canvas_info.create_text(220, 35, text="? / 100.000.000", font="Arial 20 bold")
# #  Création élément 2 ( Affichage de l'image du coin )
coin = PhotoImage(file="coin.png")
canvas_info.create_image(470, 35, image=coin)
# #### Fin de la création des éléments pour l'affichage du bandeau
canvas_info.grid(row=1, column=1, columnspan=3, sticky="NW")
#__________________________________________________________Fin du panneau affichage balance________________________________________________________



#______________________________________________________________Panneau d'amélioration _____________________________________________________________
panneau_informations = Canvas(fenetre, width=280, height=490, bg="#50514F")
# ####  Création des éléments pour la création du panneau d'amélioration (Nombre d'améliorations dispo, cout des améliorations et bouton d'achat)
titre_amelioration = panneau_informations.create_text(140, 20, text="Améliorations", font="Arial 15 bold")
# #  Création élément 1 ( Label : "N° des améliorations" )
amelioration_rang_label = list()  # Objets tkinter représentants les numéros d'améliorations
amelioration_gain = list()        # Objets tkinter représentants les gains/seconde
coord_x = 55                      # Coordonnées x des objets
""" Utilisation d'un for créer les objets dynamiquement """
for i in range(1, 16):
    temp_text = "N°" + str(i) + " : "
    amelioration_rang_label.append(panneau_informations.create_text(20, coord_x, text=temp_text, font="Arial 8 bold"))
    a = 2 ** (i+2)
    temp_text = "+ " + str(a) + " /sec "
    ameliorations_gains.append(a)
    amelioration_gain.append(panneau_informations.create_text(240, coord_x, text=temp_text, font="Arial 8 bold"))
    coord_x += 30

# #  Création élément 2 ( Bouton d'achat des améliorations )
boutton_achat = list()      # Objets tkinter représentants les boutons d'achat
button_achat_w = list()     # Objets tkinter représentants les window pour placer les boutons
x = 55                      # Coordonnées x des objets
""" Utilisation d'un for pour éviter la création de 15 bouton indépendament """
for i in range(0, 15):
    text = str(amelioration_cout[i]) + " coins"
    boutton_achat.append(Button(panneau_informations, text=text))
    button_achat_w.append(panneau_informations.create_window(105, x, window=boutton_achat[i]))
    x += 30

# #  Création élément 3 ( Texte nombre d'améliorations achetées/disponnible )
x = 55                      # Coordonnées x des objets
amelioration_slot_label = list()     # Objets tkinter représentants le nombre d'améliorations achetées / le nombre d'améliorations disponnibles
""" Utilisation d'un for pour éviter la création de 15 texte indépendament """
for i in range(15):
    ameliorations_possedees.append(0)
    if i < 4:
        amelioration_slot_label.append(panneau_informations.create_text(180, x, text="? / 10", font="Arial 8 bold"))
        amelioration_slot.append(10)
    if 8 > i > 3:
        amelioration_slot_label.append(panneau_informations.create_text(180, x, text="? / 5", font="Arial 8 bold"))
        amelioration_slot.append(5)
    if 12 > i > 7:
        amelioration_slot_label.append(panneau_informations.create_text(180, x, text="? / 3", font="Arial 8 bold"))
        amelioration_slot.append(3)
    if 14 > i > 11:
        amelioration_slot_label.append(panneau_informations.create_text(180, x, text="? / 2", font="Arial 8 bold"))
        amelioration_slot.append(2)
    if i > 13:
        amelioration_slot_label.append(panneau_informations.create_text(180, x, text="? / 1", font="Arial 8 bold"))
        amelioration_slot.append(1)
    x += 30
# #### Fin de la création des éléments pour l'affichage du panneau d'améliorations
panneau_informations.grid(row=2, column=0, sticky="W")
#_________________________________________________________Fin du panneau d'amélioration _____________________________________________________________

fenetre.mainloop()
