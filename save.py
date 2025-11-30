import getpass
import os
import sys


#Pour traiter les fichiers CSV
import pandas as pd

from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException

from datetime import datetime

from paramiko import ssh_exception

#Definition des variables

chemin = "/home/ansible/save_conf/"

#Demande des informations de connexions

#user = input("Login : ")
#passwd = getpass.getpass("Password : ")

user = "admin"
passwd = "ici_mot_de_passe"

#Formatage de la date pour le nom du fichier
now = datetime.now()
date = now.strftime("%Y-%m-%d")
heure = now.strftime("%H:%M:%S")

#Definition des fonctions

#Fonction log : enregistrement d'un fichier log

def log(message):
	with open("backup.log", 'a') as file:
		file.write(message+"\n")

def save_conf(host, conf, date):
	#tmp = "/home/ansible/save_conf/"+date+"/"+host+"_"+date+".cfg"
	tmp = chemin+date+"/"+host+"_"+date+".cfg"
	with open(tmp,'w') as file:
		file.write(conf)
#Fin de definition des fonctions

#Inscription dans le fichier log du lancement du script
with open("backup.log",'a') as file:
	file.write("\nDebut de la tache de sauvegarde - ")
	file.write(date)
	file.write(" à ")
	file.write(heure)
	file.write("\n")

#Vérification de la présence du fichier source en argument
try:
	if sys.argv[1]:
		if os.path.exists(sys.argv[1]):
			fic_src = sys.argv[1]
		else:
			log("Le fichier "+sys.argv[1]+" n'exise pas\nFin du script")
			quit()
except IndexError:
	log("Absence du nom du fichier source en argument")
	log("Fin du script")
	quit()

liste = pd.read_csv(fic_src, delimiter=";")

#Creation du dossier de configuration en fonction de la date
if not os.path.exists(chemin+date):
	os.mkdir(chemin+date)

for index, ear in liste.iterrows():
	ear_fabricant = ear["fabricant"]
	ear_ip = ear["ip"]
	if ear_fabricant == "hp_comware":
		try:
			connect = ConnectHandler(device_type="hp_comware", ip=ear_ip, username=user, password=passwd)
		except NetmikoTimeoutException:
			log(ear_ip+" : injoignable")
			print(ear_ip+" : injoignable")
		except NetmikoAuthenticationException:
			log(ear_ip+" : connexion SSH impossible")
			print(ear_ip+" : connexion SSH impossible")
		else:
			hostname = connect.find_prompt()[1:-1]
			print(ear_ip+" - "+hostname)
			conf = connect.send_command("dis current-configuration")
			save_conf(hostname, conf, date)
			log(hostname+" : OK")
	elif ear_fabricant == "cisco_ios":
		try:
			connect = ConnectHandler(device_type="cisco_ios", ip=ear_ip, username=user, password=passwd)
		except NetmikoTimeoutException:
			log(ear_ip+" : injoignable")
			print(ear_ip+" : injoignable")
		except NetmikoAuthenticationException:
			log(ear_ip+" : connexion SSH impossible")
			print(ear_ip+" : connexion SSH impossible")
		else:
			hostname = connect.find_prompt()[:-1]
			print(ear_ip+" - "+hostname)
			connect.enable()
			conf = connect.send_command("sh run")
			save_conf(hostname, conf, date)
			log(hostname+" : OK")
	elif ear_fabricant == "allied_telesis_awplus":
		try:
			connect = ConnectHandler(device_type="allied_telesis_awplus", ip=ear_ip, username=user, password=passwd)
		except NetmikoTimeoutException:
			log(ear_ip+" : injoignable")
			print(ear_ip+" : injoignable")
		except NetmikoAuthenticationException:
			log(ear_ip+" : connexion SSH impossible")
			print(ear_ip+" : connexion SSH impossible")
		else:
			hostname = connect.find_prompt()[:-1]
			print(ear_ip+" - "+hostname)
			connect.enable()
			conf = connect.send_command("sh run")
			save_conf(hostname, conf, date)
			log(hostname+" : OK")
	connect.disconnect()
now = datetime.now()
heure = now.strftime("%H:%M:%S")
log("Fin de la sauvegarde à "+heure+"\n")

print("Fin du script")
