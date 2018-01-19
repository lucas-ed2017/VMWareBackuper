#!/bin/python
# -*- coding: utf-8 -*-

import VirtualMachine, FTPServer    #Outras classes necessaria
from os import system   #classe que manipula a linha de comando
import sys

class VMWAreBackuper:    #inicio da classe

    def __init__(self, ftp): #construtor
        self.VMlist = [] #atributo que conter o nome de todas as VMs
        self.ftp = ftp
        system('vim-cmd vmsvc/getallvms or vim-cmd vmsvc/getallvms > allvms.txt')   #gerar texto com todas as Maquinas Virtuais
        try:
            with open('allvms.txt') as allvms:  #abrir arquivo de texto anteriormente gerado
                VMs = allvms.readlines()        #todas as linhas do texto
                for line in VMs[1:]:            #ignorar a primeira linha (linha 0 (zero)) e ler o resto do texto 
                    VMsNames = line.split()     #transformar a linha atual em indexs
                    self.VMlist.append(VMsNames[1].strip())  #pegar o index com o nome e jogar na lista de nomes de VMs tirando espaços inuteis
            system('rm -r allvms.txt')  #apagar arquivo de texto inutil anteriormente gerado
        except Exception as e:
            print(e)

    def backupVM(self, vmname):     #fazer backup de uma maquina especifica
        for name in self.VMlist:   #procurar maquina desejada
            try:
                if name == vmname:    #maquina encontrada
                        print("Virtual Machine " + vmname + " found")
                        vm = VirtualMachine.VirtualMachine(vmname)  #objeto maquina virtual
                        print("Turning VM " + vmname + " off.")
                        vm.turnOff()
                        #ftp = FTPServer.FTPServer('192.168.163.130', 'ftp', 'l25081999')    #conexão ao servidor FTP
                        print("Packing VM " + vmname + " and sending it to server " + self.ftp.address)
                        self.ftp.sendFile(vmname) #Enviar uma copia da pasta da vm compactada para o servidor
                        print("Success! Turning VM " + vmname + " on")
                        vm.turnOn()
            except:
                    print("Unexpected error: ", sys.exc_info()[0])

ftp = FTPServer.FTPServer("000.000.000.000", "user", "pass", "/")
v = VMWAreBackuper(ftp)
v.backupVM('VMName')


