import pygame # importa a biblioteca toda do pygame
from pygame.locals import * # importa todo o conteúdo da "pasta" locals
from sys import exit # importa a funcionalidade de fechar do sistema

# Inicializa o Pygame
pygame.init()
# Configura a janela do jogo
largura = 800 # largura da janela do jogo
altura = 600 # altura da janela do jogo
tela = pygame.display.set_mode((largura,altura)) # tamanho da janela do jogo, sendo números inteiros
pygame.display.set_caption("Pygame - Luffy Revenge") # titulo da janela do jogo

# Estado inicial do personagem

# x_lufy = 100 # posição horizontal do personagem, da esquerda para a direita
# y_lufy = 550 # posição vertical do personagem, de cima para baixo 
x_lufy,y_lufy = 100,500
# largura_personagem, altura_personagem = 120, 200 # largura e altura do personagem # revisar esse numero
largura_personagem = 60 # largura do personagem # revisar esse numero
altura_personagem = 100 # altura do personagem # revisar esse numero
char_1 = pygame.image.load("sprites/luffy_sprite_5002.png") # Carrega o sprite do Luffy
# Testei e faltou ajustar a posicao nova e tamanho do char_1
char_1 = pygame.transform.scale(char_1, (largura_personagem, altura_personagem)) # Redimensiona o sprite
# Necessário para a função pulo
luffy_vel_y = 0
luffy_no_ar = False

controle_frame = pygame.time.Clock() # controle de frames do jogo, para limitar a taxa de atualização da tela
wallpaper = pygame.image.load("image/background_lufy_022.png")  # carrega a imagem do cenário do jogo
wallpaper = pygame.transform.scale(wallpaper, (largura, altura)) # redimensiona
x_wallpaper = 0 # Variável para fazer o cenário andar

corrimao = pygame.image.load("image/background_lufy_023.png")
corrimao = pygame.transform.scale(corrimao, (largura, 200))
x_corrimao = 0 # Variável para fazer o corrimão andar

# Construcao da funcao pulo, variaveis globais
gravidade = 0.5
# altura_do_chao = 550
altura_do_chao = 500 # Ajuste para a nova altura do personagem
# altura_do_chao2 = 550 # usar p/ andar intermediário.

# Obstaculos iniciais
barril_01 = pygame.image.load("sprites/barril_01.png")
altura_barril = 100
largura_barril = 100
barril_01 = pygame.transform.scale(barril_01, (largura_barril, altura_barril))
x_barril = largura # distancia máxima. Começa fora da tela na direita
y_barril = 550     # MESMA altura do chão do Luffy


# 
def pulo(y_atual, vel_y, no_ar): # parametros
    if no_ar: # verifica se o personagem está no ar
        y_atual += vel_y
        vel_y += gravidade
        if y_atual >= altura_do_chao:
            y_atual = altura_do_chao
            no_ar = False
            vel_y = 0
    return y_atual, vel_y, no_ar

# Versao 7 - testando o primeiro obstaaculo.
# Versao 8 - trocando o circle pelo sprite do luffy.
# Vou criar uma funcao sprite fora loop, colocar uma flag de estado e trocar o sprite conforme a situacao ou fase
# Depois tenho que voltar e trabalhar na colisao, pontuação ... ainda tem a questao do menu.

# Loop principal do jogo
while True:
    for event in pygame.event.get(): # percorre a lista de eventos do pygame
        if event.type == QUIT: # se o evento for do tipo QUIT
            pygame.quit() # fecha o pygame
            exit() # fecha o sistema

    # Cenario
    tela.blit(wallpaper, (x_wallpaper, 0)) # Desenha o fundo na posição (0,0)
    tela.blit(wallpaper, (x_wallpaper + largura, 0))
    # Cenario - movimento
    x_wallpaper -= 3 # desliza p/ esquerda
    # x_wallpaper -= 2 # desliza p/ esquerda MUDAR A VEL tras um efeito visual diferente
    if x_wallpaper < -largura:
        x_wallpaper = 0 # reseta a posição

    # Personagem
    # pygame.draw.circle(tela, (255, 0, 0), (x_lufy, y_lufy), 20) # desenha um círculo vermelho representando o personagem
    tela.blit(char_1, (x_lufy, y_lufy)) # Desenha o sprite do Luffy na posição (x_lufy, y_lufy)
    # Personagem - Movimento
    if pygame.key.get_pressed()[K_w] and not luffy_no_ar:
        luffy_no_ar = True
        luffy_vel_y = -15 # altura do pulo (velocidade inicial do pulo)
    # Aplica a função no Luffy
    y_lufy, luffy_vel_y, luffy_no_ar = pulo(y_lufy, luffy_vel_y, luffy_no_ar)

    # Barril
    # blit (x,y)
    tela.blit(barril_01, (x_barril, y_barril-(altura_barril//2))) # Desenha o barril
    # Tive alguma dificuldade para alinhar a altura do barril na tela do jogo
    # Quando aprender a colisao, tem que prestar atencao nisso.
    # quando eu começo com personagens novos
    # Tenho esquecido de inserir eles na tela AQUI
    # pelo menos eu já sei exatamente onde vir na sequencia ...

    # Barril - movimento
    x_barril -= 7 # Velocidade do obstáculo
    if x_barril < -50:
        x_barril = largura # Renasce na direita

    # Corrimão
    # tela.blit(corrimao, (0, 100))
    tela.blit(corrimao, (x_corrimao, 100)) # Desenha o corrimão na sobre-posição (chamei a "ordem importa"...)
    tela.blit(corrimao, (x_corrimao + largura, 100))
    # Corrimão - movimento
    x_corrimao -= 3 # desliza p/ esquerda
    if x_corrimao < -largura:
        x_corrimao = 0 # reseta a posição

    pygame.display.update() # atualiza a tela do jogo
    controle_frame.tick(60) # limita a taxa de atualização da tela para 60 frames por segundo