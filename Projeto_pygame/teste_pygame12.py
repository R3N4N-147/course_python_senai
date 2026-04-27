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

# Estado inicial dos cenários do jogo
status_jogo = "MENU" # Pode ser "MENU", "JOGANDO" ou "GAME_OVER"
imagem_menu = pygame.image.load("image/menu_jogo.png")
imagem_menu = pygame.transform.scale(imagem_menu, (largura, altura))

wallpaper = pygame.image.load("image/background_lufy_022.png")  # carrega a imagem do cenário do jogo
wallpaper = pygame.transform.scale(wallpaper, (largura, altura)) # redimensiona
x_wallpaper = 0 # Variável para fazer o cenário andar

# Estado inicial do character e objetos do jogo
x_lufy,y_lufy = 100,500
largura_personagem, altura_personagem = 60, 100 
char_1 = pygame.image.load("sprites/luffy_sprite_5002.png") # Carrega o sprite do character
char_1 = pygame.transform.scale(char_1, (largura_personagem, altura_personagem)) # Redimensiona o sprite
luffy_vel_y, luffy_no_ar = 0, False # Usado para a função pulo

corrimao = pygame.image.load("image/background_lufy_023.png")
corrimao = pygame.transform.scale(corrimao, (largura, 200))
x_corrimao = 0 # Variável para fazer o corrimão andar

# Construcao da funcao pulo, variaveis globais
altura_do_chao = 500 # Ajuste para a nova altura do personagem
altura_do_floor = 350 # usar para 1o andar (piso intermediário).
gravidade = 0.5

pontos = 0 # Var para potuação
fonte = pygame.font.SysFont("arial", 30, bold=True) # Escolhe a fonte, tamanho e negrito
vidas_char = 3 # Var para vidas
vidas_oponente = 3 # Var para vidas do oponente (se for implementar um oponente)

# Obstaculos iniciais
barril_01 = pygame.image.load("sprites/barril_01.png")
altura_barril = 100
largura_barril = 100
barril_01 = pygame.transform.scale(barril_01, (largura_barril, altura_barril))
x_barril = largura # distancia máxima. Começa fora da tela na direita
# y_barril = 550 # nao precisa mais. pois adotei altura_do_chao...
velocidade_jogo_barril = 0 # var para acelerar a velocidade do barril. 
# Depois eu deveria pensar em uma classe para usar melhor isso com objetos e funcoes

controle_frame = pygame.time.Clock() # controle de frames do jogo, para limitar a taxa de atualização da tela

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
# Versao 9 - Trabalhar na Colisao
# Versao 10 - pontos
# Versao 11 - vidas
# Versao 12 - Vou começar a trabalhar no menu
# Versao 13 - mudar a logica do menu para clicar sobre o objeto, ao invés de apertar enter. E adicionar a opção de sair do jogo no menu. 
# Talvez seja melhor criar um menu separado, com uma classe para organizar melhor as coisas.

# Loop principal do jogo
while True:
    for event in pygame.event.get(): # percorre a lista de eventos do pygame
        if event.type == QUIT: # se o evento for do tipo QUIT
            pygame.quit() # fecha o pygame
            exit() # fecha o sistema
        if status_jogo == "MENU" and event.type == KEYDOWN:
            if event.key == K_RETURN: # Pressiona Enter para começar
                status_jogo = "JOGANDO"
                # Reseta variáveis se necessário
                vidas_char = 3
                pontos = 0
                # adicionar outras variáveis que precisam ser resetadas aqui?

    if status_jogo == "MENU":
        tela.blit(imagem_menu, (0, 0)) # Desenha a imagem do menu na tela

    elif status_jogo == "JOGANDO":
        # captura de teclas
        keys = pygame.key.get_pressed() # captura o estado atual de todas as teclas
        # Cenario 
        # (Lembrete: Eu chamo o cenário 2x para criar o efeito de continuidade, e depois reseto a posição para criar o loop infinito)
        tela.blit(wallpaper, (x_wallpaper, 0)) # Desenha o 1º fundo na posição (0,0)
        tela.blit(wallpaper, (x_wallpaper + largura, 0)) # Desenha o 2º fundo na posição (largura,0) para criar o efeito de continuidade
        # Cenario - movimento
        x_wallpaper -= 3 # desliza p/ esquerda
        # x_wallpaper -= 2 # desliza p/ esquerda MUDAR a velocidade tras um efeito visual diferente
        if x_wallpaper < -largura:
            x_wallpaper = 0 # reseta a posição

        # Personagem
        # pygame.draw.circle(tela, (255, 0, 0), (x_lufy, y_lufy), 20) # desenha um círculo vermelho representando o personagem
        tela.blit(char_1, (x_lufy, y_lufy)) # Desenha o sprite do Luffy na posição (x_lufy, y_lufy)
        # Personagem - Movimento
        # if pygame.key.get_pressed()[K_w] and not luffy_no_ar:
        if keys[K_w] and not luffy_no_ar:
            luffy_no_ar = True
            luffy_vel_y = -15 # altura do pulo (velocidade inicial do pulo)
            # Aplica a função no Luffy

        y_lufy, luffy_vel_y, luffy_no_ar = pulo(y_lufy, luffy_vel_y, luffy_no_ar)

        # Barril
        # blit (x,y)
        tela.blit(barril_01, (x_barril, altura_do_chao)) # Desenha o barril
        # ALTEREI a altura do barril para a mesma do chão do Luffy, para facilitar a colisão.

        # Barril - movimento
        x_barril -= 7 + velocidade_jogo_barril # Movimento (Velocidade do obstáculo)
        # lembrete: a operação acontece da esquerda para a direita
        # primeiro o valor de velocidade_jogo_barril é somado a 7, e depois o resultado é subtraído de x_barril.
        # -7
        # -8
        # -9 e assim por diante, aumentando a velocidade do barril conforme a pontuação aumenta.
        if x_barril < -50:
            x_barril = largura # Renasce na direita
            pontos += 1 # Aumenta a pontuação quando o barril passa pro lado esquerdo após sair da tela 50 pixels
            # pontos += 20 # Para testes
            # mais sobre pontuacao mais abaixo ...
            if pontos % 50 == 0: # A cada "pontos % x", aumenta a velocidade do barril
                velocidade_jogo_barril += 1 # Aumenta a velocidade do barril

        # Corrimao
        # tela.blit(corrimao, (0, 100))
        tela.blit(corrimao, (x_corrimao, 100)) # Desenha o corrimão na sobre-posição (a "ordem importa"...)
        tela.blit(corrimao, (x_corrimao + largura, 100)) #
        # Corrimão - movimento
        x_corrimao -= 3 # desliza p/ esquerda
        if x_corrimao < -largura:
            x_corrimao = 0 # reseta a posição

        # Colisão - usando retângulos para detectar a colisão entre o personagem e o barril
        luffy_rect = pygame.Rect(x_lufy, y_lufy, largura_personagem-10, altura_personagem-5) # Cria um retângulo para o Luffy
        barril_rect = pygame.Rect(x_barril, altura_do_chao, largura_barril, altura_barril) # Cria um retângulo para o barril
        # lógica da colisão
        if luffy_rect.colliderect(barril_rect): # Verifica se os retângulos colidem 
            vidas_char -= 1 # -1 vida do character
            x_barril = largura # Renasce na direita
            if vidas_char <= 0:
                status_jogo = "MENU" # Muda o estado do jogo
                x_barril = largura
                velocidade_jogo_barril = 0
                y_lufy = 500
                luffy_vel_y = 0
                luffy_no_ar = False

        # Exibe a pontuação
        mensagem = f"Pontos: {pontos}" # Formata o texto
        texto_formatado = fonte.render(mensagem, True, (255, 255, 255)) # Renderiza (Texto, Anti-aliasing, Cor Branca)
        tela.blit(texto_formatado, (600, 30)) # Desenha no canto superior direito
        # Vidas
        msg_vidas = f"Vidas: {vidas_char}"
        texto_vidas = fonte.render(msg_vidas, True, (255, 0, 0)) # Vermelho
        tela.blit(texto_vidas, (30, 30)) # Desenha no canto superior esquerdo

    pygame.display.update() # atualiza a tela do jogo
    controle_frame.tick(60) # limita a taxa de atualização da tela para 60 frames por segundo