# Bibliotecas
import pygame
import random

# Inicialização e música de fundo
pygame.init()
pygame.mixer.init()                                    
pygame.mixer.music.load("assets/snd/musica_fundo.mp3") 
pygame.mixer.music.play(-1)
som_explosao = pygame.mixer.Sound("assets/snd/Somexplosão.mp3")
# pygame.mixer.init()                                    # ADICIONA
# pygame.mixer.music.load("assets/snd/musica_fundo.mp3")
# pygame.mixer.music.load("assets/snd/audiodegrito.mp3")             # ADICIONA
# pygame.mixer.music.play(-1)   
clock = pygame.time.Clock()

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

branco  = (255,255,255)
preto   = (0,0,0)
verde   = (0,200,0)
vermelho= (255,0,0)
amarelo = (255,255,0)
azul    = (100,149,237)
cinza   = (80,80,80)

# tamanhos de cada uma das platadormas
altura  = 400
largura = 800

#  Carrega imagens 
inicio_img = pygame.image.load("assets/img/capa.png").convert()
inicio_img = pygame.transform.scale(inicio_img, (WIDTH, HEIGHT))

background = pygame.image.load("assets/img/prediosfogo.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

gameover_img = pygame.image.load("assets/img/game_over.png").convert_alpha()
gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

rua_img = pygame.image.load("assets/img/estrada.png").convert_alpha()
rua_img = pygame.transform.scale(rua_img, (largura, altura))

rua_esq_img = pygame.image.load("assets/img/estrada3.png").convert_alpha()
rua_esq_img = pygame.transform.scale(rua_esq_img, (largura, altura))

rua_meio_img = pygame.image.load("assets/img/estrada2.png").convert_alpha()
rua_meio_img = pygame.transform.scale(rua_meio_img, (largura, altura))

rua_dir_img = pygame.image.load("assets/img/estrada4.png").convert_alpha()
rua_dir_img = pygame.transform.scale(rua_dir_img, (largura, altura))

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

mao_img = pygame.image.load("assets/img/cerebro.png").convert_alpha()
mao_img = pygame.transform.scale(mao_img, (90, 90))

moeda_img = pygame.image.load("assets/img/moeda.png").convert_alpha()
moeda_img = pygame.transform.scale(moeda_img, (70, 70))

moeda_coletada = pygame.image.load("assets/img/moeda.png").convert_alpha()
moeda_coletada = pygame.transform.scale(moeda_coletada, (40, 40))

plat3_img = pygame.transform.scale(plat3_img, (largura, altura))

# ── Imagens das bombas ───────────────────────────────────────────────────────
bomba_imgs = {
    "atomica":    (pygame.transform.scale(pygame.image.load("assets/img/atomica.png").convert_alpha(),    (100, 100)), 10),
    "barril":     (pygame.transform.scale(pygame.image.load("assets/img/barril.png").convert_alpha(),     (100, 100)), 10),
    "bomba":      (pygame.transform.scale(pygame.image.load("assets/img/bomba.png").convert_alpha(),      (100, 100)), 4),
    "explosivo2": (pygame.transform.scale(pygame.image.load("assets/img/explosivo2.png").convert_alpha(), (100, 100)), 1),
    "explosivos": (pygame.transform.scale(pygame.image.load("assets/img/explosivos.png").convert_alpha(), (100, 100)), 2),
    "foguete":    (pygame.transform.scale(pygame.image.load("assets/img/foguete.png").convert_alpha(),    (100, 100)), 12),
    "fronte":     (pygame.transform.scale(pygame.image.load("assets/img/fronte.png").convert_alpha(),     (100, 100)), 2),
    "granada":    (pygame.transform.scale(pygame.image.load("assets/img/granada.png").convert_alpha(),    (100, 100)), 3),
    "toxico":     (pygame.transform.scale(pygame.image.load("assets/img/toxico.png").convert_alpha(),     (100, 100)), 16),
}

# ── Imagens dos veículos ─────────────────────────────────────────────────────
VEICULOS_INFO = [
    ("carro",        4,  240, 150),
    ("patinete",     2,  140, 165),
    ("golfe",        3,  240, 150),
    ("escavadeira",  7,  330, 195),
    ("aviao",       16,  450, 180),
    ("submarino",   10,  330, 180),
    ("tanque",      12,  360, 180),
    ("jetsky",       2,  270, 165),
    ("rover",        5,  300, 180),
]

veiculos_imgs = {}
for nome, num, larg, alt in VEICULOS_INFO:
    try:
        img = pygame.image.load(f"assets/img/{nome}.png").convert_alpha()
        img = pygame.transform.scale(img, (larg, alt))
        veiculos_imgs[nome] = (img, num)
    except:
        print(f"Aviso: assets/img/{nome}.png não encontrado")

# ── Imagens das pessoas (2 frames cada) ──────────────────────────────────────
PESSOAS_FRAMES = []
for i in range(1, 5):
    try:
        f1 = pygame.image.load(f"assets/img/pessoa{i}.1.png").convert_alpha()
        f1 = pygame.transform.scale(f1, (110, 160))
        f2 = pygame.image.load(f"assets/img/pessoa{i}.2.png").convert_alpha()
        f2 = pygame.transform.scale(f2, (110, 160))
        PESSOAS_FRAMES.append([f1, f2])
    except:
        print(f"Aviso: pessoa{i}.1.png ou pessoa{i}.2.png não encontrado")

# ── Hitboxes das plataformas ─────────────────────────────────────────────────
HITBOX_OFFSETS = {
    id(rua_esq_img):  (5, 220, 20),
    id(rua_meio_img): (5, 220, 20),
    id(rua_dir_img):  (5, 220, 20),
    id(rua_img):      (5, 220, 20),
    id(plat1_img):    (5, 220, 580),
    id(plat2_img):    (270, 220, 540),
    id(plat3_img):    (580, 220, 585),
}

PLATS_VEICULO = {id(rua_img), id(rua_esq_img), id(rua_meio_img), id(rua_dir_img)}

#Criando conjuntos de possíveis plataformas + posição plataforma (500)
PLAT = [rua_img, plat1_img, plat2_img, plat3_img]
chao = HEIGHT - 400

tempo_pulo_max  = 15
Velocidade_pulo = -20
gravidade       = 1

def calcular_tempo_no_ar():
    y = 0
    vy = 0
    tempo_pulo = tempo_pulo_max
    pulando = True
    frames = 0

    while True: #contar quantidade de frames
        frames += 1

        if pulando and tempo_pulo > 0: # verificar se o personagem está no impulso do pulo (e ainda se stá disponível)
            vy = Velocidade_pulo
            tempo_pulo -= 1

        vy += gravidade
        y += vy

        if tempo_pulo == 0: #impulso pulo acabou
            pulando = False

        if y >= 0 and frames > 1: # player voltou ou passou do chao - deolve n° total de frames no ar
            return frames

tempo_no_ar_max = calcular_tempo_no_ar()

def calcular_gap_seguro(plat_anterior):
    velocidade = abs(velocidade_mundo)
    if plat_anterior.image is plat3_img:
        base_min, base_max = 180, 210
    elif plat_anterior.image is plat2_img:
        base_min, base_max = 150, 180
    elif plat_anterior.image is plat1_img:
        base_min, base_max = 160, 180
    else: # rua_img
        base_min, base_max = 160, 190

    # aumenta o gap conforme a velocidade do jogo aumenta
    bonus = max(0, (velocidade - 4) * 15)
    return random.randint(base_min + bonus, base_max + bonus)

# Conteúdo quantidade
coins        = 0
zombie_count = 1

#  Tela de início 
inicio_jogo        = True
largura_botao      = 200
botao_altura_b     = 60
centraliza_x_botao = WIDTH//2 - largura_botao//2
y_botao            = HEIGHT//2 + 50 #deixar um pouco mais para baixo do centro
botao_rect         = pygame.Rect(centraliza_x_botao, y_botao, largura_botao, botao_altura_b)

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


#  CLASSE PLATAFORMA
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem if imagem is not None else random.choice(PLAT) # sortear aleatoriamente uma das 4 plataformas
        self.rect  = self.image.get_rect() # cria um retângulo de plataforma (colisão)
        self.rect.x = x  #posição x da plataforma
        self.rect.y = y #posição y da plataforma
        margem_esq, offset_y, corte = HITBOX_OFFSETS[id(self.image)]
        self.hitbox = pygame.Rect(x + margem_esq, y + offset_y,
                                  self.rect.width - corte, 50)

    def update(self):
        self.rect.x   += velocidade_mundo  #mover a plataforma para a esquerda
        self.hitbox.x += velocidade_mundo
        if self.rect.right < 0:  # se a imagem sair da tela, a remove
            self.kill()


def criar_proxima_plataforma(plat_anterior):
    if random.random() < 0.2:
        return criar_trio(plat_anterior)
    imagem = random.choices(PLAT, weights=[5, 1, 1, 1], k=1)[0]
    margem_esq, offset_y, corte = HITBOX_OFFSETS[id(imagem)]
    gap = calcular_gap_seguro(plat_anterior)
    x   = plat_anterior.hitbox.right + gap - margem_esq
    return Plataforma(x, chao, imagem)


def criar_trio(plat_anterior):
    gap = calcular_gap_seguro(plat_anterior)

    # posição inicial do trio
    margem_esq, _, _ = HITBOX_OFFSETS[id(rua_esq_img)]

    x_inicio = plat_anterior.hitbox.right + gap - margem_esq

    # esquerda
    plat_esq = Plataforma(x_inicio, chao, rua_esq_img)

    # meio colado
    plat_meio = Plataforma(plat_esq.rect.right,chao,rua_meio_img)
    # direita colada
    plat_dir = Plataforma(plat_meio.rect.right,chao,rua_dir_img)

    return (plat_esq, plat_meio, plat_dir)


#  CLASSE MOEDA
class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = moeda_coletada
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += velocidade_mundo
        if self.rect.right < 0:
            self.kill()


def gerar_moedas(plat):
    if random.random() < 0.5:
        padrao = random.choice(['linha', 'arco', 'escada'])
        x_base = random.randint(plat.hitbox.left, plat.hitbox.right - 200)
        y_base = plat.hitbox.top - 160
        if padrao == 'linha':
            for i in range(5):
                m = Moeda(x_base + i * 50, y_base)
                moedas.add(m); todos_sprites.add(m)
        elif padrao == 'arco':
            for i, dy in enumerate([0, -60, -100, -60, 0]):
                m = Moeda(x_base + i * 50, y_base + dy)
                moedas.add(m); todos_sprites.add(m)
        elif padrao == 'escada':
            for i in range(5):
                m = Moeda(x_base + i * 50, y_base - i * 30)
                moedas.add(m); todos_sprites.add(m)


#  CLASSE BOMBA
class Bomba(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem, dano):
        pygame.sprite.Sprite.__init__(self)
        self.image  = imagem
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y # fica no chão da plataforma
        self.dano   = dano  # quantidade de zombies que mata

    def update(self):
        self.rect.x += velocidade_mundo
        if self.rect.right < 0:
            self.kill()


def gerar_bomba(plat):
    # não gera bomba nas plataformas pequenas
    if plat.image in [plat1_img, plat2_img, plat3_img]:
        return
    
    # Escolhe bombas baseado no tamanho da horda
    if zombie_count < 5:
        opcoes = ["explosivo2", "explosivos", "fronte", "granada", "bomba"]
    elif zombie_count < 10:
        opcoes = ["bomba", "granada", "fronte", "explosivos", "barril", "atomica"]
    else:
        opcoes = ["barril", "atomica", "foguete", "toxico"]
    if random.random() < 0.4:
        nome   = random.choice(opcoes)
        imagem, dano = bomba_imgs[nome]
        min_x  = plat.hitbox.left + 20
        max_x  = plat.hitbox.right - imagem.get_width() - 20
        if max_x <= min_x:
            return
        bombas.add(Bomba(random.randint(min_x, max_x), plat.hitbox.top, imagem, dano))


# ═══════════════════════════════════════════════════════════════
#  CLASSE PESSOA  (animada, 2 frames)
# ═══════════════════════════════════════════════════════════════
class Pessoa(pygame.sprite.Sprite):
    INTERVALO_ANIM = 20   # frames entre cada troca de imagem (~3x por segundo)

    def __init__(self, plataforma, frames):
        pygame.sprite.Sprite.__init__(self)
        self.frames  = frames          # [frame1, frame2]
        self.frame_atual = 0
        self.timer_anim  = 0
        self.image   = self.frames[0]
        self.plat    = plataforma

        self.rect = self.image.get_rect()
        self.rect.bottom = plataforma.hitbox.top

        # Posição aleatória com margem
        margem = 40
        min_x  = plataforma.hitbox.left  + margem
        max_x  = plataforma.hitbox.right - margem - self.rect.width
        if max_x > min_x:
            self.rect.left = random.randint(min_x, max_x)
        else:
            self.rect.left = min_x

        # Hitbox lateral (para o zumbi trocar com ela)
        self.hitbox = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.rect.width,
            self.rect.height
        )

        # margem para não sobrepor
        self.rect.width  = 110
        self.rect.height = 160

    def update(self):
        # Animação: alterna entre os 2 frames
        self.timer_anim += 1
        if self.timer_anim >= self.INTERVALO_ANIM:
            self.timer_anim  = 0
            self.frame_atual = 1 - self.frame_atual   # alterna 0 → 1 → 0
            self.image = self.frames[self.frame_atual]

        # Move junto com o mundo
        self.rect.x   += velocidade_mundo
        self.hitbox.x += velocidade_mundo

        # Se a plataforma foi removida, remove a pessoa
        if not self.plat.alive():
            self.kill()
            return

        # Acompanha superfície da plataforma
        self.rect.bottom   = self.plat.hitbox.top
        self.hitbox.bottom = self.rect.bottom
        self.hitbox.left   = self.rect.left

        if self.rect.right < 0:
            self.kill()


def gerar_pessoa(plat):
    if not PESSOAS_FRAMES:
        return
    if id(plat.image) not in PLATS_VEICULO:
        return

    # Sorteia quantas pessoas vão aparecer (0, 1, 2 ou 3)
    quantidade = random.choices([0, 1, 2, 3], weights=[20, 35, 30, 15])[0]

    x_ocupados = []  # controla posições já usadas para não sobrepor

    for _ in range(quantidade):
        frames = random.choice(PESSOAS_FRAMES)
        nova   = Pessoa(plat, frames)

        # Verifica sobreposição com moedas
        colidiu = any(nova.rect.colliderect(m.rect) for m in moedas)
        # Verifica sobreposição com veículos
        colidiu = colidiu or any(nova.rect.colliderect(v.rect) for v in veiculos)
        # Verifica sobreposição com outras pessoas
        colidiu = colidiu or any(nova.rect.colliderect(p.rect) for p in pessoas)
        # Verifica sobreposição com pessoas já geradas nesta rodada
        colidiu = colidiu or any(
            abs(nova.rect.centerx - x) < 90 for x in x_ocupados
        )

        if not colidiu:
            pessoas.add(nova)
            x_ocupados.append(nova.rect.centerx)


#  CLASSE VEÍCULO
class Veiculo(pygame.sprite.Sprite):
    def __init__(self, plataforma, img, numero):
        pygame.sprite.Sprite.__init__(self)
        self.image  = img
        self.numero = numero
        self.plat   = plataforma

        self.rect = self.image.get_rect()
        self.rect.bottom = plataforma.hitbox.top

        # Posição aleatória com margem dos dois lados
        margem = 80
        min_x  = plataforma.hitbox.left  + margem
        max_x  = plataforma.hitbox.right - margem - self.rect.width
        self.rect.left = random.randint(min_x, max_x)

        # ── Hitboxes do veículo ──────────────────────────────────────────
        # Lateral direita: empurra o zumbi (frente do veículo)
        self.hitbox_lateral = pygame.Rect(
            self.rect.left,
            self.rect.top + 20,          # começa um pouco abaixo do topo
            15,                           # largura fina na lateral esquerda
            self.rect.height - 20
        )
        # Topo: zumbi pode pousar em cima
        self.hitbox_topo = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.rect.width,
            15                            # altura fina no topo
        )

        self._font = pygame.font.SysFont("Arial Black", 22, bold=True)

    def update(self):
        dx = velocidade_mundo
        self.rect.x          += dx
        self.hitbox_lateral.x += dx
        self.hitbox_topo.x    += dx

        if not self.plat.alive():
            self.kill()
            return

        # Acompanha superfície da plataforma
        self.rect.bottom          = self.plat.hitbox.top
        self.hitbox_lateral.bottom = self.rect.bottom
        self.hitbox_topo.top       = self.rect.top

        if self.rect.right < 0:
            self.kill()

    def draw_badge(self, surface):
        txt    = self._font.render(str(self.numero), True, (20, 20, 20))
        tw, th = txt.get_size()
        pad    = 6
        bw, bh = tw + pad*2, th + pad*2
        cx     = self.rect.centerx
        cy     = self.rect.top - bh//2 - 4

        sh = pygame.Surface((bw+2, bh+2), pygame.SRCALPHA)
        pygame.draw.rect(sh, (0,0,0,100), sh.get_rect(), border_radius=8)
        surface.blit(sh, (cx - bw//2 - 1, cy - bh//2 + 2))

        badge = pygame.Surface((bw, bh), pygame.SRCALPHA)
        pygame.draw.rect(badge, (255,210,0,230), badge.get_rect(), border_radius=8)
        pygame.draw.rect(badge, (0,0,0,180),     badge.get_rect(), 2, border_radius=8)
        badge.blit(txt, (pad, pad))
        surface.blit(badge, (cx - bw//2, cy - bh//2))


def spawnar_veiculo(plataformas):
    plats_validas = [
        p for p in plataformas
        if id(p.image) in PLATS_VEICULO
        and p.hitbox.left >= WIDTH
        and p.hitbox.width > 350
    ]
    if not plats_validas or not veiculos_imgs:
        return None

    plats_sem_veiculo = [
        p for p in plats_validas
        if not any(v.plat is p for v in veiculos)
    ]
    if not plats_sem_veiculo:
        return None

    plat_escolhida = random.choice(plats_sem_veiculo)
    nome = random.choice(list(veiculos_imgs.keys()))
    img, numero = veiculos_imgs[nome]

    margem = 80
    if img.get_width() >= plat_escolhida.hitbox.width - margem * 2:
        return None

    # Tenta até 10 posições sem sobrepor moedas
    for _ in range(10):
        novo_veiculo = Veiculo(plat_escolhida, img, numero)
        if not any(novo_veiculo.rect.colliderect(m.rect) for m in moedas):
            # Remove pessoas que sobrepõem o veículo
            for p in list(pessoas):
                if novo_veiculo.rect.colliderect(p.rect):
                    p.kill()
            return novo_veiculo

    return None



#  CLASSE ZUMBI EXTRA (segue o líder com delay)

DELAY_PULO    = 8    # frames de delay entre cada zumbi na fila
ESPACO_FILA   = 70  # pixels de espaço entre cada zumbi

class ZumbiExtra(pygame.sprite.Sprite):
    def __init__(self, posicao_na_fila):
        pygame.sprite.Sprite.__init__(self)
        self.image = zombie_img
        self.rect  = self.image.get_rect()

        self.posicao_na_fila = posicao_na_fila  # 1, 2, 3...
        self.velocidade_y    = 0
        self.chao            = True

        # Timer de delay do pulo — cada zumbi espera mais
        self.timer_pulo_delay = 0
        self.delay_total      = posicao_na_fila * DELAY_PULO
        self.aguardando_pulo  = False
        self.pulando          = False
        self.tempo_pulo       = 0
        self.tempo_pulo_max   = 15

        # Posição inicial: atrás do player
        self.rect.x      = 150 - posicao_na_fila * ESPACO_FILA
        self.rect.bottom = 720

    def iniciar_pulo_delay(self):
        # Chamado quando o líder pula — começa a contar o delay.
        if self.chao and not self.aguardando_pulo and not self.pulando:
            self.aguardando_pulo  = True
            self.timer_pulo_delay = 0

    def soltar_pulo(self):
        self.pulando    = False
        self.tempo_pulo = 0

    def update(self, plataformas, veiculos):
        # Delay do pulo
        if self.aguardando_pulo:
            self.timer_pulo_delay += 1
            if self.timer_pulo_delay >= self.delay_total:
                self.aguardando_pulo = False
                if self.chao:
                    self.pulando    = True
                    self.tempo_pulo = self.tempo_pulo_max
                    self.chao       = False

        # Pulo
        if self.pulando and self.tempo_pulo > 0:
            self.velocidade_y = -20
            self.tempo_pulo  -= 1

        # Gravidade
        self.velocidade_y += 1
        self.rect.y       += self.velocidade_y

        # Posição X: segue atrás do player com espaço fixo
        x_alvo = 150 - self.posicao_na_fila * ESPACO_FILA
        self.rect.x = x_alvo

        self.chao = False

        # Colisão com plataformas
        for plat in plataformas:
            if self.rect.colliderect(plat.hitbox):
                if self.velocidade_y > 0:
                    self.rect.bottom = plat.hitbox.top
                    self.velocidade_y = 0
                    self.chao = True

        # Colisão com veículos (pousa em cima)
        for v in veiculos:
            if self.rect.colliderect(v.hitbox_topo):
                if self.velocidade_y > 0:
                    self.rect.bottom = v.hitbox_topo.top
                    self.velocidade_y = 0
                    self.chao = True

        # Cai no buraco → game over (tratado no loop principal)
        if self.rect.top > HEIGHT:
            return True
        return False


#  CLASSE JOGADOR
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        #imagem Jogador/zombie
        self.image = zombie_img
        self.rect  = self.image.get_rect()
        self.pulando = False # botão espaço sendo segurado
        self.tempo_pulo = 0  # frames restantes do pulo
        self.tempo_pulo_max = 15  # frames máximos segurando o espaço

        # Posição inicial
        self.rect.x = 150 #posiciona o jogador x =150
        self.rect.bottom = 720 # ficar em cima do chão

        # Pulo
        self.velocidade_y = 0
        self.velocidade_x = 0
        self.chao = True #permitir pular

    def update(self, plataformas, veiculos, pessoas):
        if self.pulando and self.tempo_pulo > 0:
            self.velocidade_y = -20
            self.tempo_pulo  -= 1

            if self.rect.x < 150 and self.velocidade_x == 0:
                self.velocidade_x += 5

        self.velocidade_y += 1
        self.rect.y += self.velocidade_y

        self.rect.x += self.velocidade_x 
        if self.rect.x >= 150:
            self.velocidade_x = 0
            self.rect.x = 150

        self.chao = False

        # ── Colisão com plataformas ───────────────────────────────────────
        for plat in plataformas:
            if self.rect.colliderect(plat.hitbox):
                if self.velocidade_y > 0:
                    self.rect.bottom = plat.hitbox.top
                    self.velocidade_y = 0
                    self.chao = True

        # ── Colisão com veículos ──────────────────────────────────────────
        for v in veiculos:
            # Pousa em cima do veículo
            if self.rect.colliderect(v.hitbox_topo):
                if self.velocidade_y > 0:
                    self.rect.bottom = v.hitbox_topo.top
                    self.velocidade_y = 0
                    self.chao = True

            # Lateral: fica preso (empurrado junto com o veículo)
            elif self.rect.colliderect(v.hitbox_lateral):
                # Encosta na lateral esquerda do veículo
                self.rect.right = v.hitbox_lateral.left

        # ── Game over por cair no buraco ──────────────────────────────────
        if self.rect.top > HEIGHT:
            return True # game over

        # ── Game over por sair pela esquerda (preso atrás do veículo) ────
        if self.rect.right < 0:
            return True

        return False

    def pular(self): # chamado quando APERTA o espaço
        if self.chao: # só pula se estiver no chão
            self.pulando = True
            self.tempo_pulo = self.tempo_pulo_max
            self.chao = False
            # Avisa todos os zumbis extras para preparar o pulo com delay
            for z in zumbis_extras:
                z.iniciar_pulo_delay()

    def soltar_pulo(self): # chamado quando SOLTA o espaço
        self.pulando = False # desativar o pulo
        self.tempo_pulo = 0
        for z in zumbis_extras:
            z.soltar_pulo()


# Criar jogador + grupo sprites
player = Jogador()
todos_sprites = pygame.sprite.Group()
moedas = pygame.sprite.Group()
bombas = pygame.sprite.Group()
plataformas = pygame.sprite.Group()
veiculos = pygame.sprite.Group()
pessoas = pygame.sprite.Group()
zumbis_extras = pygame.sprite.Group()  # grupo da horda
todos_sprites.add(player)


# Criação plataformas iniciais
plat_inicial = Plataforma(0, chao, rua_img)
plat_inicial.hitbox = pygame.Rect(0, chao + 220, largura, 50)
todos_sprites.add(plat_inicial)
plataformas.add(plat_inicial)

ultima_plat = plat_inicial
x_final = plat_inicial.hitbox.right

while x_final < WIDTH + 200:
    resultado = criar_proxima_plataforma(ultima_plat)
    if isinstance(resultado, tuple):
        for plat in resultado:
            todos_sprites.add(plat)
            plataformas.add(plat)
            gerar_moedas(plat)
            gerar_pessoa(plat)
        ultima_plat = resultado[-1]
    else:
        todos_sprites.add(resultado)
        plataformas.add(resultado)
        gerar_moedas(resultado)
        gerar_pessoa(resultado)
        ultima_plat = resultado
    x_final = ultima_plat.hitbox.right

timer_jogo      = 0
DELAY_VEICULOS  = 5 * FPS
timer_spawn_vei = 0
INTERVALO_SPAWN = FPS


#  LOOP PRINCIPAL
while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.pular()

        if event.type == pygame.KEYUP: # quando SOLTA a tecla
            if event.key == pygame.K_SPACE:
                player.soltar_pulo()

    timer_jogo += 1

    if timer_jogo > DELAY_VEICULOS:
        timer_spawn_vei += 1
        if timer_spawn_vei >= INTERVALO_SPAWN:
            timer_spawn_vei = 0
            novo_vei = spawnar_veiculo(plataformas)
            if novo_vei:
                veiculos.add(novo_vei)

    # Move o background
    background_rect.x += velocidade_mundo
    if background_rect.right < 0:
        background_rect.x = 0

    #Move as placasa igual ao background
    placas_rect.x += velocidade_mundo
    if placas_rect.right < 0:
        placas_rect.x = 0

    #Aumentando a velocidade do mapa a cada 10 segundos (10*60 = 600 frames)
    timer_velocidade += 1
    if timer_velocidade >= 600:
        timer_velocidade = 0
        if velocidade_mundo > velocidade_max:
            velocidade_mundo -= 1

    # Atualiza jogador passando veículos também
    game_over = player.update(plataformas, veiculos, pessoas)
    if game_over:
        window.blit(gameover_img, (0, 0))
        pygame.display.update()
        pygame.time.wait(3000)
        game = False

    # Atualiza plat, veiculo e pessoas
    plataformas.update()
    veiculos.update()
    pessoas.update()

    # Atualiza zumbis extras
    for z in list(zumbis_extras):
        caiu = z.update(plataformas, veiculos)
        if caiu:
            z.kill()

    # Colisão do player com pessoas → some a pessoa, adiciona zumbi extra
    pessoas_atingidas = pygame.sprite.spritecollide(player, pessoas, True)
    for _ in pessoas_atingidas:
        zombie_count += 1
        nova_posicao = len(zumbis_extras) + 1
        novo_z = ZumbiExtra(nova_posicao)
        zumbis_extras.add(novo_z)

    # Coleta de moedas
    moedas_coletadas = pygame.sprite.spritecollide(player, moedas, True)
    for _ in moedas_coletadas:
        coins += 1

    # Colisão com bombas
    bombas_atingidas = pygame.sprite.spritecollide(player, bombas, True)
    for bomba in bombas_atingidas:
        som_explosao.play()
        zombie_count -= bomba.dano
        # Remove zumbis extras se zombie_count diminuiu
        while len(zumbis_extras) >= zombie_count and len(zumbis_extras) > 0:
            ultimo = list(zumbis_extras)[-1]
            ultimo.kill()
        if zombie_count <= 0:
            zombie_count = 0
            game_over = True

    # Atualiza moedas e bomba
    moedas.update()
    bombas.update()

    # Gera novas plataformas pela direita
    plats_visiveis = [p for p in plataformas if p.rect.right > 0]
    while not plats_visiveis or max(p.rect.right for p in plats_visiveis) < WIDTH:
        ultima_plat = max(plats_visiveis, key=lambda p: p.hitbox.right) \
                      if plats_visiveis else None
        if ultima_plat:
            resultado = criar_proxima_plataforma(ultima_plat)
            if isinstance(resultado, tuple):
                for plat in resultado:
                    todos_sprites.add(plat)
                    plataformas.add(plat)
                    gerar_pessoa(plat)
                    gerar_moedas(plat)
                ultima_plat = resultado[-1]
            else:
                todos_sprites.add(resultado)
                plataformas.add(resultado)
                gerar_pessoa(resultado)
                gerar_moedas(resultado)
                ultima_plat = resultado
        else:
            nova_plat = Plataforma(WIDTH, chao, random.choice(PLAT))
            todos_sprites.add(nova_plat)
            plataformas.add(nova_plat)
            gerar_bomba(nova_plat)
            gerar_pessoa(nova_plat)
        plats_visiveis = [p for p in plataformas if p.rect.right > 0]

    # Desenha as placas se movendo
    window.fill(preto)

    window.blit(background, background_rect)
    background_rect2   = background_rect.copy()
    background_rect2.x += background_rect2.width
    window.blit(background, background_rect2)

    window.blit(placas_img, placas_rect)
    placas_rect2   = placas_rect.copy()
    placas_rect2.x += placas_rect2.width
    window.blit(placas_img, placas_rect2)

    # 4. Plataformas 
    plataformas.draw(window)

    # 5. Moedas
    moedas.draw(window)

    #6. Bombas
    bombas.draw(window)

    #7. Pessoas
    pessoas.draw(window) 

    # MOSTRAR HITBOX DAS BOMBAS
    for bomba in bombas:
        pygame.draw.rect(window, vermelho, bomba.rect, 2)

    for v in veiculos:
        window.blit(v.image, v.rect)

    # 8. Zumbis extras (desenhados antes do líder para ficar atrás)
    for z in zumbis_extras:
        window.blit(z.image, z.rect)

    # 9. Jogador (líder — desenhado por cima)
    window.blit(player.image, player.rect)

    # Desenha a mão da quantidade de zombies
    window.blit(mao_img, (70, 70))
    # Texto quantidade moedas
    qnt_zombie = font.render(str(zombie_count), True, branco)
    window.blit(qnt_zombie, (170, 100))

    # Desenho da moeda
    window.blit(moeda_img, (75, 180))
    # Texto quantidade moedas
    qnt_moedas = font.render(str(coins), True, branco)
    window.blit(qnt_moedas, (170, 200))

    pygame.display.update()

pygame.quit()
