import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.json","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.json","w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("base.json","r")
    dados = banco.read()
    banco.close()
    print("dados",type(dados))
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("base.json","w")
    banco.write(json.dumps(dadosDict))
    banco.close()