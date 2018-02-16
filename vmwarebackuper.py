#!/bin/python
# -*- coding: utf-8 -*-

import virtualmachine, ftpserver, packager    #Outras classes necessarias
from os import system   #classe que manipula a linha de comando
import sys
from datetime import datetime #será usado para colocar a data do backup

class vmwarebackuper:    #inicio da classe

    def __init__(self, ftp): #construtor
        self.vmlist = [] #atributo que conter o nome de todas as VMs
        self.ftp = ftp
        system('vim-cmd vmsvc/getallvms or vim-cmd vmsvc/getallvms > allvms.txt')   #gerar texto com todas as Maquinas Virtuais
        try:
            with open('allvms.txt') as allvms:  #abrir arquivo de texto anteriormente gerado
                VMs = allvms.readlines()        #todas as linhas do texto
                for line in VMs[1:]:            #ignorar a primeira linha (linha 0 (zero)) e ler o resto do texto 
                    VMsNames = line.split()     #transformar a linha atual em indexs
                    self.vmlist.append(VMsNames[1].strip())  #pegar o index com o nome e jogar na lista de nomes de VMs tirando espaços inuteis
            system('rm -r allvms.txt')  #apagar arquivo de texto inutil anteriormente gerado
        except Exception as e:
            print(e)

    def backupvm(self, vmname):     #fazer backup de uma maquina especifica
        for name in self.vmlist:   #procurar maquina desejada
            try:
                if name == vmname:    #maquina encontrada
                        print("Virtual Machine " + vmname + " found")
                        vm = virtualmachine.virtualmachine(vmname)  #objeto maquina virtual
                        print("Turning VM " + vmname + " off.") #aviso de maquina está sendo desligada
                        vm.turnoff()    #metodo desligar maquina
                        print("Packing VM " + vmname + " and sending it to server " + self.ftp.address)
                        finalfile = str(vmname  + '_B_' + str(datetime.now()) + '.tar')
                        print(finalfile)
                        packer = packager.packager(str('/vmfs/volumes/datastore1/' + vmname), finalfile) #preparar empacotador
                        packer.compress() #empacotar maquina virtual
                        self.ftp.sendfile(finalfile) #Enviar uma copia da pasta da vm compactada para o servidor
                        print("Success! Turning VM " + vmname + " on")
                        vm.turnon()
            except:
                    print("Unexpected error: ", sys.exc_info()[0])
                    
ftp = ftpserver.ftpserver('192.168.163.130', 'ftp', 'l25081999', '/home/ftp')
v = vmwarebackuper(ftp)
v.backupvm('windows')


