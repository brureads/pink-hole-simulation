
import pygame
import random
import math

pygame.init()

# ==========================================
# PINK HOLE 6.8 - SOFT PLASMA
# ==========================================

LARGURA = 1100
ALTURA = 700
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pink Hole 6.8 | Soft Plasma")
relogio = pygame.time.Clock()

CX = LARGURA // 2
CY = ALTURA // 2

RAIO_BURACO = 37
RAIO_INTERNO = 47
RAIO_EXTERNO = 310

INCLINACAO_INICIAL = 0.34
VELOCIDADE_INICIAL = 1.0

inclinacao = INCLINACAO_INICIAL
velocidade = VELOCIDADE_INICIAL
pausado = False
tempo = 0.0

random.seed(42)

# ==========================================
# ESTRELAS
# ==========================================

estrelas = []

for _ in range(250):
    estrelas.append((
        random.randint(0, LARGURA - 1),
        random.randint(0, ALTURA - 1),
        random.randint(50, 210),
        random.choice([1, 1, 1, 2])
    ))

# ==========================================
# PARTICULAS EXTERNAS
# ==========================================

particulas = []

for _ in range(14000):
    distribuicao = random.random() ** 1.4

    raio = RAIO_INTERNO + distribuicao * (
        RAIO_EXTERNO - RAIO_INTERNO
    )

    particulas.append({
        "raio": raio,
        "angulo": random.uniform(0, math.tau),
        "velocidade": 0.018 * (110 / raio) ** 1.5,
        "brilho": random.uniform(0.45, 0.85),
        "espessura": random.uniform(-5, 5),
        "tamanho": random.choice([1, 1, 1, 2])
    })

# ==========================================
# PARTICULAS INTERNAS
# ==========================================

particulas_internas = []

for _ in range(4000):
    raio = random.uniform(43, 115)

    particulas_internas.append({
        "raio": raio,
        "angulo": random.uniform(0, math.tau),
        "velocidade": 0.018 * (110 / raio) ** 1.5,
        "brilho": random.uniform(0.40, 0.80),
        "espessura": random.uniform(-3, 3),
        "tamanho": 1
    })

# ==========================================
# PARTICULAS DO ARCO SUPERIOR
# ==========================================

particulas_arco = []

for _ in range(1700):
    particulas_arco.append({
        "angulo": random.uniform(math.pi, math.tau),
        "raio": random.gauss(48, 7),
        "brilho": random.uniform(0.3, 0.75),
        "fase": random.uniform(0, math.tau)
    })

# ==========================================
# CORES DO PLASMA
# ==========================================

def cor_particula(raio, brilho):
    if raio < 70:
        cor = (255, 175, 225)
    elif raio < 105:
        cor = (255, 145, 215)
    elif raio < 150:
        cor = (255, 115, 205)
    elif raio < 220:
        cor = (245, 65, 175)
    else:
        cor = (185, 30, 120)

    return tuple(
        min(255, int(c * brilho))
        for c in cor
    )

# ==========================================
# SUPERFICIES
# ==========================================

disco_tras = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

disco_frente = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

arco = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

# ==========================================
# BRILHO DIFUSO EM DUAS CAMADAS
# ==========================================

def aplicar_brilho(superficie, intensidade):
    # Camada ampla: espalha a luz
    pequeno = pygame.transform.smoothscale(
        superficie,
        (LARGURA // 8, ALTURA // 8)
    )

    amplo = pygame.transform.smoothscale(
        pequeno,
        (LARGURA, ALTURA)
    )

    amplo.set_alpha(intensidade // 2)

    tela.blit(
        amplo,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_ADD
    )

    # Camada suave: une as particulas
    medio = pygame.transform.smoothscale(
        superficie,
        (LARGURA // 3, ALTURA // 3)
    )

    suave = pygame.transform.smoothscale(
        medio,
        (LARGURA, ALTURA)
    )

    suave.set_alpha(intensidade)

    tela.blit(
        suave,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_ADD
    )

# ==========================================
# DESENHAR PARTICULAS
# ==========================================

def desenhar_particulas(lista, superficie, metade):
    for p in lista:
        angulo = p["angulo"]

        if metade == "tras" and math.sin(angulo) >= 0:
            continue

        if metade == "frente" and math.sin(angulo) < 0:
            continue

        raio = p["raio"]

        x = CX + math.cos(angulo) * raio
        y = (
            CY
            + math.sin(angulo) * raio * inclinacao
            + p["espessura"]
        )

        cor = cor_particula(raio, p["brilho"])

        pygame.draw.circle(
            superficie,
            (*cor, 145),
            (int(x), int(y)),
            p["tamanho"]
        )

# ==========================================
# ARCO GRAVITACIONAL
# ==========================================

def desenhar_arco():
    arco.fill((0, 0, 0, 0))

    for p in particulas_arco:
        angulo = p["angulo"]
        raio = p["raio"]

        oscilacao = math.sin(
            tempo * 0.7 + p["fase"]
        ) * 0.7

        x = CX + math.cos(angulo) * raio
        y = (
            CY
            + math.sin(angulo) * raio * 0.95
            + oscilacao
        )

        brilho = p["brilho"]

        cor = (
            255,
            int(75 + 80 * brilho),
            int(150 + 60 * brilho),
            int(25 + 85 * brilho)
        )

        pygame.draw.circle(
            arco,
            cor,
            (int(x), int(y)),
            1
        )

    aplicar_brilho(arco, 65)
    tela.blit(arco, (0, 0))

# ==========================================
# MOVIMENTO
# ==========================================

def atualizar_particulas(lista, dt):
    if pausado:
        return

    for p in lista:
        p["angulo"] = (
            p["angulo"]
            + p["velocidade"] * dt * 60 * velocidade
        ) % math.tau

# ==========================================
# LOOP PRINCIPAL
# ==========================================

executando = True

while executando:
    dt = min(relogio.tick(FPS) / 1000, 0.05)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                executando = False

            elif evento.key == pygame.K_SPACE:
                pausado = not pausado

            elif evento.key == pygame.K_UP:
                inclinacao = min(0.90, inclinacao + 0.05)

            elif evento.key == pygame.K_DOWN:
                inclinacao = max(0.12, inclinacao - 0.05)

            elif evento.key == pygame.K_RIGHT:
                velocidade = min(4.0, velocidade + 0.25)

            elif evento.key == pygame.K_LEFT:
                velocidade = max(0.0, velocidade - 0.25)

            elif evento.key == pygame.K_r:
                inclinacao = INCLINACAO_INICIAL
                velocidade = VELOCIDADE_INICIAL
                pausado = False

    if not pausado:
        tempo += dt * velocidade

    atualizar_particulas(particulas, dt)
    atualizar_particulas(particulas_internas, dt)

    tela.fill((0, 0, 0))

    # ESTRELAS
    for x, y, brilho, tamanho in estrelas:
        pygame.draw.circle(
            tela,
            (brilho, brilho, brilho),
            (x, y),
            tamanho
        )

    # 1. DISCO DE TRAS
    disco_tras.fill((0, 0, 0, 0))

    desenhar_particulas(
        particulas,
        disco_tras,
        "tras"
    )

    desenhar_particulas(
        particulas_internas,
        disco_tras,
        "tras"
    )

    aplicar_brilho(disco_tras, 120)
    tela.blit(disco_tras, (0, 0))

    # 2. ARCO SUPERIOR
    desenhar_arco()

    # 3. SOMBRA CENTRAL
    pygame.draw.circle(
        tela,
        (3, 1, 9),
        (CX, CY),
        RAIO_BURACO
    )

    # 4. DISCO DA FRENTE
    disco_frente.fill((0, 0, 0, 0))

    desenhar_particulas(
        particulas,
        disco_frente,
        "frente"
    )

    desenhar_particulas(
        particulas_internas,
        disco_frente,
        "frente"
    )

    aplicar_brilho(disco_frente, 105)
    tela.blit(disco_frente, (0, 0))

    pygame.display.flip()

pygame.quit()
