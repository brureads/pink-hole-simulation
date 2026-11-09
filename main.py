
import pygame
import random
import math

pygame.init()

# ==========================================
# PINK HOLE 6.0 - COSMIC NEBULA
# ==========================================

LARGURA = 1100
ALTURA = 700
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pink Hole 6.0 | Cosmic Nebula")

relogio = pygame.time.Clock()

CX = LARGURA // 2
CY = ALTURA // 2

RAIO_BURACO = 65
RAIO_INTERNO = 88
RAIO_EXTERNO = 310

# ==========================================
# CONTROLES
# ==========================================

inclinacao = 0.34
velocidade = 1.0
pausado = False

# ==========================================
# ESTRELAS
# ==========================================

random.seed(42)

estrelas = []

for _ in range(250):
    estrelas.append((
        random.randint(0, LARGURA - 1),
        random.randint(0, ALTURA - 1),
        random.randint(50, 210),
        random.choice([1, 1, 1, 2])
    ))

# ==========================================
# PARTICULAS
# ==========================================

particulas = []

QUANTIDADE = 7000

for _ in range(QUANTIDADE):

    distribuicao = random.random() ** 1.4

    raio = (
        RAIO_INTERNO
        + distribuicao * (RAIO_EXTERNO - RAIO_INTERNO)
    )

    angulo = random.uniform(0, math.tau)

    velocidade_orbital = (
        0.018 * (110 / raio) ** 1.5
    )

    particulas.append({
        "raio": raio,
        "angulo": angulo,
        "velocidade": velocidade_orbital,
        "brilho": random.uniform(0.65, 1.0),
        "espessura": random.uniform(-7, 7)
    })

# ==========================================
# CORES DA NEBULOSA
# ==========================================

def cor_particula(raio, brilho):

    distancia = (
        (raio - RAIO_INTERNO)
        / (RAIO_EXTERNO - RAIO_INTERNO)
    )

    if distancia < 0.20:
        cor = (255, 225, 250)

    elif distancia < 0.48:
        cor = (255, 135, 220)

    elif distancia < 0.75:
        cor = (255, 65, 175)

    else:
        cor = (190, 30, 120)

    return tuple(
        int(c * brilho) for c in cor
    )

# ==========================================
# BRILHO DA NEBULOSA
# ==========================================

glow = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

for raio, alpha in [
    (290, 3),
    (240, 5),
    (190, 8),
    (145, 12),
    (105, 18)
]:

    superficie = pygame.Surface(
        (raio * 2, raio * 2),
        pygame.SRCALPHA
    )

    pygame.draw.ellipse(
        superficie,
        (255, 45, 165, alpha),
        (
            0,
            int(raio * 0.65),
            raio * 2,
            int(raio * 0.7)
        )
    )

    glow.blit(
        superficie,
        (CX - raio, CY - raio)
    )

# ==========================================
# ANEL LUMINOSO
# ==========================================

anel = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

for raio, alpha, largura in [
    (76, 12, 14),
    (73, 20, 9),
    (70, 45, 4),
    (68, 90, 2)
]:

    pygame.draw.circle(
        anel,
        (255, 115, 215, alpha),
        (CX, CY),
        raio,
        largura
    )

# ==========================================
# CAMADA DO DISCO
# ==========================================

disco = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

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
                inclinacao = min(
                    0.90,
                    inclinacao + 0.05
                )

            elif evento.key == pygame.K_DOWN:
                inclinacao = max(
                    0.12,
                    inclinacao - 0.05
                )

            elif evento.key == pygame.K_RIGHT:
                velocidade = min(
                    4.0,
                    velocidade + 0.25
                )

            elif evento.key == pygame.K_LEFT:
                velocidade = max(
                    0.0,
                    velocidade - 0.25
                )

            elif evento.key == pygame.K_r:
                inclinacao = 0.34
                velocidade = 1.0
                pausado = False

    tela.fill((0, 0, 0))

    # ESTRELAS
    for x, y, brilho, tamanho in estrelas:

        pygame.draw.circle(
            tela,
            (brilho, brilho, brilho),
            (x, y),
            tamanho
        )

    # BRILHO DE FUNDO
    tela.blit(glow, (0, 0))

    disco.fill((0, 0, 0, 0))

    # PARTICULAS
    for p in particulas:

        if not pausado:
            p["angulo"] = (
                p["angulo"]
                + p["velocidade"] * dt * 60 * velocidade
            ) % math.tau

        raio = p["raio"]
        angulo = p["angulo"]

        x = CX + math.cos(angulo) * raio

        y = (
            CY
            + math.sin(angulo) * raio * inclinacao
            + p["espessura"]
        )

        cor = cor_particula(
            raio,
            p["brilho"]
        )

        pygame.draw.circle(
            disco,
            (*cor, 175),
            (int(x), int(y)),
            2
        )

    # SUAVIZACAO
    disco_pequeno = pygame.transform.smoothscale(
        disco,
        (LARGURA // 3, ALTURA // 3)
    )

    disco_suave = pygame.transform.smoothscale(
        disco_pequeno,
        (LARGURA, ALTURA)
    )

    disco_suave.set_alpha(135)

    tela.blit(
        disco_suave,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_ADD
    )

    tela.blit(disco, (0, 0))

    # ANEL LUMINOSO
    tela.blit(anel, (0, 0))

    # CENTRO ESCURO
    pygame.draw.circle(
        tela,
        (3, 1, 9),
        (CX, CY),
        RAIO_BURACO
    )

    pygame.display.flip()

pygame.quit()
