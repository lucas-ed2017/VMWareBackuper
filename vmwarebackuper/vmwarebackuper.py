#!/bin/python
# -*- coding: utf-8 -*-

try:
    import virtualmachine, ftpserver, packager
except ImportError:
    import vmwarebackuper.virtualmachine, vmwarebackuper.ftpserver, vmwarebackuper.packager    #Outras classes necessarias

from os import system   #classe que manipula a linha de comando
import sys
from datetime import datetime #será usado para colocar a data do backup

class vmwarebackuper():    #inicio da classe
    def __init__(self, ftp, extension='.tar.gz'): #construtor
        self.vmlist = [] #atributo que conter o nome de todas as VMs
        self.ftp = ftp
        self.extension = extension
        system('vim-cmd vmsvc/getallvms or vim-cmd vmsvc/getallvms > allvms.txt')   #gerar texto com todas as Maquinas Virtuais
        try:
            with open('allvms.txt') as allvms:  #abrir arquivo de texto anteriormente gerado
                VMs = allvms.readlines()        #todas as linhas do texto
                for line in VMs[1:]:            #ignorar a primeira linha (linha 0 (zero)) e ler o resto do texto 
                    VMsNames = line.split()     #transformar a linha atual em indexs
                    self.vmlist.append(VMsNames[1].strip())  #pegar o index com o nome e jogar na lista de nomes de VMs tirando espaços inuteis
            system('rm -r allvms.txt')  #apagar arquivo de texto inutil anteriormente gerado
        except IOError as i:
            print(i)
            print("Error! don't was possible search the VirtualMachines ")
        except Exception as e:
            print(e)
            print("Error! don't was possible continue")

    def backupvm(self, vmname):     #fazer backup de uma maquina especifica
        try:
            if vmname in self.vmlist:    #maquina encontrada
                print("Virtual Machine " + vmname + " found")
                vm = virtualmachine.virtualmachine(vmname)  #objeto maquina virtual
                print("Turning VM " + vmname + " off.") #aviso de maquina está sendo desligada
                vm.turnoff()    #metodo desligar maquina
                print("Packing VM " + vmname)
                finalfile = vmname  + '_vmwarebackuper_' + str(datetime.now())
                packer = packager.packager(vmname, finalfile) #preparar empacotador
                packer.compress() #empacotar maquina virtual
                finalfile = finalfile + self.extension
                print("Sending " + vmname + " to server " + self.ftp.address)
                self.ftp.sendfile(finalfile) #Enviar uma copia da pasta da vm compactada para o servidor
                system('rm -r \'' + finalfile + '\'') #remover a copia agora inutil
                print("Success! Turning VM " + vmname + " on")
                vm.turnon()
            else:
                print("Virtual Machine " + vmname + " not found.")
        except Exception as e:
            print("Unexpected error: ", sys.exc_info()[0])
            print(e)

    def backupallvms(self):
        for vmname in self.vmlist:
            self.backupvm(vmname)

    def getallvms(self):
        return self.vmlist
