Nécessaires : netmiko & pandas

1. Création de la variable d'environnement en bash
export DB_PASSWORD="ici_mot_de_passe"

2. Lecture de la variable d'environnement en python via le module OS
import os
password = os.getenv("DB_PASSWORD")
print(password)

3. Format du fichier .csv
ip;fabricant

4. Exec fichier .sh 
