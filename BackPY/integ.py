import pyodbc
import os
import numpy as np
from time import sleep
import gc

def guess_devtype(file):
	if("2.2.2.1" in (str)(file)):
		return "fortigate"
	else:
		return "switch"

server = "HPELITEBOOK\MSSQLSERVEUR;"

while True:
	dir_path = "./logs/"
	log_files = os.listdir(dir_path)
	#print(log_files)

	months = {
			"Jan":"01","Feb":"02","Mar":"03","Avr":"04","Mai":"05","Jun":"06",
			"Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"
			}

	cnxn_str = ("Driver={SQL Server Native Client 11.0};"+
	            "Server="+server+
	            "Database=syslog;"
	            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)
	cursor = cnxn.cursor()


	#boucle tt les fichiers
	for file in log_files:

		path = dir_path+file
		print("lecture : "+path)

		prelog = np.genfromtxt(path, delimiter='\n', dtype=str, encoding="utf-8")

		devtype = guess_devtype(file)

		if(devtype == "fortigate"):
			for i in range(prelog.shape[0]):

				#pour chaque fichier log du dossier 
				#print("file : "+file+", log : ",i)
				all_ = ""
				atts = {"date=":"","time=":"", "devname=":"", "srcip=":"",
				"subtype=":"", "type=":"", "user=":"", "msg=":"", "ui=":"", 
				"attack=":""}
				
				log = prelog[i].replace("'","''").replace("\"","").split(" ")

				
				try:
					log.remove("")
				except ValueError:
					pass
				
				in_msg = False
				for log_part,l in zip(log,range(len(log))):

					essential = False
					for att in atts:
						if(att in log_part and att[0:2] == log_part[0:2]):
							essential = True
							atts[att] = log_part.split("=")[1]
							if (att == "msg="):
								in_msg = True
							break
					if (not essential):
						if (in_msg):
							atts["msg="] = atts["msg="]+" "+log_part
						else :
							all_ = all_+" "+log_part

				all_ = all_[1:]

				#print("\n\n----done----\n\n")
				#print(atts)
				#print()
				#print(all_)
				#print("\n\n\nnext---------------------\n\n\n")

				requete = "INSERT INTO [sec_logs] ([datetime],[devname],\
					[type],[loguser],[msg],[ui],[attack],[logall])\
	            	VALUES \
	            	('"+atts["date="]+" "+atts["time="]+"','"\
	            	+atts["devname="]+"','"+atts["type="]+" "\
	            	+atts["subtype="]+"','"+atts["user="]+"','"+atts["msg="]\
	            	+"','"+atts["ui="]+"','"+atts["attack="]+"','"+all_+"')"

				#print("_______req_______")
				#print(requete)
				#print("_________________")
				try:
					cursor.execute(requete)
					cnxn.commit()
				except Exception as e:
					if(not os.path.exists("./err_sec.txt")):
						create = open("./err_sec.txt","w")
						create.close()
					err_file = open("./err_sec.txt","a")
					err_file.write("err :\n"+(str)(e)+"\n---------\n"+requete+"\n\n")
					err_file.close()
					print("erreur log fortigate : \n\n")
					print(e)
					print("------------")
					print(requete)
					print("\n\n")

					#write in backup file log that could'nt be inserted 
					err_log_file = open(file[:-4]+"_err.log","a")
					err_log_file.write(prelog[i])
					err_log_file.close()


			print("fait, fichier supprimé "+path,end="\n\n")
			os.remove(path)

		else :
			try:
				print(prelog.shape[0])
			except IndexError:
				prelog = [prelog]
				prelog = np.array(prelog)

			for k in range(prelog.shape[0]):
				atts = []
				log = prelog[k].replace("'","''").replace("\"","").split(" ")
				atts.append("'"+log[3]+"'")
				atts.append("'"+log[4][:-1]+"'")
				atts.append("'"+months[log[5]]+" "+log[6]+" "+log[7][:-1]+"'")
				atts.append("'"+log[8][:-1]+"'")
				j = 9
				msg = ""
				while (j < len(log)):
					msg = msg + " " + log[j]
					j = j + 1
				atts.append("'"+msg[1:]+"'")

				requete = "INSERT INTO [dbo].[res_logs]\
				([devip],[devid],[datetime],[opt],[msg])\
				VALUES\
				("+",".join(atts)+")"


				#print("\n\n-------\n\n")
				#print(requete)
				#print("\n\n")


				try:
					cursor.execute(requete)
					cnxn.commit()
				except Exception as e:
					if(not os.path.exists("./err_res.txt")):
						create = open("./err_res.txt","w")
						create.close()
					err_file = open("./err_res.txt","a")
					err_file.write("err :\n"+(str)(e)+"\n---------\n"+requete+"\n\n")
					err_file.close()
					print("erreur log fortigate : \n\n")
					print(e)
					print("------------")
					print(requete)
					print("\n\n")

					#write in backup file log that could'nt be inserted 
					err_log_file = open(file[:-4]+"_err.log","a")
					err_log_file.write(prelog[i])
					err_log_file.close()


			print("fait, fichier supprimé : "+path,end="\n\n")
			os.remove(path)

		del prelog
		del devtype
		gc.collect()



	del cnxn
	sleep(600)