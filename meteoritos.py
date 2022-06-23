import pygame
import sys
from pygame.locals import *
# importar nuestras clases
from clases import jugador
from clases import asteroide
from random import randint
import time

#variables
ancho = 480
alto= 700
listaAsteroide=[]
puntos = 0
vida = 3
colorFuente=(209,92,94)
jugando =True


#Cargar asteroides------------------------------
def cargarAsteroides(x, y):
    meteoro = asteroide.Asteroide(x, y)
    listaAsteroide.append(meteoro)
def gameOver():
    global jugando
    global puntos
    jugando =False
    for meteoritos in listaAsteroide:
        listaAsteroide.remove(meteoritos)
#-----------------------------------------------


#Funcion prinsipal--------------------------------
def meteoritos():
    pygame.init()
    ventana = pygame.display.set_mode((ancho,alto))
    #Imagen de fondo
    fondo = pygame.image.load("imagenes/fondo.png")
    #Titulo
    pygame.display.set_caption("Meteoritos")
    #Crea objeto jugador
    nave = jugador.Nave()
    contador=0
    #Sonidos
    pygame.mixer.music.load("sonidos/fondo.wav")
    pygame.mixer.music.play(3)
    sonidoColicion = pygame.mixer.Sound("sonidos/colision.aiff")
    #fuentes
    fuenteMarcador = pygame.font.SysFont("Arial",23)
    #ciclo
    while True:
        ventana.blit(fondo,(0,0))
        nave.dibujar(ventana)
        #tiempo
        tiempo = time.perf_counter()
        #marcador
        global puntos
        global vida
        textoMarcador = fuenteMarcador.render("Puntos: "+str(puntos),0,colorFuente)
        vidatext= fuenteMarcador.render("Vida: "+str(vida),0,colorFuente)
        ventana.blit(textoMarcador,(0,0))
        ventana.blit(vidatext,(0,30))
        #Creamos asteroides------------------
        if tiempo - contador > 1:
            contador = tiempo
            posX = randint(2,278)
            cargarAsteroides(posX,0)
        #Comprobamos lista asteroide---------
        if len(listaAsteroide)>0:
            for x in listaAsteroide:
                if jugando ==True:
                    x.dibujar(ventana)
                    x.recorrido()
                if x.rect.top > 700:
                    listaAsteroide.remove(x)
                else:
                    #VIDA ANALISAR
                    if x.rect.colliderect(nave.rect):
                        listaAsteroide.remove(x)
                        nave.vida=False
                        sonidoColicion.play()
                        gameOver()
        
        #disparo del poryectil
        if len(nave.listaDisparo)>0:
            for x in nave.listaDisparo:
                x.dibujar(ventana)
                x.recorrido()
                if x.rect.top<-10:
                    nave.listaDisparo.remove(x)
                else:
                    for meteoritos in listaAsteroide:
                        if x.rect.colliderect(meteoritos.rect):
                            listaAsteroide.remove(meteoritos)
                            nave.listaDisparo.remove(x)
                            puntos+=1

        nave.mover()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type==pygame.KEYDOWN:
                if jugando ==True:
                    if evento.key == K_LEFT:
                        nave.rect.left-=nave.velocidad
                    elif evento.key == K_RIGHT:
                        nave.rect.right+= nave.velocidad
                    elif evento.key == K_SPACE:
                        x, y= nave.rect.center
                        nave.disparar(x, y)
        if jugando ==False:
            FuenteGameOver=pygame.font.SysFont("Arial",40)
            textoGameOver=FuenteGameOver.render("Game Over",0,colorFuente)
            ventana.blit(textoGameOver,(140,350))     
            pygame.mixer.music.fadeout(3000)       
        pygame.display.update()

#llamar funcion
meteoritos()
