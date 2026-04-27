# Configure o ambiente em Python, no nosse caso ambiente VSCode, para usar o Pygame.
# Certifique-se de ter o Pygame instalado. 
# Para fazer isso, no terminal (não é aqui) digite: pip install pygame
# Obtendo sucesso na instalação do Pygame, podemos prosseguir para o próximo passo.

# Agora, vamos criar um arquivo Python para testar o Pygame.

import pygame # importa a biblioteca toda do pygame
from pygame.locals import * # importa todo o conteúdo da "pasta" locals
from sys import exit # importa a funcionalidade de fechar do sistema

# Inicializa o Pygame
pygame.init()
# Configura a janela do jogo
largura = 800 # largura da janela do jogo
altura = 600 # altura da janela do jogo
tela = pygame.display.set_mode((largura,altura)) # tamanho da janela do jogo, sendo números inteiros
pygame.display.set_caption("Pygame - LufyRun") # titulo da janela do jogo

# Estado inicial do personagem
x_lufy = 50 # posição horizontal do personagem, da esquerda para a direita
y_lufy = 450 # posição vertical do personagem, de cima para baixo
largura_personagem = 20 # largura do personagem # revisar esse numero
altura_personagem = 20 # altura do personagem # revisar esse numero

# Loop principal do jogo
while True:
    for event in pygame.event.get(): # percorre (iterage) a lista de eventos do pygame
        if event.type == QUIT: # se o evento for do tipo QUIT, ou seja, fechar a janela
            pygame.quit() # fecha o pygame
            exit() # fecha o sistema

    tela.fill((255, 255, 255)) # preenche a tela com a cor branca
    #Tela de fundo do jogo, ou seja, o cenário do jogo
    # código para desenhar o cenário do jogo aqui

    # código para desenhar o personagem do jogo aqui
    # método .circle(), onde o primeiro argumento é a superfície onde o círculo será desenhado, 
    #                        o segundo argumento é a cor do círculo (neste caso, vermelho: 255, 0, 0), 
    #                        o terceiro argumento é a posição do centro do círculo (x_lufy, y_lufy) e 
    #                        o quarto argumento é o raio do círculo (20)
    pygame.draw.circle(tela, (255, 0, 0), (x_lufy, y_lufy), 20) # desenha um círculo vermelho representando o personagem
    if pygame.key.get_pressed()[K_a]:   x_lufy -=1
    if pygame.key.get_pressed()[K_w]:   y_lufy -=1
    if pygame.key.get_pressed()[K_s]:   y_lufy +=1
    if pygame.key.get_pressed()[K_d]:   x_lufy +=1
    # Limites da tela para o personagem 
    # Modificar o códigopara restringir dentro de um limite.
    if x_lufy > largura:
        x_lufy = 0 - largura_personagem
    if x_lufy < 0 - largura_personagem:
        x_lufy = largura
    if y_lufy > altura:
        y_lufy = 0 - altura_personagem
    if y_lufy < 0 - altura_personagem:
        y_lufy = altura

    
    pygame.display.update() # atualiza a tela do jogo
