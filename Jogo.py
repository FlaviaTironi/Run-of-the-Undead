# Bibliotecas
import pygame
import random

# INICIALIZAÇÃO
pygame.init()
pygame.mixer.init()                                    # ADICIONA
pygame.mixer.music.load("assets/snd/musica_fundo.mp3")           # ADICIONA
pygame.mixer.music.play(-1)                            # ADICIONA (loop infinito)
clock = pygame.time.Clock()
clock = pygame.time.Clock() #relógio para controlar a velocidade do jogo

# Dados gerais do jogo
WIDTH = 1710
HEIGHT = 900
FPS = 60

# Aumentando a velocidade do mapa conforme o tempo
timer_velocidade = 0
velocidade_max = -35 
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

# tamanhos de cada uma das platadormas
altura = 400
largura = 800

# Carrega imagens
inicio_img = pygame.image.load("assets/img/capa.png").convert()
inicio_img = pygame.transform.scale(inicio_img, (WIDTH, HEIGHT))

background = pygame.image.load("assets/img/prediosfogo.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

rua_img = pygame.image.load("assets/img/estrada.png").convert_alpha()
rua_img = pygame.transform.scale(rua_img, (largura, altura))

plat1_img = pygame.image.load("assets/img/plat5.png").convert_alpha()
plat1_img = pygame.transform.scale(plat1_img, (largura, altura))

plat2_img = pygame.image.load("assets/img/plat6.png").convert_alpha()
plat2_img = pygame.transform.scale(plat2_img, (largura, altura))

plat3_img = pygame.image.load("assets/img/plat7.png").convert_alpha()
plat3_img = pygame.transform.scale(plat3_img, (largura, altura))

placas_img = pygame.image.load("assets/img/placas.png").convert_alpha()
placas_img = pygame.transform.scale(placas_img, (WIDTH-100, HEIGHT-100))
placas_rect = placas_img.get_rect()
placas_rect.x = 0
placas_rect.y = 130

zombie_img = pygame.image.load("assets/img/zombie.png").convert_alpha()
zombie_img = pygame.transform.scale(zombie_img, (80, 100))

mao_img = pygame.image.load("assets/img/mao.png").convert_alpha()
mao_img = pygame.transform.scale(mao_img, (200,200))

moeda_img = pygame.image.load("assets/img/moeda.png").convert_alpha()
moeda_img = pygame.transform.scale(moeda_img, (70,70))

plat3_img = pygame.transform.scale(plat3_img, (largura, altura))

# Define hitbox específico para cada imagem
HITBOX_OFFSETS = {id(rua_img): (5, 220, 20),id(plat1_img): (5 , 220, 580),id(plat2_img): (270, 220, 540),id(plat3_img): (580, 220, 585),}

#Criando conjuntos de possíveis plataformas + posição plataforma (500)
PLAT = [rua_img,plat1_img,plat2_img,plat3_img]
chao = HEIGHT -400

tempo_pulo_max = 15
VEL_PULO = -20
GRAVIDADE = 1

def calcular_tempo_no_ar():
    y = 0
    vy = 0
    tempo_pulo = tempo_pulo_max
    pulando = True
    frames = 0

    while True:
        frames += 1

        if pulando and tempo_pulo > 0:
            vy = VEL_PULO
            tempo_pulo -= 1

        vy += GRAVIDADE
        y += vy

        if tempo_pulo == 0:
            pulando = False

        if y >= 0 and frames > 1:
            return frames

TEMPO_NO_AR_MAX = calcular_tempo_no_ar()


def calcular_gap_seguro(plat_anterior):
    velocidade = abs(velocidade_mundo)

    if plat_anterior.image is plat3_img:
        base_min, base_max = 160, 200
    elif plat_anterior.image is plat2_img:
        base_min, base_max = 130, 170
    elif plat_anterior.image is plat1_img:
        base_min, base_max = 140, 170
    else:  # rua_img
            base_min, base_max = 160, 190
        

    # aumenta o gap conforme a velocidade do jogo aumenta
    bonus = max(0, (velocidade - 4) * 12)

    gap_min = base_min + bonus
    gap_max = base_max + bonus

    return random.randint(gap_min, gap_max)

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

#===== Classe plataformas =====
class Plataforma (pygame.sprite.Sprite):
    def __init__(self, x, y, imagem=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem if imagem is not None else random.choice(PLAT) # sortear aleatoriamente uma das 4 plataformas
        self.rect = self.image.get_rect() # cria um retângulo de plataforma (colisão)
        self.rect.x = x #posição x da plataforma
        self.rect.y = y #posição y da plataforma

        margem_esq, offset_y, corte = HITBOX_OFFSETS[id(self.image)]
        self.hitbox = pygame.Rect(x + margem_esq, y + offset_y, self.rect.width - corte, 50)

            
    def update (self):
        self.rect.x += velocidade_mundo #mover a plataforma para a esquerda
        self.hitbox.x += velocidade_mundo
        if self.rect.right < 0: # se a imagem sair da tela, a remove
            self.kill()

def criar_proxima_plataforma(plat_anterior):
    imagem = random.choices(PLAT, weights=[5, 1, 1, 1], k=1)[0]
    margem_esq, offset_y, corte = HITBOX_OFFSETS[id(imagem)]


    # Rua juntas
    if plat_anterior.image is rua_img and imagem is rua_img:
        # juntar ruas grandes
        if random.random() < 0.80:
            x = plat_anterior.rect.right
        else:
            # deixar buracos ruas grandes 
            gap = random.randint(20, 80)
            x = plat_anterior.rect.right + gap

    else:
        # demais casos continuam com gap controlado
        gap = calcular_gap_seguro(plat_anterior)
        x = plat_anterior.hitbox.right + gap - margem_esq

    return Plataforma(x, chao, imagem)

#===== Classe jogador =====
class Jogador (pygame.sprite.Sprite):
    def __init__(self):
    # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        #imagem Jogador/zombie
        self.image = zombie_img
        self.rect = self.image.get_rect()

        self.pulando = False # botão espaço sendo segurado
        self.tempo_pulo = 0 # frames restantes do pulo
        self.tempo_pulo_max = 15  # frames máximos segurando o espaço

        # Posição inicial
        self.rect.x = 150 #posiciona o jogador x =150
        self.rect.bottom = 720 # ficar em cima do chão

        # Pulo
        self.velocidade_y = 0 
        self.chao = True #permitir pular

    def update(self,plataformas):
        # Pulo longo baseado no tempo segurando
        if self.pulando and self.tempo_pulo > 0: # enquanto o espaço está sendo segurado e ainda tem tempo de pulo, manter a velicodade subindo
            self.velocidade_y = -20
            self.tempo_pulo -= 1

        # Gravidade
        self.velocidade_y += 1 
        self.rect.y += self.velocidade_y # aplicar a gravidade - mover verticalmente jogador
        
        # Colisão com plataformas
        self.chao = False
        for plat in plataformas:
            if self.rect.colliderect(plat.hitbox):
                if self.velocidade_y > 0:
                    self.rect.bottom = plat.hitbox.top
                    self.velocidade_y = 0
                    self.chao = True

        # Morreu ao cair no buraco
        if self.rect.top > HEIGHT:
            return True  # game over

        return False
        
    def pular(self):  # chamado quando APERTA o espaço
        if self.chao: # só pula se estiver no chão
            self.pulando = True
            self.tempo_pulo = self.tempo_pulo_max
            self.chao = False 

    def soltar_pulo(self):  # chamado quando SOLTA o espaço
        self.pulando = False # desativar o pulo
        self.tempo_pulo = 0

# Criar jogador + grupo sprites
player = Jogador()
todos_sprites = pygame.sprite.Group()
plataformas = pygame.sprite.Group()
todos_sprites.add(player)

# Criação plataformas iniciais

# Força plataforma longa no início
plat_inicial = Plataforma(0, chao)
plat_inicial.image = rua_img
plat_inicial.rect = plat_inicial.image.get_rect()
plat_inicial.rect.x = 0
plat_inicial.rect.y = chao
plat_inicial.hitbox = pygame.Rect(0, chao + 220, largura, 50)
todos_sprites.add(plat_inicial)
plataformas.add(plat_inicial)

ultima_plat = plat_inicial
x_final = plat_inicial.hitbox.right

while x_final < WIDTH + 200:
    plat = criar_proxima_plataforma(ultima_plat)
    todos_sprites.add(plat)
    plataformas.add(plat)
    ultima_plat = plat
    x_final = plat.hitbox.right

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.pular()

        if event.type == pygame.KEYUP:  # quando SOLTA a tecla
            if event.key == pygame.K_SPACE:
                player.soltar_pulo()

    # Move o background
    background_rect.x += velocidade_mundo
    if background_rect.right < 0: # se sair da tela, volta para o início
        background_rect.x = 0

    #Move as placasa igual ao background
    placas_rect.x += velocidade_mundo 
    if placas_rect.right < 0:
        placas_rect.x = 0 
    
    #Aumentando a velocidade do mapa a cada 10 segundos (10*60 = 600 frames)
    timer_velocidade +=1
    if timer_velocidade >=600:
        timer_velocidade = 0
        if timer_velocidade> velocidade_max:
            velocidade_mundo -= 1

    # Atualiza jogador e plataformas
    game_over = player.update(plataformas)
    if game_over:
        pygame.mixer.music.load("assets/snd/musica_fundo.mp3")
        game = False
    plataformas.update()

    # Desenha o fundo duas vezes
    window.fill(preto)
    window.blit(background, background_rect)
    background_rect2 = background_rect.copy()
    background_rect2.x += background_rect2.width
    window.blit(background, background_rect2)

# Gera novas plataformas pela direita
    plats_visiveis = [p for p in plataformas if p.rect.right > 0]
    while not plats_visiveis or max(p.rect.right for p in plats_visiveis) < WIDTH:
        ultima_plat = max(plats_visiveis, key=lambda p: p.hitbox.right) if plats_visiveis else None
        if ultima_plat:
            nova_plat = criar_proxima_plataforma(ultima_plat)
        else:
            nova_plat = Plataforma(WIDTH, chao, random.choice(PLAT))
        todos_sprites.add(nova_plat)
        plataformas.add(nova_plat)
        plats_visiveis = [p for p in plataformas if p.rect.right > 0]

# Desenha as placas se movendo
    window.blit(placas_img, placas_rect)
    placas_rect2 = placas_rect.copy()
    placas_rect2.x += placas_rect2.width
    window.blit(placas_img, placas_rect2)

    # 4. Plataformas 
    plataformas.draw(window)

    # 5. Jogador 
    window.blit(player.image, player.rect)

    # 5. Jogador 
    window.blit(player.image, player.rect)

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