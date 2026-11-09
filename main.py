
import pygame
import random
import math

pygame.init()

# ==========================================
# PINK HOLE - GRAVITATIONAL LENSING
# ==========================================

LARGURA = 1100
ALTURA = 700
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pink Hole | Gravitational Lensing")

relogio = pygame.time.Clock()

CX = LARGURA // 2
CY = ALTURA // 2

RAIO_BURACO = 65
RAIO_INTERNO = 90
RAIO_EXTERNO = 310

random.seed(42)

# ==========================================
# ESTRELAS
# ==========================================

estrelas = []

for _ in range(250):
    estrelas.append((
        random.randrange(LARGURA),
        random.randrange(ALTURA),
        random.randint(50, 210),
        random.choice([1, 1, 1, 2])
    ))

# ==========================================
# PARTICULAS DO DISCO
# ==========================================

particulas = []

for _ in range(6500):
    distribuicao = random.random() ** 1.4

    raio = RAIO_INTERNO + distribuicao * (
        RAIO_EXTERNO - RAIO_INTERNO
    )

    particulas.append({
        "raio": raio,
        "angulo": random.uniform(0, math.tau),
        "velocidade": 0.018 * (110 / raio) ** 1.5,
        "brilho": random.uniform(0.65, 1.0),
        "espessura": random.uniform(-5, 5)
    })

# ==========================================
# PALETA ROSA
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

    return tuple(int(c * brilho) for c in cor)

# ==========================================
# ARCOS DE LENTE GRAVITACIONAL
# ==========================================

def desenhar_arcos(superficie, tempo):

    # Cada arco acompanha uma elipse
    # deformada para simular luz curvada.

    for lado in [-1, 1]:

        for camada in range(7):

            pontos = []

            for i in range(101):

                t = i / 100
                x_normalizado = -1 + 2 * t

                x = CX + x_normalizado * (
                    145 + camada * 5
                )

                altura = math.sqrt(
                    max(0, 1 - x_normalizado ** 2)
                )

                y = (
                    CY
                    + lado * altura * (
                        100 + camada * 4
                    )
                )

                # Movimento sutil do brilho
                onda = math.sin(
                    t * math.tau * 3 + tempo * 0.8
                ) * 1.5

                y += onda

                pontos.append((int(x), int(y)))

            alpha = max(8, 95 - camada * 14)

            pygame.draw.lines(
                superficie,
                (255, 105, 210, alpha),
                False,
                pontos,
                max(1, 4 - camada // 2)
            )

# ==========================================
# CAMADAS DE RENDERIZACAO
# ==========================================

disco = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

arcos = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

# Brilho estatico ao redor do centro
brilho_central = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

for raio, alpha in [
    (110, 5),
    (95, 8),
    (80, 14),
    (72, 24)
]:
    pygame.draw.circle(
        brilho_central,
        (255, 70, 180, alpha),
        (CX, CY),
        raio,
        5
    )

# ==========================================
# LOOP PRINCIPAL
# ==========================================

executando = True
tempo = 0

while executando:

    dt = min(relogio.tick(FPS) / 1000, 0.05)
    tempo += dt

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                executando = False

    tela.fill((0, 0, 0))

    # ESTRELAS
    for x, y, brilho, tamanho in estrelas:
        pygame.draw.circle(
            tela,
            (brilho, brilho, brilho),
            (x, y),
            tamanho
        )

    tela.blit(brilho_central, (0, 0))

    # DISCO DE ACRECAO
    disco.fill((0, 0, 0, 0))

    for p in particulas:

        p["angulo"] = (
            p["angulo"]
            + p["velocidade"] * dt * 60
        ) % math.tau

        raio = p["raio"]
        angulo = p["angulo"]

        x = CX + math.cos(angulo) * raio
        y = (
            CY
            + math.sin(angulo) * raio * 0.34
            + p["espessura"]
        )

        cor = cor_particula(raio, p["brilho"])

        pygame.draw.circle(
            disco,
            (*cor, 175),
            (int(x), int(y)),
            2
        )

    # DISCO SUAVIZADO
    disco_pequeno = pygame.transform.smoothscale(
        disco,
        (LARGURA // 3, ALTURA // 3)
    )

    disco_suave = pygame.transform.smoothscale(
        disco_pequeno,
        (LARGURA, ALTURA)
    )

    disco_suave.set_alpha(115)

    tela.blit(
        disco_suave,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_ADD
    )

    tela.blit(disco, (0, 0))

    # ARCOS GRAVITACIONAIS
    arcos.fill((0, 0, 0, 0))
    desenhar_arcos(arcos, tempo)
    tela.blit(arcos, (0, 0))

    # SOMBRA CENTRAL
    pygame.draw.circle(
        tela,
        (3, 1, 9),
        (CX, CY),
        RAIO_BURACO
    )

    # ANEL LUMINOSO
    pygame.draw.circle(
        tela,
        (255, 125, 220),
        (CX, CY),
        RAIO_BURACO + 2,
        2
    )

    pygame.display.flip()

pygame.quit()
