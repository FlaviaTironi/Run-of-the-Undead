import pygame
import random

# INICIALIZAÇÃO
clock = pygame.time.Clock() # velocidade do jogo

pygame.init()

WIDTH = 600
HEIGHT = 400

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run of the Undead")

# ----- Inicia estruturas de dados

game = True

branco = (255,255,255)
preto = (0,0,0)
verde = (0,200,0)
vermelho = (255,0,0)
amarelo = (255,255,0)
azul = (100,149,237)
cinza = (80,80,80)

# Gerar tela de início
inicio_jogo = True
timer_inicio = 180

while inicio_jogo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    inicio = pygame.image.load("assets/img/inicio.png").convert()

    window.fill (preto)
    window.blit(inicio, (0, 0)) 
    fonte_titulo = pygame.font.SysFont(None, 100) # carrega uma nova fonte de texto (none = padrão; 48 = tamanho fonte)
    titulo = fonte_titulo.render ("Run of the Undead", True, branco) # cria uma imagem a partir da fonte criada na linha anterior
    titulo_centro = titulo.get_rect(center = (WIDTH//2, HEIGHT//2)) # o centro da caixa de texto fica no centro da tela
    window.blit(titulo, titulo_centro) #desenha em window a imagem titulo na posicao titulo_centro

# Contabiliza o tempo da tela de início
    pygame.display.update()
    clock.tick (60)
    timer_inicio -= 1
    if timer_inicio <= 0:
        inicio_jogo = False

# =====================================

score = 0
coins = 0
zombie_count = 1

font = pygame.font.SysFont(None, 40)

background = pygame.image.load("assets/img/cidade.png").convert()
zombie_img = pygame.image.load("assets/img/zombie.png").convert_alpha()

# ===== Loop principal =====
FPS = 60
while game:
    clock.tick (FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (0, 0)) 
    
    pygame.display.update()  # Mostra o novo frame para o jogador