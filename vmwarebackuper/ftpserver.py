#!/bin/python
# -*- coding: utf-8 -*-
import ftplib #biblioteca FTP
import progressbar
from os import system		 #comando system permite dar comandos pelo terminal
from os import stat

class ftpserver(object):	#inicio da classe
	
	def __init__(self, address, user, password, baseDir):	#construtor
		self.address = address	#metodos
		self.user = user
		self.password = password
		self.baseDir = baseDir
		self.ftp = ftplib.FTP(self.address)
		self.ftp.login(user=self.user, passwd=self.password)
		self.ftp.cwd(self.baseDir)
		#self.connect()

	def sendfile(self, file):	#compactar e enviar a maquina compactada
                try:
                        #self.connect()
                        total = stat(file).st_size
                        bar = progressbar.progressbar(0, total)
                        def create_callback():
                                def cb(data):
                                        bar.update_progress(len(data)/total)

                                return cb
                        callback = create_callback()
                        self.ftp.storbinary("STOR " + file, open(file, 'rb'), callback=create_callback())
                        self.end()
                except ftplib.all_errors as e:
                        print(e)
                        self.end()
                        #self.connected = False
                        raise

	#def downloadfile(self, file):
        #        self.connect()
#		self.ftp.retrbinary('RETR ' + file, open(file, 'wb').write())	#baixar um sistema requisitado
#		self.end()

	#def connect(self):
        #        try:	#tentar estabelecer conexão FTP
        #                self.ftp = ftplib.FTP(self.address, timeout = 100) #conexão com o servidor
        #                self.ftp.login(user=self.user, passwd=self.password)
        #                self.ftp.set_pasv(False) #entra no modo ativo do FTP, necessário para alguns ambientes, estudar se o modo ativo funciona em todos os ambientes, no IFRN foi necessário
        #                self.ftp.cwd(self.baseDir)
        #                self.connected = True
        #                print('FTP Connection successfull!')
#		except ftplib.all_errors as e:	#conexão falhou
#			self.connected = False
#			print(e)
#			raise

	def end(self):
                #self.connected = False
                self.ftp.quit()
