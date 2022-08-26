from flask import Flask, request
import pyodbc
from flask_cors import CORS
 

app = Flask(__name__)
CORS(app)

d_atts_sec = {"datetime":"","devname":"","type":"",\
"loguser":"","msg":"","ui":"","attack":"","logall":""}

d_atts_res = {"devip":"","devid":"","datetime":"","opt":"","msg":""}

d_atts_2 = {"user":"","group":""}

groups = {"sec":1 , "res": 2, "adm": 3}

#serv = "Server=HPELITEBOOK\MSSQLSERVEUR;"
#serv = "Server=DESKTOP-LV5JDV8;"


@app.route('/get_group', methods = ['POST', 'GET'])
def get_group():
	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)
	user = ""
	try:
		if request.method == 'POST':
			user = request.json['test3Mail']
		else:
			user = request.args.get('test3Mail')
		print("succes : ",user)  
	except Exception as e:
		print("echec : ",user)
		print(e)

	try:
		req = "SELECT [group] FROM [syslog].[dbo].[usergroup] WHERE [user] = '"+user+"'"
		cursor = cnxn.cursor()
		cursor.execute(req)
		group = []
		for c in cursor:
			group.append(groups[c[0]])
		
	except Exception as e:
		print (e)
		return({'group':4})
		# user n'existe pas
	
	#group = pd.read_sql(req, cnxn)

	del cnxn

	try:
		print({'group':(str)(group[0])})
		return ({'group':(str)(group[0])})
	except Exception :
		return({'group':4}) 


@app.route('/get_all_usergroup', methods = ['POST', 'GET'])
def get_all_usergroup():
	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)  

	req = "SELECT * FROM [syslog].[dbo].[usergroup]"

	#group = pd.read_sql(req, cnxn)

	cursor = cnxn.cursor()
	cursor.execute(req)
	group = []
	for c in cursor:
		dic = d_atts_2.copy()
		inc = 0
		for att in d_atts_2:
			dic[att]=(str)(c[inc])
			inc = inc + 1

		group.append(dic)
	del cnxn

	return (group)


@app.route('/insert_usergroup', methods = ['POST', 'GET'])
def insert_usergroup():
	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)
	user = ""
	grp = ""

	try:
		if request.method == 'POST':
			user = request.json['umail']
			grp = request.json['ugrp']
		else:
			user = request.args.get('umail')
			grp = request.args.get('ugrp')   
		print("succes recup parametres :         (user : ",user,"   ;   grp : ",grp,")")
	except Exception as e:
		print("echec recup parametres")
		print(e)

	req = "INSERT INTO [syslog].[dbo].[usergroup] ([user],[group]) VALUES\
			('"+user+"','"+grp+"')"

	cursor = cnxn.cursor()
	try:
		cursor.execute(req)
		cnxn.commit()
		success = "success"
	except Exception as e:
		print("erreur /get_all_usergroup : ")
		print(e)
		success = "fail"
	finally:
		del cnxn
	return(success)


@app.route('/delete_usergroup', methods = ['POST', 'GET'])
def delete_usergroup():
	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)
	user = ""
	try:
		if request.method == 'POST':
			user = request.json['umail']
			print("heree",user)
		else:
			user = request.args.get('umail') 
		print("succes recup parametres :         (user : ",user,")")
	except Exception as e:
		print("echec recup parametres")
		print(e)

	req = "DELETE FROM [syslog].[dbo].[usergroup] where [user] = '"+user+"'"

	cursor = cnxn.cursor()
	try:
		cursor.execute(req)
		cnxn.commit()
		success = "success"
	except Exception as e:
		print("erreur /delete_usergroup : ")
		print(e)
		success = "fail"
	finally:
		del cnxn
		return(success)


@app.route('/update_usergroup', methods = ['POST', 'GET'])
def update_usergroup():
	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)

	try:
		if request.method == 'POST':
			new_user = request.json['newmail']
			new_grp = request.json['newgrp']
			old_user = request.json['umail']
		else:
			new_user = request.args.get('newmail')
			new_grp = request.args.get('newgrp')
			old_user = request.args.get('umail')
		print("succes recup parametres :         (new_user : ",new_user,"   ;   new_grp : ",new_grp,"   ;   old_user : ",old_user,")")
	except Exception as e:
		print("echec recup parametres")
		print(e)

	req = "UPDATE [usergroup] SET [user] = '"+new_user+"',[group] = '"+new_grp+"' WHERE \
	[user] = '"+old_user+"'"

	cursor = cnxn.cursor()
	try:
		cursor.execute(req)
		cnxn.commit()
		success = "success"
	except Exception as e:
		print("erreur /delete_usergroup : ")
		print(e)
		success = "fail"
	finally:
		del cnxn
		return(success)


@app.route('/all_sec_logs', methods = ['POST', 'GET'])
def all_sec_logs():
	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)

	req = "SELECT [datetime],[devname],[type],[loguser],[msg],[ui],[attack],[logall]\
	 FROM [dbo].[sec_logs] "

	#group = pd.read_sql(req, cnxn)

	cursor = cnxn.cursor()
	cursor.execute(req)
	group = []
	for c in cursor:
		dic = d_atts_sec.copy()
		inc = 0
		for att in d_atts_sec:
			dic[att]=(str)(c[inc])
			inc = inc + 1

		group.append(dic)
	del cnxn

	return (group)


@app.route('/sec_logs', methods = ['POST', 'GET'])
def get_sec_logs():
	
	try:
		if request.method == 'POST':
			page = (int)(request.json['page'])
		else:
			page = (int)(request.args.get('page'))
	except Exception as e:
		# no params found
		print("erreur /sec_logs :")
		print(e)
		print("\n")
		page = 1

	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)

	req =  "SELECT [datetime],[devname],[type],[loguser],[msg],[ui],[attack],[logall]\
			FROM [syslog].[dbo].[sec_logs]\
			ORDER BY id \
	    	OFFSET (10)*("+(str)(page)+"-1) ROWS\
	    	FETCH NEXT 10 ROWS ONLY; "


	#group = pd.read_sql(req, cnxn)

	cursor = cnxn.cursor()
	cursor.execute(req)
	group = []
	for c in cursor:
		dic = d_atts_sec.copy()
		inc = 0
		for att in d_atts_sec:
			dic[att]=(str)(c[inc])
			inc = inc + 1

		group.append(dic)
	del cnxn

	return (group)


@app.route('/all_res_logs', methods = ['POST', 'GET'])
def all_res_logs():
	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)
	req = "SELECT [devip],[devid],[datetime],[opt],[msg] FROM [res_logs] "
	#group = pd.read_sql(req, cnxn)

	cursor = cnxn.cursor()
	cursor.execute(req)
	group = []
	for c in cursor:
		dic = d_atts_res.copy()
		inc = 0
		for att in d_atts_res:
			dic[att]=(str)(c[inc])
			inc = inc + 1

		group.append(dic)
	del cnxn

	return (group)


@app.route('/res_logs', methods = ['POST', 'GET'])
def get_res_logs():


	try:
		if request.method == 'POST':
			page = (int)(request.json['page'])
		else:
			page = (int)(request.args.get('page'))
	except Exception as e:
		# no params found
		print("erreur /res_logs :")
		print(e)
		print("\n")
		page = 1
	

	cnxn_str = ("Driver={SQL Server Native Client 11.0};"
			"Server=HPELITEBOOK\MSSQLSERVEUR;"
            "Database=syslog;"
            "Trusted_Connection=yes;")
	cnxn = pyodbc.connect(cnxn_str)
	req =  "SELECT [devip],[devid],[datetime],[opt],[msg]\
			FROM [syslog].[dbo].[res_logs]\
			ORDER BY id \
	    	OFFSET (10)*("+(str)(page)+"-1) ROWS\
	    	FETCH NEXT 10 ROWS ONLY; "

	#group = pd.read_sql(req, cnxn)

	cursor = cnxn.cursor()
	cursor.execute(req)
	group = []
	for c in cursor:
		dic = d_atts_res.copy()
		inc = 0
		for att in d_atts_res:
			dic[att]=(str)(c[inc])
			inc = inc + 1

		group.append(dic)
	del cnxn

	return (group)



if __name__ == "__main__":
    app.run()