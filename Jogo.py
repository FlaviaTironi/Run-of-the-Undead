# Bibliotecas
import pygame
import random

# INICIALIZAÇÃO
pygame.init()
clock = pygame.time.Clock() #relógio para controlar a velocidade do jogo

# Dados gerais do jogo
WIDTH = 1710
HEIGHT = 900
FPS = 60

# Aumentando a velocidade do mapa conforme o tempo
timer_velocidade = 0
velocidade_max = -50
velocidade_mundo = -4

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run of the Undead")
font = pygame.font.SysFont(None, 40) # escrever textos na tela

game = True

branco = (255,255,255)
preto = (0,0,0)
verde = (0,200,0)
vermelho = (255,0,0)
amarelo = (255,255,0)
azul = (100,149,237)
cinza = (80,80,80)

# Carrega imagens
inicio_img = pygame.image.load("assets/img/capa.png").convert()
inicio_img = pygame.transform.scale(inicio_img, (WIDTH, HEIGHT))

background = pygame.image.load("assets/img/prediosfogo.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

rua_img = pygame.image.load("assets/img/estrada.png").convert_alpha()
rua_img = pygame.transform.scale(rua_img, (WIDTH, HEIGHT))
rua_rect = rua_img.get_rect()

placas_img = pygame.image.load("assets/img/placas.png").convert_alpha()
placas_img = pygame.transform.scale(placas_img, (WIDTH-100, HEIGHT-100))
placas_rect = placas_img.get_rect()

zombie_img = pygame.image.load("assets/img/zombie.png").convert_alpha()
zombie_img = pygame.transform.scale(zombie_img, (80, 100))


mao_img = pygame.image.load("assets/img/mao.png").convert_alpha()
mao_img = pygame.transform.scale(mao_img, (200,200))

moeda_img = pygame.image.load("assets/img/moeda.png").convert_alpha()
moeda_img = pygame.transform.scale(moeda_img, (70,70))

# Conteúdo quantidade
coins = 0
zombie_count = 1

# ===== Tela de início =====
inicio_jogo = True

# Botão "Jogar"
largura_botao = 200
botao_altura = 60
centraliza_x_botao = WIDTH//2 - largura_botao//2
y_botao = HEIGHT //2 +50 #deixar um pouco mais para baixo do centro
botao_rect = pygame.Rect (centraliza_x_botao,y_botao,largura_botao, botao_altura)

while inicio_jogo:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:  # CLICAR COM O MOUSE
            inicio_jogo = False

    window.blit(inicio_img, (0, 0))

# # Título
#     fonte_titulo = pygame.font.SysFont(None, 100)
#     titulo = fonte_titulo.render("Run of the Undead", True, branco)
#     titulo_centro = titulo.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
#     window.blit(titulo, titulo_centro)

# Desenha a caixa branca do botão
    pygame.draw.rect(window, branco, botao_rect)

# Desenha a borda do botão
    pygame.draw.rect(window, preto, botao_rect, 3)

    # Texto "jogar"
    fonte_botao = pygame.font.SysFont(None, 60)
    texto_botao= fonte_botao.render("Jogar", True, preto)
    texto_centro = texto_botao.get_rect(center=botao_rect.center)
    window.blit(texto_botao, texto_centro)

    pygame.display.update()

#===== Classe jogador =====
class Jogador (pygame.sprite.Sprite):
    def __init__(self):
    # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

#imagem Jogador/zombie
        self.image = zombie_img
        self.rect = self.image.get_rect()

        # Posição inicial
        self.rect.x = 150
        self.rect.bottom = HEIGHT - 125 # ficar em cima do chão

        # Pulo
        self.velocidade_y = 0
        self.chao = True

    def update(self):
        # Gravidade
        self.velocidade_y += 1
        self.rect.y += self.velocidade_y
        
        # Chão
        if self.rect.bottom >= HEIGHT-125:
            self.rect.bottom = HEIGHT - 125
            self.velocidade_y = 0
            self.chao = True
        
    def pular (self):
        if self.chao:
            self.velocidade_y = -20
            self.chao = False

# Criar jogador + grupo sprites
player = Jogador()
todos_sprites = pygame.sprite.Group()
todos_sprites.add(player)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.pular()

    # Move o background
    background_rect.x += velocidade_mundo
    if background_rect.right < 0:
        background_rect.x = 0
    
    #Aumentando a velocidade do mapa a cada 10 segundos (10*60 = 600 frames)
    timer_velocidade +=1
    if timer_velocidade >=600:
        timer_velocidade = 0
        if timer_velocidade> velocidade_max:
            velocidade_mundo -= 1

    # Atualizando sprites
    todos_sprites.update()

    # Desenha o fundo duas vezes
    window.fill(preto)
    window.blit(background, background_rect)
    background_rect2 = background_rect.copy()
    background_rect2.x += background_rect2.width
    window.blit(background, background_rect2)

    # Desenha a rua
    window.blit(rua_img, (0, 200))
    # Desenha a rua
    window.blit(placas_img, (0, 130))

    # Desenha sprites
    todos_sprites.draw(window)

    # Desenha a mão da quantidade de zombies
    window.blit(mao_img, (10,10))
    # Texto quantidade moedas
    qnt_zombie = font.render(str(zombie_count), True, branco)
    window.blit(qnt_zombie, (170,100))

    # Desenho da moeda
    window.blit(moeda_img, (75,180))
    # Texto quantidade moedas
    qnt_moedas = font.render(str(coins), True, branco)
    window.blit(qnt_moedas, (170,200))

    pygame.display.update()

pygame.quit()