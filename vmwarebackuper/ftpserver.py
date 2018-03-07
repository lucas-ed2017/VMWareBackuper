#!/bin/python
# -*- coding: utf-8 -*-
import ftplib #biblioteca FTP
from os import system		 #comando system permite dar comandos pelo terminal

class ftpserver(object):	#inicio da classe
	
	def __init__(self, address, user, password, baseDir):	#construtor
		self.address = address	#metodos
		self.user = user
		self.password = password
		self.baseDir = baseDir
		self.connect()

	def sendfile(self, file):	#compactar e enviar a maquina compactada
                try:
                        self.connect()
                        self.ftp.storbinary("STOR " + file, open(file, 'rb'))
                        self.ftp.end()
                except ftplib.all_errors as e:
                        print(e)
                        self.end()
                        self.connected = False
                        raise

	def downloadfile(self, file):
                self.connect()
		self.ftp.retrbinary('RETR ' + file, open(file, 'wb').write())	#baixar um sistema requisitado
		self.ftp.end()

	def connect(self):
                try:	#tentar estabelecer conexão FTP
                        self.ftp = ftplib.FTP(self.address, timeout = 100) #conexão com o servidor
                        self.ftp.login(user=self.user, passwd=self.password)
                        self.ftp.set_pasv(False) #entra no modo ativo do FTP, necessário para alguns ambientes, estudar se o modo ativo funciona em todos os ambientes, no IFRN foi necessário
                        self.ftp.cwd(self.baseDir)
                        self.connected = True
                        print('FTP Connection successfull!')
		except ftplib.all_errors as e:	#conexão falhou
			self.connected = False
			print(e)
			raise

	def end(self):
                self.connected = False
                self.ftp.quit()
