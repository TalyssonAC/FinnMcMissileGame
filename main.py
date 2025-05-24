import pygame
import random
import os
import json
import math
import speech_recognition as sr
from datetime import datetime
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.util import inverterNome

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Iron Man do Marcão")
icone  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
iron = pygame.image.load("assets/FinnMcMissile.png")
fundoStart = pygame.image.load("assets/fundoStart.jpg")
fundo = pygame.image.load("assets/fundo.png")
fundoDead = pygame.image.load("assets/fundoDead.png")
missel = pygame.image.load("assets/missile.png")
missileSound = pygame.mixer.Sound("assets/missile.wav")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("assets/finnsound.mp3")

def reconhecer_pontuacao():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language="pt-BR")
        return texto
    except:
        return ""

def escrever_log(nome, pontos):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("log.dat", "a") as f:
        f.write(f"{nome},{pontos},{data_hora}\n")

def jogar(nome):

    lanes = [35, 275, 500, 750]
    largura_lane = lanes[1] - lanes[0]

    larguraPersona = 236
    alturaPersona = 135
    larguaMissel  = 50
    alturaMissel  = 250

    current_lane = 1
    posicaoYPersona = 550 
    posicaoXPersona = lanes[current_lane] + (largura_lane - larguraPersona) // 2
    lane_index = random.randint(0, 3)
    posicaoXMissel = lanes[lane_index] + (largura_lane - larguaMissel) // 2
    posicaoYMissel = -240
    velocidadeMissel = 5

    segundo_missel_ativo = False
    posicaoYMissel2 = -600
    lane_index2 = random.randint(0, 3)
    posicaoXMissel2 = lanes[lane_index2] + (largura_lane - larguaMissel) // 2
    velocidadeMissel2 = 5

    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    dificuldade  = 30
    paused = False
    frame = 0

    fundo_y = 0
    fundo_altura = fundo.get_height()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    paused = not paused
                elif not paused:
                    if evento.key == pygame.K_RIGHT and current_lane < 3:
                        current_lane += 1
                        posicaoXPersona = lanes[current_lane] + (largura_lane - larguraPersona) // 2
                    elif evento.key == pygame.K_LEFT and current_lane > 0:
                        current_lane -= 1
                        posicaoXPersona = lanes[current_lane] + (largura_lane - larguraPersona) // 2

        if paused:
            tela.blit(fundo, (0, fundo_y))
            if fundo_y + fundo_altura > tamanho[1]:
                tela.blit(fundo, (0, fundo_y - fundo_altura))
            texto_pause = fonteMorte.render("PAUSE", True, (255,255,0))
            rect = texto_pause.get_rect(center=(tamanho[0]//2, tamanho[1]//2))
            tela.blit(texto_pause, rect)
            pygame.display.update()
            relogio.tick(60)
            continue

        fundo_y += max(4, velocidadeMissel // 2)
        if fundo_y >= fundo_altura:
            fundo_y = 0
        tela.blit(fundo, (0, fundo_y))
        if fundo_y + fundo_altura > tamanho[1]:
            tela.blit(fundo, (0, fundo_y - fundo_altura))

        tela.blit(iron, (posicaoXPersona, posicaoYPersona))

        posicaoYMissel += velocidadeMissel
        if posicaoYMissel > 700:
            posicaoYMissel = -240
            pontos += 1
            velocidadeMissel += 1
            lane_index = random.randint(0, 3)
            posicaoXMissel = lanes[lane_index] + (largura_lane - larguaMissel) // 2
            pygame.mixer.Sound.play(missileSound)

        tela.blit(missel, (posicaoXMissel, posicaoYMissel))

        if pontos >= 30:
            segundo_missel_ativo = True

        if segundo_missel_ativo:
            posicaoYMissel2 += velocidadeMissel2
            if posicaoYMissel2 > 700:
                posicaoYMissel2 = -240
                lane_index2 = random.randint(0, 3)
                posicaoXMissel2 = lanes[lane_index2] + (largura_lane - larguaMissel) // 2
                pygame.mixer.Sound.play(missileSound)
            tela.blit(missel, (posicaoXMissel2, posicaoYMissel2))

        texto = fonteMenu.render("Pontos: "+str(pontos), True, preto)
        tela.blit(texto, (15,15))
        msg1 = fonteMenu.render("< >: Mover-se", True, preto)
        msg2 = fonteMenu.render("ESC: Pausa", True, preto)
        tela.blit(msg1, (15,40))
        tela.blit(msg2, (15,60))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))

        colisao1 = (
            len(set(pixelsMisselY).intersection(pixelsPersonaY)) > dificuldade and
            len(set(pixelsMisselX).intersection(pixelsPersonaX)) > dificuldade
        )

        colisao2 = False
        if segundo_missel_ativo:
            pixelsMissel2X = list(range(posicaoXMissel2, posicaoXMissel2 + larguaMissel))
            pixelsMissel2Y = list(range(posicaoYMissel2, posicaoYMissel2 + alturaMissel))
            colisao2 = (
                len(set(pixelsMissel2Y).intersection(pixelsPersonaY)) > dificuldade and
                len(set(pixelsMissel2X).intersection(pixelsPersonaX)) > dificuldade
            )

        if colisao1 or colisao2:
            escrever_log(nome, pontos)
            dead(pontos)

        pygame.display.update()
        relogio.tick(60)

def pedir_nome():
    nome = ""
    ativo = True
    input_box = pygame.Rect(400, 370, 200, 40)
    box_rect = pygame.Rect(350, 300, 300, 200)
    cor_box = (0, 0, 0)
    cor_borda = (60, 60, 60)
    cor_input = pygame.Color('lightskyblue3')
    fonte = pygame.font.SysFont("arial", 36)
    fonte_titulo = pygame.font.SysFont("arial", 28, bold=True)

    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nome.strip() == "":
                        nome = "Jogador"
                    return nome
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 15 and evento.unicode.isprintable():
                        nome += evento.unicode

        tela.blit(fundoStart, (0,0))
        pygame.draw.rect(tela, cor_box, box_rect, border_radius=25)
        pygame.draw.rect(tela, cor_borda, box_rect, 4, border_radius=25)
        txt = fonte_titulo.render("Digite seu nome:", True, (255,255,255))
        tela.blit(txt, (box_rect.x + 50, box_rect.y + 30))
        pygame.draw.rect(tela, cor_input, input_box, 2, border_radius=10)
        txt_nome = fonte.render(nome, True, (255,255,255))
        tela.blit(txt_nome, (input_box.x+10, input_box.y+5))
        pygame.display.flip()
        relogio.tick(30)

def mostrar_botao_jogar(nome):
    botao_largura = 200
    botao_altura = 60
    botao_x = (tamanho[0] - botao_largura) // 2
    botao_y = (tamanho[1] - botao_altura) // 2
    fonte_botao = pygame.font.SysFont("arial", 36, bold=True)
    azul = (0, 120, 255)
    while True:
        tela.blit(fundoStart, (0,0))
        botao_rect = pygame.draw.rect(tela, azul, (botao_x, botao_y, botao_largura, botao_altura), border_radius=20)
        texto = fonte_botao.render("JOGAR", True, (255,255,255))
        tela.blit(texto, (botao_x + (botao_largura-texto.get_width())//2, botao_y + (botao_altura-texto.get_height())//2))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    return nome
        relogio.tick(60)

def dead(pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40

    if os.path.exists("log.dat"):
        with open("log.dat", "r") as f:
            linhas = f.readlines()[-5:]
    else:
        linhas = []

    falou_pontuacao = False

    box_rect = pygame.Rect(250, 120, 500, 350)
    cor_box = (0, 0, 0)
    cor_borda = (60, 60, 60)
    fonte_titulo = pygame.font.SysFont("arial", 32, bold=True)

    while True:
        tela.blit(fundoDead, (0,0))
        
        pygame.draw.rect(tela, cor_box, box_rect, border_radius=25)
        pygame.draw.rect(tela, cor_borda, box_rect, 4, border_radius=25)

        tela.blit(fonte_titulo.render("Últimas partidas:", True, (255,255,255)), (box_rect.x + 20, box_rect.y + 20))
        
        for i, linha in enumerate(linhas):
            tela.blit(fonteMenu.render(linha.strip(), True, (255,255,0)), (box_rect.x + 20, box_rect.y + 70 + i*30))
        
        tela.blit(fonteMenu.render(f"Sua pontuação: {pontos}", True, (255,255,255)), (box_rect.x + 20, box_rect.y + 230))
        
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))

        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))

        pygame.display.update()

        if not falou_pontuacao:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(f"Sua pontuação foi {pontos}")
            engine.runAndWait()
            falou_pontuacao = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    pygame.mixer.music.play(-1)
                    nome = pedir_nome()
                    jogar(nome)
                if quitButton.collidepoint(evento.pos):
                    quit()
        relogio.tick(60)

def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40

    while True:
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))

        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    nome = pedir_nome()
                    jogar(nome)
                if quitButton.collidepoint(evento.pos):
                    quit()
        relogio.tick(60)

start()