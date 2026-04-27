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
x_lufy = 100 # posição horizontal do personagem, da esquerda para a direita
y_lufy = 550 # posição vertical do personagem, de cima para baixo 
# 550 em y para o personagem ficar na parte de baixo
largura_personagem = 20 # largura do personagem # revisar esse numero
altura_personagem = 20 # altura do personagem # revisar esse numero
luffy_vel_y = 0      # NOVO: Necessário para a função pulo
luffy_no_ar = False  # NOVO: Necessário para a função pulo

controle_frame = pygame.time.Clock() # controle de frames do jogo, para limitar a taxa de atualização da tela
wallpaper = pygame.image.load("image/background_lufy_022.png")  # carrega a imagem do cenário do jogo
wallpaper = pygame.transform.scale(wallpaper, (largura, altura)) # redimensiona
x_wallpaper = 0 # Variável para fazer o cenário andar

corrimao = pygame.image.load("image/background_lufy_023.png")
corrimao = pygame.transform.scale(corrimao, (largura, 200))
x_corrimao = 0 # Variável para fazer o corrimão andar

# versao 5
# Construcao da funcao pulo, variaveis globais
gravidade = 0.5
altura_do_chao = 550
altura_do_chao2 = 550 # usar p/ andar intermediário.

# Ao pressionar w, eu mudo 2 variáveis: luffy_no_ar e luffy_vel_y. 
# A função pulo é chamada a cada frame, e ela verifica se o personagem está no ar (luffy_no_ar). 
# Se estiver, ela atualiza a posição vertical (y_atual) do personagem com base na velocidade vertical (vel_y) 
# e aplica a gravidade para simular a queda. 
# Quando o personagem atinge o chão (altura_do_chao), ele é reposicionado para ficar exatamente no chão, 
# a variável luffy_no_ar é definida como False, e a velocidade vertical é zerada para que o personagem 
# pare de cair. 
# resumo: Pressionar w é o gatilho, while é o loop que faz a gravidade ser aplicada até as var serem resetadas.
def pulo(y_atual, vel_y, no_ar):
    if no_ar: # verifica se o personagem está no ar
        y_atual += vel_y
        vel_y += gravidade
        if y_atual >= altura_do_chao:
            y_atual = altura_do_chao
            no_ar = False
            vel_y = 0
    return y_atual, vel_y, no_ar

# Loop principal do jogo
while True:
    for event in pygame.event.get(): # percorre (iterage) a lista de eventos do pygame
        if event.type == QUIT: # se o evento for do tipo QUIT, ou seja, fechar a janela
            pygame.quit() # fecha o pygame
            exit() # fecha o sistema

    # código para desenhar o cenário do jogo aqui
    # Ordem corrimao na frente, luffy, cenário atrás
    # Cenario
    # tela.blit(wallpaper, (0, 0)) # Desenha o fundo na posição (0,0)
    tela.blit(wallpaper, (x_wallpaper, 0)) 
    tela.blit(wallpaper, (x_wallpaper + largura, 0))
    x_wallpaper -= 3 # desliza p/ esquerda
    if x_wallpaper < -largura:
        x_wallpaper = 0 # reseta a posição

    # Personagem
    pygame.draw.circle(tela, (255, 0, 0), (x_lufy, y_lufy), 20) # desenha um círculo vermelho representando o personagem
    # Corrimão
    # tela.blit(corrimao, (0, 100))
    tela.blit(corrimao, (x_corrimao, 100)) 
    tela.blit(corrimao, (x_corrimao + largura, 100))
    x_corrimao -= 3 # desliza p/ esquerda
    if x_corrimao < -largura:
        x_corrimao = 0 # reseta a posição

    # if pygame.key.get_pressed()[K_a]:   x_lufy -=5
    # if pygame.key.get_pressed()[K_w]:   y_lufy -=5
    # if pygame.key.get_pressed()[K_s]:   y_lufy +=5
    # if pygame.key.get_pressed()[K_d]:   x_lufy +=5
    # # Limites da tela para o personagem 
    # # Modificar o códigopara restringir dentro de um limite.
    # if x_lufy > largura:
    #     x_lufy = 0 - largura_personagem
    # if x_lufy < 0 - largura_personagem:
    #     x_lufy = largura
    # if y_lufy > altura:
    #     y_lufy = 0 - altura_personagem
    # if y_lufy < 0 - altura_personagem:
    #     y_lufy = altura

    if pygame.key.get_pressed()[K_w] and not luffy_no_ar:
        luffy_no_ar = True
        luffy_vel_y = -15 # altura do pulo (velocidade inicial do pulo)

    # Aplica a função no Luffy
    y_lufy, luffy_vel_y, luffy_no_ar = pulo(y_lufy, luffy_vel_y, luffy_no_ar)

    pygame.display.update() # atualiza a tela do jogo
    controle_frame.tick(60) # limita a taxa de atualização da tela para 60 frames por segundo