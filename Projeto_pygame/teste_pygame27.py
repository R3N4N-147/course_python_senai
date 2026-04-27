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

tela_vitoria_img = pygame.image.load("image/tela_vitoria1.png") # < --- V 28
tela_vitoria_img = pygame.transform.scale(tela_vitoria_img, (largura, altura))  # < --- V 28

# 5. Imagens - Personagem e Objetos
largura_personagem, altura_personagem = 60, 100 # original tem 120x198
char_1 = pygame.image.load("sprites/luffy_sprite_5002.png") # Carrega o sprite do character
char_1 = pygame.transform.scale(char_1, (largura_personagem, altura_personagem)) # Redimensiona o sprite
char_corrida = pygame.image.load("sprites/luffy_sprite_5003.png") # Versao 17 
char_corrida = pygame.transform.scale(char_corrida, (largura_personagem + 20, altura_personagem)) # Versao 17

altura_barril, largura_barril = 100, 100
barril_01 = pygame.image.load("sprites/barril_01.png")
barril_01 = pygame.transform.scale(barril_01, (largura_barril, altura_barril))

img_coracao = pygame.image.load("sprites/heart_1_short.png") # Versao 16
img_coracao = pygame.transform.scale(img_coracao, (30, 30)) # Versao 16

largura_triplo, altura_triplo = 150, 150
img_barril_triplo = pygame.image.load("sprites/barril_02.png") # V. 19
img_barril_triplo = pygame.transform.scale(img_barril_triplo, (largura_triplo, altura_triplo))

# Sprites de Ataque - Versão 21
# luffy_ataque_corpo = pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5016.png"), (60, 100))
luffy_energia = pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5026.png"), (80, 60)) # Golpe a frente
luffy_explosao = pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5020.png"), (100, 100))
animacao_ataque = [
    pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5011.png"), (largura_personagem, altura_personagem)),
    pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5012.png"), (largura_personagem + 20, altura_personagem)),
    pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5015.png"), (120, 100)), # Braço esticando
    pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5016.png"), (120, 100))  # Golpe final
]
luffy_energia = pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5026.png"), (150, 60))
luffy_explosao = pygame.transform.scale(pygame.image.load("sprites/luffy_sprite_5020.png"), (100, 100))

# Versão 24
# Imagem do cenário do Boss
wallpaper_boss = pygame.transform.scale(pygame.image.load("image/background_lufy_012.png"), (largura, altura))
# Sprite do Chefe 
img_boss = pygame.transform.scale(pygame.image.load("sprites/z_almirante_ancestral_2002.png"), (80, 120))
img_boss_ataque_1 = pygame.image.load("sprites/z_almirante_ancestral_2003.png") # < ----- V 25.3
img_boss_ataque_1 = pygame.transform.scale(img_boss_ataque_1, (80, 120)) # < ------------ V 25.3
img_boss_ataque_2 = pygame.image.load("sprites/z_almirante_ancestral_2006.png") # < ----- V 25.3
img_boss_ataque_2 = pygame.transform.scale(img_boss_ataque_2, (100, 120)) # < ----------- V 25.3

# 6. Variaveis do Jogo - Física e Status (Estado inicial do character e objetos do jogo)
# Var do char
x_lufy,y_lufy = 100,500 # Posicao (x,y) inicial do personagem no jogo
luffy_vel_y, luffy_no_ar = 0, False # Usado para a função pulo
x_wallpaper = 0 # Variável para fazer o cenário andar
x_corrimao = 0 # Variável para fazer o corrimão andar
x_barril = largura # distancia máxima. Começa fora da tela na direita
# y_barril = 550 # No y que usa essa dimensão adotei 'altura_do_chao'.
velocidade_jogo_barril = 0 # var para acelerar a velocidade do barril. 

# var do BOSS
x_boss = largura + 100 # V. 24
# y_boss = y_lufy # V. 24
y_boss = 480 # V. 24 480 + 120 de altura do sprite

pontos = 0 # Var para potuação
vidas_char = 3 # Var para vidas
vidas_oponente = 3 # Var para vidas do oponente (se for implementar um oponente)
altura_do_chao = 500 # Ajuste para a nova altura do personagem
altura_do_floor = 350 # usar para 1o andar (piso intermediário).
gravidade = 0.5

delay_inicio = 180 # V. 17 - Variável de controle do delay (3 segundos = 180 frames a 60 FPS)

# Variáveis da fruta V. 18
x_fruta = largura + 50 # Começa fora da tela
y_fruta = 0
fruta_ativa = False
frutas_coletadas = 0
proximo_alvo_fruta = 20 # V. 20 Correção na logica da pontuação (tirar 'pontos % 20')

barril_atual = "simples" # Começa com o simples - V. 19
# Variável para saber qual barril está vindo

# # Variáveis de controle de ataque - V. 20
# atacando = False
# duracao_ataque = 0 # Tempo que o "soco" fica ativo

# # Versão 21
# # Variável para controlar se mostramos a explosão
# exibindo_explosao = False
# timer_explosao = 0
# x_explosao, y_explosao = 0, 0
# indice_animacao = 0
# frame_animacao = 0
# VELOCIDADE_ANIMACAO = 8 # Quantos frames cada sprite fica na tela (menor = mais rápido)

# --- Variáveis de Ataque e Animação (Versão 22) ---
atacando = False              # Diz se o Luffy está no meio de um golpe
indice_anim_ataque = 0        # Qual sprite da lista (0 a 3) está passando
timer_anim_ataque = 0         # Contador de frames para trocar o sprite
VELOCIDADE_ANIMACAO = 7       # Tempo de exposição de cada sprite (ajustável)

# --- Variáveis de Impacto/Explosão ---
exibindo_explosao = False     # Liga/Desliga o desenho do sprite 5020
timer_explosao = 0            # Quanto tempo a explosão fica na tela
x_explosao, y_explosao = 0, 0 # Posição onde o barril explodiu

# --- Versão 23: Variáveis de Tempo e Metas ---
# 60 segundos * 60 FPS = 3600 frames
# tempo_fase = 3600 < ------------ Movi para dentro do reset, como chamo o reset bem no começo de cada jogo acho que vai dar certo.
meta_frutas = 3
# meta_pontos = 150 # Ajuste conforme achar melhor para o desafio
meta_pontos = 60

# Versão 24 - BOSS
# metas_batidas = False
# timer_vitoria_fase = 300
# --- Versão 25: Variáveis da IA do Boss ---
status_boss = "MOVENDO" # "MOVENDO", "PISCANDO", "ATACANDO"
timer_boss = 0
vel_boss_x = 3
vel_boss_y = 2
vidas_boss = 6
piscando_boss = False



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
    global vidas_char, x_barril, velocidade_jogo_barril, y_lufy, delay_inicio
    global luffy_atual, luffy_no_ar, frutas_coletadas, proximo_alvo_fruta, tempo_fase
    global metas_batidas, timer_vitoria_fase,  vidas_boss, status_boss, x_boss, timer_boss
    # vidas_char = 3
    vidas_char = 5
    x_barril = largura
    velocidade_jogo_barril = 0
    x_lufy, y_lufy = 100, 500
    delay_inicio = 180
    velocidade_jogo_barril = 0 # < --- V 25.2
    luffy_atual = char_1 # Volta para o sprite parado (5002)
    luffy_no_ar = False
    # Lembrete: 'pontos = 0' estava aqui antes. Movi pontos após a funcao reset (ver ação ação do botão Iniciar Jogo) 
    # Como eu tbm chamo reset quando ele morre, nao dava tempo de salvar a pontuação.
    frutas_coletadas = 0 # V. 18
    proximo_alvo_fruta = 20 # Resetamos o alvo também!
    # tempo_fase = 3600 # V. 23
    tempo_fase = 5400 # 5400 frames / 60 frames = 90 segundos
    metas_batidas = False # V. 25
    timer_vitoria_fase = 300 # V. 25

    # Reset do Boss
    vidas_boss = 5
    status_boss = "MOVENDO"
    x_boss = largura + 100
    timer_boss = 0

# Versão 20 - Sistema de Ataque (Tecla Espaço) - Colisão ofensiva e pontuação diferenciada.
# Versão 21 - Animação de Ataque (Sequência dos 5 sprites: 5011, 5013, 5014...).
# versão 22.py Animação de Ataque - Melhorias. Refatoração. 5 horas.
# versão 23.py Condições de Vitória da Fase (Tempo Limite + Meta de Frutas e Pontos). 1 horas.

# versão 24.py Carregamento do cenário do Chefe e entrada dos personagens. 1 hora.

# versão 25.py Chefe: Movimentação, Piscar e Golpe Indefensável. 2 horas.
# versão 26.py Janela de Vulnerabilidade do Chefe e Sistema de 5 Vidas (Boss). 4 horas.
# versão 27.py Diálogos Finais e Efeito de Degradê (Derrota do Chefe). 1 hora.
# versão 28.py Tela de Vitória Final e Retorno ao Menu Principal. 1 hora.

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
        keys = pygame.key.get_pressed()
        
        # 1. GERENCIAMENTO DE QUAL SPRITE USAR (Lógica de Prioridade)
        if atacando:
            timer_anim_ataque += 1
            if timer_anim_ataque >= VELOCIDADE_ANIMACAO:
                timer_anim_ataque = 0
                indice_anim_ataque += 1
            
            if indice_anim_ataque < len(animacao_ataque):
                luffy_atual = animacao_ataque[indice_anim_ataque]
                # Se for o último frame do ataque (5016), desenha a ENERGIA (5026)
                if indice_anim_ataque == 3:
                    tela.blit(luffy_energia, (x_lufy + 100, y_lufy + 20))
                    # Retângulo invisível do golpe de energia para colisão
                    rect_golpe = pygame.Rect(x_lufy + 100, y_lufy + 20, 150, 60)
            else:
                atacando = False
                indice_anim_ataque = 0
        
        elif luffy_no_ar:
            luffy_atual = char_corrida # Sprite de pulo/corrida
        
        elif delay_inicio > 0:
            luffy_atual = char_1 # Sprite parado 5002
            
        else:
            luffy_atual = char_corrida # Sprite correndo 5003

        # 2. DESENHO DO CENÁRIO (Vem antes dos personagens)
        tela.blit(wallpaper, (x_wallpaper, 0))
        tela.blit(wallpaper, (x_wallpaper + largura, 0))
        tela.blit(corrimao, (x_corrimao, 100))
        tela.blit(corrimao, (x_corrimao + largura, 100))

        # 3. MOVIMENTO DO CENÁRIO E BARRIL (Só se o delay acabou)
        if delay_inicio > 0:
            delay_inicio -= 1
            txt_contagem = fonte.render(str((delay_inicio // 60) + 1), True, (255, 255, 0))
            tela.blit(txt_contagem, (largura // 2, altura // 2))
        else:
            tempo_fase -= 1 # <--- ADICIONE ESTA LINHA AQUI (V.23)

            x_wallpaper -= 3
            if x_wallpaper <= -largura: x_wallpaper = 0
            x_corrimao -= 3
            if x_corrimao <= -largura: x_corrimao = 0
            x_barril -= 7 + velocidade_jogo_barril

            # --- NOVA LÓGICA DE DERROTA POR TEMPO ---
            if tempo_fase <= 0:
                status_jogo = "DIGITANDO_NOME"
                resetar_jogo()

        # 4. GATILHOS DE TECLADO
        if keys[K_w] and not luffy_no_ar and not atacando:
            luffy_no_ar = True
            luffy_vel_y = -15
        
        if keys[K_SPACE] and not atacando and delay_inicio <= 0:
            atacando = True
            indice_anim_ataque = 0
            timer_anim_ataque = 0

        # 5. FÍSICA E DESENHOS FINAIS
        y_lufy, luffy_vel_y, luffy_no_ar = pulo(y_lufy, luffy_vel_y, luffy_no_ar)
        
        # Se o barril sair da tela
        if x_barril < -150:
            x_barril = largura
            pontos += 1
            barril_atual = random.choice(["simples", "triplo"])

        # Desenha o Barril e o Luffy
        if barril_atual == "simples":
            tela.blit(barril_01, (x_barril, altura_do_chao))
            barril_rect = pygame.Rect(x_barril, altura_do_chao, largura_barril, altura_barril)
        else:
            tela.blit(img_barril_triplo, (x_barril, altura_do_chao))
            barril_rect = pygame.Rect(x_barril, altura_do_chao, 150, 100)

        tela.blit(luffy_atual, (x_lufy, y_lufy))

        # --- LÓGICA DA FRUTA (REINTEGRADA) ---
        # if pontos >= proximo_alvo_fruta and not fruta_ativa:
        #     fruta_ativa = True
        #     x_fruta = largura
        #     y_fruta = random.randint(300, 480) # Altura randômica
        #     proximo_alvo_fruta += 20 # Define o próximo alvo (40, 60...)
        # V. 23
        # Só tenta criar a fruta se o barril estiver na metade esquerda da tela
        if pontos >= proximo_alvo_fruta and not fruta_ativa and x_barril < 300:
            fruta_ativa = True
            x_fruta = largura + 100 # Nasce bem na direita
            y_fruta = random.randint(300, 420) # Altura para o pulo
            proximo_alvo_fruta += 20 # Define o próximo alvo (40, 60...)

        if fruta_ativa:
            x_fruta -= 10 # Fruta é rápida!
            tela.blit(img_fruta, (x_fruta, y_fruta))
            
            # Criamos o retângulo da fruta para colisão
            rect_fruta = pygame.Rect(x_fruta, y_fruta, 40, 40)
            
            # Se o Luffy encostar na fruta
            if luffy_rect.colliderect(rect_fruta):
                frutas_coletadas += 1
                fruta_ativa = False # Coletou, ela some
                pontos += 10 # Bônus
            
            # Se a fruta sair da tela
            if x_fruta < -50:
                fruta_ativa = False

        # 6. COLISÕES
        luffy_rect = pygame.Rect(x_lufy, y_lufy, largura_personagem, altura_personagem)
        
        # Colisão do GOLPE de energia (Só se estiver no último frame do ataque)
        if atacando and indice_anim_ataque == 3:
            if rect_golpe.colliderect(barril_rect):
                exibindo_explosao = True
                timer_explosao = 15
                x_explosao, y_explosao = x_barril, y_lufy
                x_barril = largura + 100
                pontos += 5 if barril_atual == "triplo" else 3 # Pontuação por destruir barril
        
        # Colisão de DANO (Luffy encostou no barril)
        elif luffy_rect.colliderect(barril_rect):
            vidas_char -= 1
            x_barril = largura
            if vidas_char <= 0:
                status_jogo = "DIGITANDO_NOME"
                nome_temp = "" # Limpa para o novo jogador
                resetar_jogo()

        # Diz se coletou a quantidade de frutas necessarias ...
        # --- LOGICA DE VITÓRIA / TRANSIÇÃO (V.23) ---
        if frutas_coletadas >= meta_frutas and pontos >= meta_pontos:
            metas_batidas = True # Lembre de criar esta var como False no setup> ok

        if metas_batidas:
            timer_vitoria_fase -= 1 # Lembre de criar esta var como 300 no setup> ok
            
            if timer_vitoria_fase > 0:
                # O Luffy continua correndo por 5 segundos
                txt_vitoria = fonte.render("METAS ATINGIDAS! PREPARE-SE...", True, (0, 255, 0))
                tela.blit(txt_vitoria, (largura // 2 - 200, altura // 2))
            else:
                # O tempo de 5s acabou: Congela a tela e pede o ENTER
                # status_jogo = "AGUARDANDO_BOSS" # Mude para esse estado para destravar < --- V.25 < --- V.25.2
                txt_enter = fonte.render("PRESSIONE ENTER PARA O CHEFE FINAL", True, (255, 255, 255))
                tela.blit(txt_enter, (largura // 2 - 250, altura // 2 + 20))
                
                # Trava o movimento de tudo para o jogador apertar Enter com calma
                velocidade_jogo_barril = -7 
                x_wallpaper += 3 
                x_corrimao += 3

                if keys[K_RETURN]:
                    status_jogo = "BOSS_LOAD"
                    x_lufy = -100 # Prepara o Luffy para entrar na V.24

        # 7. EXPLOSÃO E UI
        if exibindo_explosao:
            tela.blit(luffy_explosao, (x_explosao, y_explosao))
            timer_explosao -= 1
            if timer_explosao <= 0: exibindo_explosao = False
            
        # códigos de pontos e corações...

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

        # EXIBE O TEMPO (V.23)
        segundos = tempo_fase // 60
        cor_relogio = (255, 255, 255)
        if segundos <= 10: cor_relogio = (255, 0, 0) # Fica vermelho se faltar pouco
        
        txt_tempo = fonte.render(f"Tempo: {segundos}s", True, cor_relogio)
        tela.blit(txt_tempo, (largura // 2 - 50, 30)) # No topo, centralizado

    # V. 24 - BOSS
    elif status_jogo == "BOSS_LOAD":
        # 1. Desenha o Cenário do Almirante
        tela.blit(wallpaper_boss, (0, 0))
        
        # 2. Entrada do Luffy (Caminhada Automática)
        if x_lufy < 150:
            x_lufy += 3
            luffy_atual = char_corrida 
        else:
            luffy_atual = char_1 # Para ao chegar
            
        # 3. Entrada do Almirante (Caminhada Automática)
        if x_boss > 550:
            x_boss -= 2
        
        # 4. Desenha os personagens
        tela.blit(luffy_atual, (x_lufy, y_lufy))
        tela.blit(img_boss, (x_boss, y_boss))
        
        # 5. Conclusão da Entrada
        if x_lufy >= 150 and x_boss <= 550:
            # Espera uns 2 segundos com o texto ants de lutar
            txt_combate = fonte.render("PREPARE-SE PARA A BATALHA!", True, (255, 0, 0))
            tela.blit(txt_combate, (largura // 2 - 180, 100))
            #V. 25
            if timer_vitoria_fase > -120: # Reutilizando o timer para economizar var
                timer_vitoria_fase -= 1
            else:
                # --- DESTRAVANDO A TRANSIÇÃO --- V 25 ajuste
                status_jogo = "BOSS_LUTA"
                timer_boss = 0
                status_boss = "MOVENDO"
                # Garante que as vidas e velocidades estão setadas
                vidas_boss = 5
                vel_boss_x, vel_boss_y = 3, 2

    # Versão 25 - Comandos e lógica BOSS "IA"
    # Versão 25/26 - Lógica da Luta Final
    elif status_jogo == "BOSS_LUTA":
        tela.blit(wallpaper_boss, (0, 0))
        timer_boss += 1
        keys = pygame.key.get_pressed()

        # 1. DEFINIR QUAL SPRITE USAR (Lógica Única)
        # Começamos com o padrão para evitar o erro de "not defined"
        img_atual_boss = img_boss 

        if status_boss == "MOVENDO":
            x_boss += vel_boss_x
            y_boss += vel_boss_y
            if x_boss <= 400 or x_boss >= largura - 100: vel_boss_x *= -1
            if y_boss <= 100 or y_boss >= altura - 250: vel_boss_y *= -1
            
            if timer_boss >= 180:
                status_boss = "PISCANDO"
                timer_boss = 0

        elif status_boss == "PISCANDO":
            # Apenas mantém o timer correndo para o efeito de piscar lá embaixo
            if timer_boss >= 60:
                status_boss = "ATACANDO"
                timer_boss = 0

        elif status_boss == "ATACANDO":
            # Troca o sprite baseado no tempo do golpe
            if timer_boss < 15:
                img_atual_boss = img_boss_ataque_1 # Punho erguido
            else:
                img_atual_boss = img_boss_ataque_2 # Energia Negra
            
            # Efeito visual no chão
            tela.blit(luffy_explosao, (x_lufy - 20, altura_do_chao - 50)) 
            
            if not luffy_no_ar and timer_boss == 1:
                vidas_char -= 1
                x_lufy -= 50 
            
            if timer_boss >= 45:
                status_boss = "MOVENDO"
                timer_boss = 0

        # 2. DESENHO DO BOSS (Regra de Ouro: Uma única linha de blit para o boss)
        # Só desenha se não estiver no frame "invisível" do piscar
        if not (status_boss == "PISCANDO" and (timer_boss % 10 < 5)):
            tela.blit(img_atual_boss, (x_boss, y_boss))

        # 3. CONTROLES DO LUFFY E SISTEMA DE ATAQUE (V.25.4)
        if keys[K_a] and x_lufy > 50: x_lufy -= 5
        if keys[K_d] and x_lufy < 450: x_lufy += 5
        if keys[K_w] and not luffy_no_ar and not atacando:
            luffy_no_ar = True
            luffy_vel_y = -15

        if keys[K_SPACE] and not atacando:
            atacando = True
            indice_anim_ataque = 0
            timer_anim_ataque = 0

        # GERENCIAMENTO DO SPRITE E FÍSICA
        y_lufy, luffy_vel_y, luffy_no_ar = pulo(y_lufy, luffy_vel_y, luffy_no_ar)

        if atacando:
            timer_anim_ataque += 1
            if timer_anim_ataque >= VELOCIDADE_ANIMACAO:
                timer_anim_ataque = 0
                indice_anim_ataque += 1
            
            if indice_anim_ataque < len(animacao_ataque):
                luffy_sprite_final = animacao_ataque[indice_anim_ataque]
                # Desenha a ENERGIA no frame de impacto (igual aos barris)
                if indice_anim_ataque == 3:
                    tela.blit(luffy_energia, (x_lufy + 100, y_lufy + 20))
                    # Colisão com o Boss
                    rect_golpe = pygame.Rect(x_lufy + 100, y_lufy + 20, 150, 60)
                    rect_boss = pygame.Rect(x_boss, y_boss, 80, 120)
                    if rect_golpe.colliderect(rect_boss):
                        vidas_boss -= 1
                        exibindo_explosao = True
                        timer_explosao = 15
                        x_explosao, y_explosao = x_boss, y_boss
                        x_boss += 30 # Empurra o chefe
                        atacando = False 
            else:
                atacando = False
        else:
            # Sprite Normal ou Pulo
            luffy_sprite_final = char_1 if not luffy_no_ar else char_corrida

        # DESENHO FINAL DO LUFFY
        tela.blit(luffy_sprite_final, (x_lufy, y_lufy))

        # 4. HUD E FINALIZAÇÃO (V.27)
        # Corações do Luffy (Esquerda)
        for i in range(vidas_char):
            tela.blit(img_coracao, (30 + (i * 35), 30))
        
        # Corações do Boss (Direita) - Substitui o texto BOSS HP
        for i in range(vidas_boss):
            tela.blit(img_coracao, (740 - (i * 35), 30))

        # Desenho do Boss (Ajustado para ficar abaixo do HUD)
        if not (status_boss == "PISCANDO" and (timer_boss % 10 < 5)):
            tela.blit(img_atual_boss, (x_boss, y_boss))

        # --- CONDIÇÕES DE FIM DE JOGO ---
        if vidas_boss <= 0:
            pontos += 500 # Bônus por derrotar o Almirante
            status_jogo = "VITORIA_FINAL"
            timer_vitoria_fase = 240 # Tempo da cena final

        if vidas_char <= 0:
            status_jogo = "DIGITANDO_NOME"
            resetar_jogo()

    # --- NOVO ESTADO: TELA DE VITÓRIA (V.29) ---
    elif status_jogo == "VITORIA_FINAL":
        tela.blit(wallpaper_boss, (0, 0))
        
        # Efeito de escurecer a tela
        overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        tela.blit(overlay, (0,0))
        
        msg1 = fonte.render("O ALMIRANTE FOI DERROTADO!", True, (255, 215, 0))
        msg2 = fonte.render("VOCÊ É O REI DOS PIRATAS!", True, (255, 255, 255))
        msg3 = fonte.render("PRESSIONE ENTER PARA SALVAR SEU RECORDE", True, (200, 200, 200))
        
        tela.blit(msg1, (largura//2 - 200, altura//2 - 60))
        tela.blit(msg2, (largura//2 - 180, altura//2))
        
        if timer_vitoria_fase <= 0:
            tela.blit(msg3, (largura//2 - 280, altura//2 + 100))
            keys = pygame.key.get_pressed()
            if keys[K_RETURN]:
                status_jogo = "DIGITANDO_NOME"
        else:
            timer_vitoria_fase -= 1

    pygame.display.update() # atualiza a tela do jogo
    controle_frame.tick(60) # limita a taxa de atualização da tela para 60 frames por segundo