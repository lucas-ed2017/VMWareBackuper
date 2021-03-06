#!/bin/python
# -*- coding: utf-8 -*-

from os import system	#comando system permite dar comandos pelo terminal
from time import sleep

class virtualmachine:	#inicio da classe
    def __init__(self, name):	#construtor
        self.name = name		#atributo nome
        system('vim-cmd vmsvc/getallvms or vim-cmd vmsvc/getallvms |grep {} > vminfo.txt'.format(self.name))	#gerar arquivo de texto com informações da maquina
        try:
            with open('vminfo.txt') as vmtext:	#abrir arquivo de texto anteriormente gerado
                self.vmid = vmtext.readline()[0:2].strip()	#obter o id e apagar espaços inuteis 
            system('rm -r vminfo.txt') #apagar arquivos de textos agora inuteis
        except IOError as i:
            print(i)
            print("Error! don't was possible read the informations about {} virtual machine".format(name))
        except Exception as e:
            print(e)
            print("Error! something wrong... ")
            
    def status(self):
        system('vim-cmd vmsvc/power.getstate {} > vmstate.txt'.format(self.vmid))
        try:
            with open('vmstate.txt') as vmstate:	#abrir arquivo gerado na linha anterior
                nowmachine = vmstate.readlines()[1].split()[1]
                system('rm -r vmstate.txt')
                return nowmachine == "on"
        except Exception as e:
            print(e)

    def turnon(self):
        if self.status() == True:
            print("The virtual machine it's already turn on")
        else:
            system('vim-cmd vmsvc/power.on {}'.format(self.vmid))	#ligar maquina
            sleep(15)
            #verificar se a máquina já foi de fato ligada
            if self.status():
                self.on = True
            else:
                attempts = 0
                while attempts < 3: #esta repetição verificara se a maquina virtual realmente ligou
                    self.on = False
                    sleep(5)
                    if not self.status():
                        attempts += 1 #se ainda nao ligou, teste novamente
                    else:
                        self.on = True #se ela ja ligou, continue com o codigo
                        break

                    if attempts == 3: #se houve 3 tentativas e a VM nao ligou, gere uma exceção
                        self.on = False
                        print("Error! 30s timeout reached and VM didn't turn on.")
                        raise Exception

    def turnoff(self):
        if self.status() == False:
            print("The virtual machine is already turned off.")
        else:
            system('vim-cmd vmsvc/power.shutdown {}'.format(self.vmid))	#desligar maquina
            sleep(15)
            #verificar se a máquina já foi de fato desligada
            if not self.status():
                self.on = False
            else:
                attempts = 0
                while attempts < 3: #esta repetição verificara se a maquina virtual realmente desligou
                    self.on = True
                    sleep(5)
                    if self.status():
                        attempts += 1 #se ainda nao desligou, teste novamente
                    else:
                        self.on = False #se ela ja desligou, continue com o codigo
                        break
                    if attempts == 3: #se houve 3 tentativas e a VM nao desligou, gere uma exceção
                        self.on = True
                        print("Error! 30s timeout reached and VM didn't turn off.")
                        raise Exception