
import pygame
import random
import math

pygame.init()

# JANELA
LARGURA = 1100
ALTURA = 700

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pink Hole Simulation")

relogio = pygame.time.Clock()

CENTRO_X = LARGURA // 2
CENTRO_Y = ALTURA // 2

RAIO_BURACO = 65

# ESTRELAS
random.seed(42)
estrelas = []

for i in range(250):
    estrelas.append((
        random.randint(0, LARGURA),
        random.randint(0, ALTURA),
        random.randint(50, 220),
        random.choice([1, 1, 1, 2])
    ))

# PARTÍCULAS
particulas = []

QUANTIDADE = 5500

for i in range(QUANTIDADE):
    raio = random.uniform(95, 310)
    angulo = random.uniform(0, math.tau)

    velocidade = 0.015 * (130 / raio) ** 1.5

    particulas.append({
        "raio": raio,
        "angulo": angulo,
        "velocidade": velocidade,
        "brilho": random.randint(150, 255)
    })

# CAMADA DE LUZ
camada_brilho = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

# ANIMAÇÃO
executando = True

while executando:

    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
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

    camada_brilho.fill((0, 0, 0, 0))

    # DISCO ROSA
    for particula in particulas:

        particula["angulo"] += particula["velocidade"]

        raio = particula["raio"]
        angulo = particula["angulo"]

        x = CENTRO_X + math.cos(angulo) * raio
        y = CENTRO_Y + math.sin(angulo) * raio * 0.35

        distancia = (raio - 95) / 215

        # GRADIENTE ROSA
        if distancia < 0.35:
            cor = (255, 210, 245)
        elif distancia < 0.65:
            cor = (255, 100, 205)
        else:
            cor = (230, 35, 145)

        posicao = (int(x), int(y))

        # Brilho suave
        pygame.draw.circle(
            camada_brilho,
            (*cor, 22),
            posicao,
            5
        )

        # Partícula principal
        pygame.draw.circle(
            tela,
            cor,
            posicao,
            1
        )

    # ADICIONA O BRILHO
    tela.blit(
        camada_brilho,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_ADD
    )

    # CENTRO ESCURO
    pygame.draw.circle(
        tela,
        (5, 2, 12),
        (CENTRO_X, CENTRO_Y),
        RAIO_BURACO
    )

    pygame.display.flip()

pygame.quit()
