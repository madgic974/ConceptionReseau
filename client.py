from fonctionClient import *

def ChoixAction():
    print("Choisir l'action a éffectuer :")
    print("Saisir 1 pour lire une valeur  :")
    print("Saisir 2 pour ajouter une valeur :")
    print("Saisir 3 pour fermer le client :")
    return(input("Saisie : "))


while(1):

    choix = ChoixAction()

    if (choix=='1') : 
        lecture("")
    elif (choix=='2') : 
        ecriture() 
    elif (choix=='3') : 
        print("Fermeture")
        exit()
    else :
        print("Erreur de saisie") 
