# Bibliotecas
import pygame
import random

# INICIALIZAÇÃO
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/snd/musica_fundo.mp3")
pygame.mixer.music.play(-1)  # loop infinito
clock = pygame.time.Clock()

# Dados gerais do jogo
WIDTH = 1710
HEIGHT = 900
FPS = 60

timer_velocidade = 0
velocidade_max = -35 
velocidade_mundo = -4

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run of the Undead")
font = pygame.font.SysFont(None, 40)

game = True

branco  = (255,255,255)
preto   = (0,0,0)
verde   = (0,200,0)
vermelho= (255,0,0)
amarelo = (255,255,0)
azul    = (100,149,237)
cinza   = (80,80,80)

# tamanhos de cada uma das plataformas
altura  = 400
largura = 800

# ── Carrega imagens ──────────────────────────────────────────────────────────
inicio_img = pygame.image.load("assets/img/capa.png").convert()
inicio_img = pygame.transform.scale(inicio_img, (WIDTH, HEIGHT))

background = pygame.image.load("assets/img/prediosfogo.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

rua_img   = pygame.image.load("assets/img/estrada.png").convert_alpha()
rua_img   = pygame.transform.scale(rua_img, (largura, altura))

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

mao_img   = pygame.image.load("assets/img/mao.png").convert_alpha()
mao_img   = pygame.transform.scale(mao_img, (200, 200))

moeda_img = pygame.image.load("assets/img/moeda.png").convert_alpha()
moeda_img = pygame.transform.scale(moeda_img, (70, 70))

# ── Imagens dos veículos (nome, numero, largura, altura) ─────────────────────
VEICULOS_INFO = [
    ("carro",        4,  160, 100),
    ("patinete",     2,   90, 110),
    ("golfe",        3,  160, 100),
    ("escavadeira",  7,  220, 130),
    ("aviao",       16,  300, 120),
    ("submarino",   10,  220, 120),
    ("tanque",      12,  240, 120),
    ("jetsky",       2,  180, 110),
    ("rover",        5,  200, 120),
]

veiculos_imgs = {}
for nome, num, larg, alt in VEICULOS_INFO:
    try:
        img = pygame.image.load(f"assets/img/{nome}.png").convert_alpha()
        img = pygame.transform.scale(img, (larg, alt))
        veiculos_imgs[nome] = (img, num)
    except:
        print(f"Aviso: assets/img/{nome}.png não encontrado")

# ── Hitboxes das plataformas ─────────────────────────────────────────────────
HITBOX_OFFSETS = {
    id(rua_img):   (5,   220, 20),
    id(plat1_img): (5,   220, 580),
    id(plat2_img): (270, 220, 540),
    id(plat3_img): (580, 220, 585),
}

PLAT = [rua_img, plat1_img, plat2_img, plat3_img]
chao = HEIGHT - 400

tempo_pulo_max = 15
VEL_PULO  = -20
GRAVIDADE = 1

def calcular_tempo_no_ar():
    y, vy, tp, pulando, frames = 0, 0, tempo_pulo_max, True, 0
    while True:
        frames += 1
        if pulando and tp > 0:
            vy = VEL_PULO; tp -= 1
        vy += GRAVIDADE; y += vy
        if tp == 0: pulando = False
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
    else:
        base_min, base_max = 150, 190
    bonus = max(0, (velocidade - 4) * 9)
    return random.randint(base_min + bonus, base_max + bonus)

coins        = 0
zombie_count = 1

# ── Tela de início ───────────────────────────────────────────────────────────
inicio_jogo = True
largura_botao = 200
botao_altura  = 60
centraliza_x_botao = WIDTH//2 - largura_botao//2
y_botao   = HEIGHT//2 + 50
botao_rect = pygame.Rect(centraliza_x_botao, y_botao, largura_botao, botao_altura)

while inicio_jogo:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            inicio_jogo = False

    window.blit(inicio_img, (0, 0))
    pygame.draw.rect(window, branco, botao_rect)
    pygame.draw.rect(window, preto,  botao_rect, 3)
    fonte_botao  = pygame.font.SysFont(None, 60)
    texto_botao  = fonte_botao.render("Jogar", True, preto)
    texto_centro = texto_botao.get_rect(center=botao_rect.center)
    window.blit(texto_botao, texto_centro)
    pygame.display.update()


# ═══════════════════════════════════════════════════════════════
#  CLASSE PLATAFORMA
# ═══════════════════════════════════════════════════════════════
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem if imagem is not None else random.choice(PLAT)
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        margem_esq, offset_y, corte = HITBOX_OFFSETS[id(self.image)]
        self.hitbox = pygame.Rect(x + margem_esq, y + offset_y,
                                  self.rect.width - corte, 50)

    def update(self):
        self.rect.x   += velocidade_mundo
        self.hitbox.x += velocidade_mundo
        if self.rect.right < 0:
            self.kill()


def criar_proxima_plataforma(plat_anterior):
    imagem = random.choices(PLAT, weights=[5, 1, 1, 1], k=1)[0]
    margem_esq, offset_y, corte = HITBOX_OFFSETS[id(imagem)]
    gap = calcular_gap_seguro(plat_anterior)
    x   = plat_anterior.hitbox.right + gap - margem_esq
    return Plataforma(x, chao, imagem)


# ═══════════════════════════════════════════════════════════════
#  CLASSE VEÍCULO
# ═══════════════════════════════════════════════════════════════
class Veiculo(pygame.sprite.Sprite):
    def __init__(self, plataforma, nome, img, numero):
        pygame.sprite.Sprite.__init__(self)
        self.image  = img
        self.numero = numero
        self.plat   = plataforma
        self.nome   = nome

        self.rect = self.image.get_rect()
        self.rect.bottom = plataforma.hitbox.top
        self.rect.left   = plataforma.hitbox.right

        self.vel   = random.randint(3, 6)
        self._font = pygame.font.SysFont("Arial Black", 22, bold=True)

    def update(self, plataformas):
        self.rect.x += velocidade_mundo - self.vel

        if not self.plat.alive():
            self.kill()
            return

        self.rect.bottom = self.plat.hitbox.top

        if self.rect.right <= self.plat.hitbox.left:
            self.kill()

    def draw_badge(self, surface):
        txt      = self._font.render(str(self.numero), True, (20, 20, 20))
        tw, th   = txt.get_size()
        pad      = 6
        bw, bh   = tw + pad*2, th + pad*2
        cx       = self.rect.centerx
        cy       = self.rect.top - bh//2 - 4

        sh = pygame.Surface((bw+2, bh+2), pygame.SRCALPHA)
        pygame.draw.rect(sh, (0,0,0,100), sh.get_rect(), border_radius=8)
        surface.blit(sh, (cx - bw//2 - 1, cy - bh//2 + 2))

        badge = pygame.Surface((bw, bh), pygame.SRCALPHA)
        pygame.draw.rect(badge, (255,210,0,230), badge.get_rect(), border_radius=8)
        pygame.draw.rect(badge, (0,0,0,180),     badge.get_rect(), 2, border_radius=8)
        badge.blit(txt, (pad, pad))
        surface.blit(badge, (cx - bw//2, cy - bh//2))


# ═══════════════════════════════════════════════════════════════
#  CLASSE JOGADOR
# ═══════════════════════════════════════════════════════════════
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = zombie_img
        self.rect  = self.image.get_rect()

        self.pulando        = False
        self.tempo_pulo     = 0
        self.tempo_pulo_max = 15

        self.rect.x      = 150
        self.rect.bottom = 720

        self.velocidade_y = 0
        self.chao = True

    def update(self, plataformas):
        if self.pulando and self.tempo_pulo > 0:
            self.velocidade_y = -20
            self.tempo_pulo  -= 1

        self.velocidade_y += 1
        self.rect.y       += self.velocidade_y

        self.chao = False
        for plat in plataformas:
            if self.rect.colliderect(plat.hitbox):
                if self.velocidade_y > 0:
                    self.rect.bottom = plat.hitbox.top
                    self.velocidade_y = 0
                    self.chao = True

        if self.rect.top > HEIGHT:
            return True
        return False

    def pular(self):
        if self.chao:
            self.pulando    = True
            self.tempo_pulo = self.tempo_pulo_max
            self.chao       = False

    def soltar_pulo(self):
        self.pulando    = False
        self.tempo_pulo = 0


# ═══════════════════════════════════════════════════════════════
#  FUNÇÃO DE SPAWN DE VEÍCULO
# ═══════════════════════════════════════════════════════════════
def spawnar_veiculo(plataformas):
    plats_validas = [
        p for p in plataformas
        if p.image is rua_img
        and p.hitbox.right > WIDTH//2
        and p.hitbox.left  < WIDTH
        and p.hitbox.width > 200
    ]
    if not plats_validas or not veiculos_imgs:
        return None

    plat_escolhida = random.choice(plats_validas)
    nome = random.choice(list(veiculos_imgs.keys()))
    img, numero = veiculos_imgs[nome]

    if img.get_width() >= plat_escolhida.hitbox.width:
        return None

    return Veiculo(plat_escolhida, nome, img, numero)


# ═══════════════════════════════════════════════════════════════
#  SETUP INICIAL
# ═══════════════════════════════════════════════════════════════
player        = Jogador()
todos_sprites = pygame.sprite.Group()
plataformas   = pygame.sprite.Group()
veiculos      = pygame.sprite.Group()
todos_sprites.add(player)

# Plataforma inicial forçada
plat_inicial = Plataforma(0, chao, rua_img)
plat_inicial.hitbox = pygame.Rect(0, chao + 220, largura, 50)
todos_sprites.add(plat_inicial)
plataformas.add(plat_inicial)

ultima_plat = plat_inicial
x_final     = plat_inicial.hitbox.right
while x_final < WIDTH + 200:
    plat = criar_proxima_plataforma(ultima_plat)
    todos_sprites.add(plat)
    plataformas.add(plat)
    ultima_plat = plat
    x_final     = plat.hitbox.right

# Timers de veículos
timer_jogo      = 0
DELAY_VEICULOS  = 5 * FPS
timer_spawn_vei = 0
INTERVALO_SPAWN = 4 * FPS


# ═══════════════════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ═══════════════════════════════════════════════════════════════
while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.pular()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.soltar_pulo()

    # ── Timers ───────────────────────────────────────────────────────────────
    timer_jogo += 1

    # ── Spawn de veículos após 5s ─────────────────────────────────────────────
    if timer_jogo > DELAY_VEICULOS:
        timer_spawn_vei += 1
        if timer_spawn_vei >= INTERVALO_SPAWN:
            timer_spawn_vei = 0
            novo_vei = spawnar_veiculo(plataformas)
            if novo_vei:
                veiculos.add(novo_vei)

    # ── Move background e placas ──────────────────────────────────────────────
    background_rect.x += velocidade_mundo
    if background_rect.right < 0:
        background_rect.x = 0

    placas_rect.x += velocidade_mundo
    if placas_rect.right < 0:
        placas_rect.x = 0

    # ── Velocidade crescente a cada 10s ───────────────────────────────────────
    timer_velocidade += 1
    if timer_velocidade >= 600:
        timer_velocidade = 0
        if velocidade_mundo > velocidade_max:
            velocidade_mundo -= 1

    # ── Atualiza ──────────────────────────────────────────────────────────────
    game_over = player.update(plataformas)
    if game_over:
        pygame.mixer.music.stop()
        game = False

    plataformas.update()
    veiculos.update(plataformas)

    # ── Gera novas plataformas à direita ──────────────────────────────────────
    plats_visiveis = [p for p in plataformas if p.rect.right > 0]
    while not plats_visiveis or max(p.rect.right for p in plats_visiveis) < WIDTH:
        ultima_plat = max(plats_visiveis, key=lambda p: p.hitbox.right) \
                      if plats_visiveis else None
        if ultima_plat:
            nova_plat = criar_proxima_plataforma(ultima_plat)
        else:
            nova_plat = Plataforma(WIDTH, chao, random.choice(PLAT))
        todos_sprites.add(nova_plat)
        plataformas.add(nova_plat)
        plats_visiveis = [p for p in plataformas if p.rect.right > 0]

    # ── Desenha ───────────────────────────────────────────────────────────────
    window.fill(preto)

    window.blit(background, background_rect)
    background_rect2   = background_rect.copy()
    background_rect2.x += background_rect2.width
    window.blit(background, background_rect2)

    window.blit(placas_img, placas_rect)
    placas_rect2   = placas_rect.copy()
    placas_rect2.x += placas_rect2.width
    window.blit(placas_img, placas_rect2)

    plataformas.draw(window)

    # Veículos + badge do número
    for v in veiculos:
        window.blit(v.image, v.rect)
        v.draw_badge(window)

    # Jogador
    window.blit(player.image, player.rect)

    # HUD
    window.blit(mao_img, (10, 10))
    qnt_zombie = font.render(str(zombie_count), True, branco)
    window.blit(qnt_zombie, (170, 100))
    window.blit(moeda_img, (75, 180))
    qnt_moedas = font.render(str(coins), True, branco)
    window.blit(qnt_moedas, (170, 200))

    # ── DEBUG (descomenta para ver hitboxes) ──────────────────────────────────
    # for plat in plataformas:
    #     cor = vermelho if plat.image is rua_img else \
    #           verde    if plat.image is plat1_img else \
    #           azul     if plat.image is plat2_img else amarelo
    #     pygame.draw.rect(window, cor, plat.hitbox, 2)
    # for v in veiculos:
    #     pygame.draw.rect(window, branco, v.rect, 2)

    pygame.display.update()

pygame.quit()
