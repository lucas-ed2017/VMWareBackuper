#!/bin/python
# -*- coding: utf-8 -*-
import ftplib #biblioteca FTP
import progressbar
from os import system		 #biblioteca system permite dar comandos pelo terminal
from os import stat

class ftpserver:	#inicio da classe
	
	def __init__(self, address, user, password, baseDir, progressbar = True):	#construtor
		self.address = address	#metodos
		self.user = user
		self.password = password
		self.baseDir = baseDir
		self.ftp = ftplib.FTP(self.address)
		self.ftp.login(user=self.user, passwd=self.password)
		self.ftp.cwd(self.baseDir)
		self.connect()
		self.progressbar = progressbar

	def sendfile(self, file):	#compactar e enviar a maquina compactada
                try:
                        self.connect()
                        if self.progressbar: #se for necessario utilizar a progressbar, crie uma e envie o arquivo
                                total = stat(file).st_size
                                bar = progressbar.progressbar(0, total)
                                cb = self.__create_callback__(bar, total)
                                self.ftp.storbinary("STOR " + file, open(file, 'rb'), callback=cb)
                        else:   #se nao, apenas envie o arquivo silenciosamente
                                self.ftp.storbinary("STOR " + file, open(file, 'rb'))
                        self.end()
                except ftplib.all_errors as e:
                        print(e)
                        self.end()
                        self.connected = False
                        raise

	def downloadfile(self, file):
                self.connect()
		self.ftp.retrbinary('RETR ' + file, open(file, 'wb').write())	#baixar um sistema requisitado
		self.end()

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

        def __create_callback__(self, progressbar, total): #os underlines no nome da funcao tornam ela 'private', o que dificulta a utilizacao em outras classes
                def cb(data):
                        progressbar.update_progress(len(data))
                return cb
