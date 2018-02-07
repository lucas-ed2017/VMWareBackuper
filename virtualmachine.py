#!/bin/python
# -*- coding: utf-8 -*-
from os import system	#comando system permite dar comandos pelo terminal

class virtualmachine(object):	#inicio da classe
    def __init__(self, name):	#construtor
        self.name = name		#atributo nome
        system('vim-cmd vmsvc/getallvms or vim-cmd vmsvc/getallvms |grep {} > vminfo.txt'.format(self.name))	#gerar arquivo de texto com informações da maquina
        try:
            with open('vminfo.txt') as vmtext:	#abrir arquivo de texto anteriormente gerado
                self.vmid = vmtext.readline()[0:2].strip()	#obter o id e apagar espaços inuteis
            system('vim-cmd vmsvc/power.getstate {} > vmstate.txt'.format(self.vmid))	#gerar arquivo de texto sobre o atual estado da maquina
        except Exception as e:
            print(e)
        try:
            with open('vmstate.txt') as vmstate:	#abrir arquivo gerado na linha anterior
                if vmstate.readlines()[1] == 'Powered on':
                    self.on = True
                else:
                    self.on = False
            	#if vmstate.readlines()[1] == 'Powered on':	#verificar se a maquina está ligada ou desligada e atribuir isso a um atributo booleano sobre a maquina ligada ou não
                #    self.on = True
                #else:
                #   self.on = False
                   
            system('rm -r vminfo.txt') #apagar arquivos de textos agora inuteis
            system('rm -r vmstate.txt')
        except Exception as e:
            print(e)
        

    def turnon(self):
        system('vim-cmd vmsvc/power.on {}'.format(self.vmid))	#ligar maquina
        self.on = True

                

    def turnoff(self):
    	system('vim-cmd vmsvc/power.off {}'.format(self.vmid))	#desligar maquina
    	sleep(15)
    	result = status()
    	if not result:
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
                raise Exception("Error! 30s timeout reached and VM didn't turn off.")
                

    def status(self):
        system('vim-cmd vmsvc/power.getstate {} > vmstate.txt'.format(self.vmid))
        with open('vmstate.txt') as vmstate:
            if vmstate.readlines()[1] == 'Powered on':
                return True
            else:
                return False

    #OBS: Falta o retorno do diretorio
