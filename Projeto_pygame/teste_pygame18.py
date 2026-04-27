import pygame # importa a biblioteca toda do pygame
import random # V.18
from pygame.locals import * # importa todo o conteúdo da "pasta" locals
from sys import exit # importa a funcionalidade de fechar do sistema

# 1. Inicializa o Pygame
pygame.init()

# 2. Configura a janela do jogo
largura, altura = 800,600 # janela do jogo (x,y)
tela = pygame.display.set_mode((largura,altura)) # tamanho da janela do jogo, sendo números inteiros
pygame.display.set_caption("Pygame - Luffy Revenge") # titulo da janela do jogo
controle_frame = pygame.time.Clock() # controle de frames do jogo, para limitar a taxa de atualização da tela
fonte = pygame.font.SysFont("arial", 30, bold=True) # Escolhe a fonte, tamanho e negrito

# 3. Estados e Sistema de Score
status_jogo = "MENU" # Pode ser "MENU", "JOGANDO" ou "GAME_OVER"
exibir_scores = False # Toggle para exibir a janela Ranking no menu
nome_temp = "" # Guarda o que o jogador digita no Game Over
lista_scores = [] # Guardará dicionários: {"nome": "Luffy", "pontos": 100} - Top 3 

# 4. Imagens - Cenários do jogo e Interface
imagem_menu = pygame.image.load("image/menu_jogo.png")
imagem_menu = pygame.transform.scale(imagem_menu, (largura, altura))

wallpaper = pygame.image.load("image/background_lufy_022.png")  # carrega a imagem do cenário do jogo
wallpaper = pygame.transform.scale(wallpaper, (largura, altura)) # redimensiona

corrimao = pygame.image.load("image/background_lufy_023.png")
corrimao = pygame.transform.scale(corrimao, (largura, 200))

quadro_ranking = pygame.image.load("image/menu_jogo4.png") # Nova imagem para score
quadro_ranking = pygame.transform.scale(quadro_ranking, (350, 250)) # Tamanho x,y

img_fruta = pygame.image.load("sprites/demon_fruits (1).png")
img_fruta = pygame.transform.scale(img_fruta, (40, 40))

# 5. Imagens - Personagem e Objetos
largura_personagem, altura_personagem = 60, 100 # original tem 120x198
char_1 = pygame.image.load("sprites/luffy_sprite_5002.png") # Carrega o sprite do character
char_1 = pygame.transform.scale(char_1, (largura_personagem, altura_personagem)) # Redimensiona o sprite
char_corrida = pygame.image.load("sprites/luffy_sprite_5003.png") # Versao 17 
char_corrida = pygame.transform.scale(char_corrida, (largura_personagem, altura_personagem)) # Versao 17

altura_barril, largura_barril = 100, 100
barril_01 = pygame.image.load("sprites/barril_01.png")
barril_01 = pygame.transform.scale(barril_01, (largura_barril, altura_barril))

img_coracao = pygame.image.load("sprites/heart_1_short.png") # Versao 16
img_coracao = pygame.transform.scale(img_coracao, (30, 30)) # Versao 16

# 6. Variaveis do Jogo - Física e Status (Estado inicial do character e objetos do jogo)
x_lufy,y_lufy = 100,500 # Posicao (x,y) inicial do personagem no jogo
luffy_vel_y, luffy_no_ar = 0, False # Usado para a função pulo
x_wallpaper = 0 # Variável para fazer o cenário andar
x_corrimao = 0 # Variável para fazer o corrimão andar
x_barril = largura # distancia máxima. Começa fora da tela na direita
# y_barril = 550 # No y que usa essa dimensão adotei 'altura_do_chao'.
velocidade_jogo_barril = 0 # var para acelerar a velocidade do barril. 

pontos = 0 # Var para potuação
vidas_char = 3 # Var para vidas
vidas_oponente = 3 # Var para vidas do oponente (se for implementar um oponente)
altura_do_chao = 500 # Ajuste para a nova altura do personagem
altura_do_floor = 350 # usar para 1o andar (piso intermediário).
gravidade = 0.5

delay_inicio = 180 # V. 17 - Variável de controle do delay (3 segundos = 180 frames a 60 FPS)

# Variáveis da fruta
x_fruta = largura + 50 # Começa fora da tela
y_fruta = 0
fruta_ativa = False
frutas_coletadas = 0

# Funções
def pulo(y_atual, vel_y, no_ar): # parametros
    if no_ar: # verifica se o personagem está no ar
        y_atual += vel_y
        vel_y += gravidade
        if y_atual >= altura_do_chao:
            y_atual = altura_do_chao
            no_ar = False
            vel_y = 0
    return y_atual, vel_y, no_ar

def resetar_jogo(): # V. 17
    global vidas_char, x_barril, velocidade_jogo_barril, y_lufy, delay_inicio, luffy_atual, luffy_no_ar
    vidas_char = 3
    x_barril = largura
    velocidade_jogo_barril = 0
    y_lufy = 500
    delay_inicio = 180
    luffy_atual = char_1 # Volta para o sprite parado (5002)
    luffy_no_ar = False
    frutas_coletadas = 0 # V. 18

# Versao 15 - Score melhorado. Refatoração.
# Versão 16 - Substituir o texto de vidas por Sprites de Coração.
# Versão 17 - Sistema de Delay Inicial (3s) com troca de Sprite (Parado -> Correndo).
# Versão 18 - Implementação da Fruta Demoníaca (Surgimento a cada 20 pontos + Altura randômica + Coleta).
# Versão 19 - Introdução do Barril Triplo e lógica de alternância entre obstáculos.
# Versão 20 - Sistema de Ataque (Tecla Espaço) - Colisão ofensiva e pontuação diferenciada.
# Versão 21 - Animação de Ataque (Sequência dos 5 sprites: 5011, 5013, 5014...).
# Versão 22 - Condições de Vitória da Fase (Tempo Limite + Meta de Frutas e Pontos).

# Loop principal do jogo
while True:
    for event in pygame.event.get(): # percorre a lista de eventos do pygame
        if event.type == QUIT: # se o evento for do tipo QUIT
            pygame.quit() # fecha o pygame
            exit() # fecha o sistema

        # 1. EVENTOS NO MENU
        if status_jogo == "MENU":
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                posicao_mouse = pygame.mouse.get_pos() # pega as posicoes do mouse (x,y)
                print(f"Você clicou em: {posicao_mouse}") # deixar aqui para mais testes futuros

                # BOTAO INICIAR (Ajuste os valores conforme sua imagem) # largura, altura = 800,600 # janela do jogo (x,y)
                if 500 < posicao_mouse[0] < 750 and 100 < posicao_mouse[1] < 200: # posicao do iniciar
                    print(f"Você clicou em INICIAR: {posicao_mouse}") # deixar aqui para mais testes futuros
                    status_jogo = "JOGANDO"
                    resetar_jogo() # <--- Reseta as variaveis V.17
                    pontos = 0 # <------- Zera apenas quando um NOVO jogo clica em iniciar

                # BOTAO SCORE (TOGGLE)
                elif 500 < posicao_mouse[0] < 750 and  250 < posicao_mouse[1] < 350:
                    print(f"Você clicou em SCORE: {posicao_mouse}")
                    exibir_scores = not exibir_scores # Inverte: se True vira False e vice-versa
                
                # BOTAO SAIR
                elif 500 < posicao_mouse[0] < 750 and 400 < posicao_mouse[1] < 500:
                    # print(f"Você clicou em SAIR: {posicao_mouse}")
                    pygame.quit() #
                    exit() #

        # 2. EVENTOS AO DIGITAR NOME
        elif status_jogo == "DIGITANDO_NOME":
            if event.type == KEYDOWN:
                if event.key == K_RETURN: # Apertou Enter, salva e volta pro menu
                    if nome_temp == "": nome_temp = "Pirata Anonimo"
                    novo_score = {"nome": nome_temp, "pontos": pontos}
                    lista_scores.append(novo_score)
                    # Ordena e pega os top 3
                    lista_scores = sorted(lista_scores, key=lambda x: x['pontos'], reverse=True)[:3]
                    status_jogo = "MENU"
                elif event.key == K_BACKSPACE:
                    nome_temp = nome_temp[:-1] # Apaga última letra
                else:
                    # Adiciona a letra digitada (limite de 10 caracteres)
                    if len(nome_temp) < 10:
                        nome_temp += event.unicode

    # DESENHOS E LOGICAS DE ESTADO
    if status_jogo == "MENU":
        tela.blit(imagem_menu, (0, 0)) # Desenha a imagem do menu na tela
        if exibir_scores:
            # Desenha (Janela de Ranking)
            tela.blit(quadro_ranking, (50, 250)) # posicao na tela x=50,y=250
            # Escreve os Top 3
            for i, s in enumerate(lista_scores):
                texto = f"{i+1}. {s['nome']} - {s['pontos']} pts"
                img_texto = fonte.render(texto, True, (255, 255, 255))
                # Ajuste o (100, 180...) conforme o desenho da imagem ranking (score)
                # tela.blit(img_texto, (100, 180 + (i * 45)))
                tela.blit(img_texto, (100, 325 + (i * 45)))

    elif status_jogo == "DIGITANDO_NOME": # V.15
        tela.blit(wallpaper, (0,0)) # Usa o fundo do jogo atrás
        # Um retângulo semi-transparente para o texto não sumir no fundo
        overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        tela.blit(overlay, (0,0))
        
        msg = fonte.render("QUAL O SEU NOME, PIRATA?", True, (255, 215, 0))
        txt_nome = fonte.render(nome_temp + "_", True, (255, 255, 255))
        tela.blit(msg, (largura//2 - 180, altura//2 - 50))
        tela.blit(txt_nome, (largura//2 - 50, altura//2))
    # VERSAO 15

    elif status_jogo == "JOGANDO":
        keys = pygame.key.get_pressed() # captura o estado atual de todas as teclas

        # 1. Traz na tela a imagem (personagens, objetos, etc...)
        # Cenario principal
        # (Lembrete: Eu chamo o cenário 2x para criar o efeito de continuidade, e depois reseto a posição para criar o loop infinito)
        tela.blit(wallpaper, (x_wallpaper, 0)) # Desenha o 1º fundo na posição (0,0)
        tela.blit(wallpaper, (x_wallpaper + largura, 0)) # Desenha o 2º fundo na posição (largura,0) para criar o efeito de continuidade

        # Personagem
        # Antes o .blit do luffy ficava por aqui

        # Barril
        # Antes o .blit do barril ficava por aqui

        # Corrimao - cenario secundario (sobre o principal)
        tela.blit(corrimao, (x_corrimao, 100)) # Desenha o corrimão na sobre-posição (a "ordem importa"...)
        tela.blit(corrimao, (x_corrimao + largura, 100)) #

        # 2. Faz o MOVIMENTO na tela da imagem (personagens, objetos, etc...)
        # --- LÓGICA DO DELAY ---
        if delay_inicio > 0:
            delay_inicio -= 1
            luffy_atual = char_1 # Sprite 5002 (Parado)
            
            # Desenha o número do countdown no centro da tela
            txt_contagem = fonte.render(str((delay_inicio // 60) + 1), True, (255, 255, 0))
            tela.blit(txt_contagem, (largura // 2, altura // 2))
        else:
            luffy_atual = char_corrida # Sprite 5003 (Correndo)
            # Cenario principal - movimento
            x_wallpaper -= 3 # desliza p/ esquerda
            if x_wallpaper <= -largura:
                x_wallpaper = 0 # reseta a posição

            x_barril -= 7 + velocidade_jogo_barril 
            if x_barril < -50:
                x_barril = largura # Renasce na direita
                pontos += 1 # +1 após sair da tela 50 pixels
                if pontos % 50 == 0: # A cada "pontos % x", aumenta a velocidade do barril
                    velocidade_jogo_barril += 1 # Aumenta a velocidade do barril

            # FRUTA DEMONIACA - VERSAO 18
            # Aparecimento da Fruta (a cada 20 pontos)
            if pontos > 0 and pontos % 20 == 0 and not fruta_ativa:
                fruta_ativa = True
                x_fruta = largura
                y_fruta = random.randint(300, 480) # Altura randômica (ajuste conforme o pulo)

            if fruta_ativa:
                x_fruta -= 10 # Fruta viaja mais rápido que o barril
                tela.blit(img_fruta, (x_fruta, y_fruta))
                
                # Colisão Luffy + Fruta
                rect_fruta = pygame.Rect(x_fruta, y_fruta, 40, 40)
                if luffy_rect.colliderect(rect_fruta):
                    frutas_coletadas += 1
                    fruta_ativa = False # Coletou, ela some
                    pontos += 10 # Bônus por pegar a fruta
                
                # Se a fruta sair da tela sem ser coletada
                if x_fruta < -50:
                    fruta_ativa = False
            # FRUTA DEMONIACA - VERSAO 18

            # Corrimao - Movimento: desliza p/ esquerda
            x_corrimao -= 3 
            if x_corrimao < -largura:
                x_corrimao = 0 # reseta a posição
        
        tela.blit(barril_01, (x_barril, altura_do_chao)) # Desenha o barril # blit (x,y)
        tela.blit(luffy_atual, (x_lufy, y_lufy))

        # Personagem - Movimento - V. 17 Tirei o mov do personagem do grupo p/ nao ser atingido pelo delay
        if keys[K_w] and not luffy_no_ar:
            luffy_no_ar = True
            luffy_vel_y = -15 # altura do pulo (velocidade inicial do pulo)
            # Aplica a função no Luffy
        y_lufy, luffy_vel_y, luffy_no_ar = pulo(y_lufy, luffy_vel_y, luffy_no_ar)
        # Barril - Movimento da esq para dir (Velocidade do obstáculo)

        # Colisão - usando retângulos para detectar a colisão entre o personagem e o barril
        luffy_rect = pygame.Rect(x_lufy, y_lufy, largura_personagem-10, altura_personagem-5) # Cria um retângulo para o Luffy
        barril_rect = pygame.Rect(x_barril, altura_do_chao, largura_barril, altura_barril) # Cria um retângulo para o barril
        # lógica da colisão
        if luffy_rect.colliderect(barril_rect): # Verifica se os retângulos colidem 
            vidas_char -= 1 # -1 vida do character
            x_barril = largura # Renasce na direita
            if vidas_char <= 0:                
                # Versao 15
                status_jogo = "DIGITANDO_NOME" # muda status
                nome_temp = "" # Limpa para o novo jogador
                resetar_jogo()

        # Exibe a pontuação
        mensagem = f"Pontos: {pontos}" # Formata o texto
        texto_formatado = fonte.render(mensagem, True, (255, 255, 255)) # Renderiza (Texto, Anti-aliasing, Cor Branca)
        tela.blit(texto_formatado, (600, 30)) # Desenha no canto superior direito
        # Exibe Vidas
        for i in range(vidas_char): # Versao 16 - Vidas
            # Posiciona um ao lado do outro (30px de distância)
            tela.blit(img_coracao, (30 + (i * 35), 30))
        tela.blit(img_fruta, (30, 80)) 
        txt_frutas = fonte.render(f"x {frutas_coletadas}", True, (255, 255, 255))
        tela.blit(txt_frutas, (80, 80))

    pygame.display.update() # atualiza a tela do jogo
    controle_frame.tick(60) # limita a taxa de atualização da tela para 60 frames por segundo