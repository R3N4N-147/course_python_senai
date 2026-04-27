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

x_lufy = largura // 2 # posição horizontal do personagem, da esquerda para a direita
y_lufy = altura // 2 # posição vertical do personagem, de cima para baixo

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


    
    pygame.display.update() # atualiza a tela do jogo
