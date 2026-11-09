
import pygame
import numpy as np
import math
import random

pygame.init()

# ==========================================
# PINK HOLE 5.0 - NEBULA ENGINE
# ==========================================

LARGURA = 1100
ALTURA = 700
FPS = 60

# Renderizamos o plasma em resolucao
# reduzida para melhorar o desempenho.
ESCALA = 3
W = LARGURA // ESCALA
H = ALTURA // ESCALA

CX = LARGURA // 2
CY = ALTURA // 2

RAIO_SOMBRA = 65

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption(
    "Pink Hole 5.0 | Nebula Engine"
)

relogio = pygame.time.Clock()

# ==========================================
# FUNDO ESTRELADO
# ==========================================

random.seed(42)

fundo = pygame.Surface(
    (LARGURA, ALTURA)
)

fundo.fill((0, 0, 0))

for _ in range(250):
    x = random.randrange(LARGURA)
    y = random.randrange(ALTURA)

    brilho = random.randint(45, 200)

    pygame.draw.circle(
        fundo,
        (brilho, brilho, brilho),
        (x, y),
        random.choice([1, 1, 2])
    )

# ==========================================
# COORDENADAS DO PLASMA
# ==========================================

# O NumPy cria uma grade de coordenadas.
# Cada posicao representa um pixel.

xs = (
    np.arange(W, dtype=np.float32)
    * ESCALA - CX
)

ys = (
    np.arange(H, dtype=np.float32)
    * ESCALA - CY
)

X, Y = np.meshgrid(xs, ys)

# ==========================================
# CONFIGURACOES INTERATIVAS
# ==========================================

inclinacao = 0.34
velocidade = 1.0
pausado = False
tempo = 0.0

# ==========================================
# FUNCAO DO PLASMA
# ==========================================

def criar_plasma(t, inclinacao):

    # Corrige a perspectiva do disco
    # conforme sua inclinacao.

    altura = max(0.12, inclinacao)

    Y_DISCO = Y / altura

    raio = np.sqrt(
        X * X + Y_DISCO * Y_DISCO
    )

    angulo = np.arctan2(
        Y_DISCO, X
    )

    # Rotacao diferencial:
    # materia interna gira mais rapido.

    rotacao = (
        t * 2.5
        / np.maximum(raio / 100, 0.5) ** 1.5
    )

    fase = angulo - rotacao

    # Textura turbulenta do plasma
    turbulencia = (
        np.sin(fase * 12 + raio * 0.13)
        * np.sin(fase * 7 - raio * 0.08)
    )

    turbulencia += (
        0.5 * np.sin(
            fase * 23 + raio * 0.21
        )
    )

    turbulencia = (
        turbulencia / 2.5
    )

    # Disco principal
    centro_disco = 165

    largura_disco = 85

    densidade = np.exp(
        -(
            (raio - centro_disco)
            / largura_disco
        ) ** 2
    )

    # Reduz a luz nas bordas
    borda_interna = np.clip(
        (raio - 82) / 28,
        0, 1
    )

    borda_externa = np.clip(
        (315 - raio) / 65,
        0, 1
    )

    densidade *= (
        borda_interna * borda_externa
    )

    # Faixas luminosas
    filamentos = (
        0.75
        + 0.25 * np.sin(
            fase * 18
            + raio * 0.10
            + turbulencia * 3
        )
    )

    plasma = (
        densidade
        * filamentos
        * (1 + turbulencia * 0.35)
    )

    plasma = np.clip(plasma, 0, 1)

    # ======================================
    # LUZ CURVADA - EFEITO ARTISTICO
    # ======================================

    # Arcos que acompanham a geometria
    # do disco, sem desenhar linhas.

    raio_tela = np.sqrt(
        X * X + Y * Y
    )

    arco_superior = np.exp(
        -(
            (
                Y
                + 100 * np.sqrt(
                    np.maximum(
                        0,
                        1 - (X / 160) ** 2
                    )
                )
            ) / 24
        ) ** 2
    )

    arco_inferior = np.exp(
        -(
            (
                Y
                - 100 * np.sqrt(
                    np.maximum(
                        0,
                        1 - (X / 160) ** 2
                    )
                )
            ) / 24
        ) ** 2
    )

    limite_arco = np.clip(
        (170 - np.abs(X)) / 25,
        0, 1
    )

    arcos = (
        arco_superior + arco_inferior
    ) * limite_arco

    # Textura dos arcos acompanha
    # o movimento do plasma.

    textura_arco = (
        0.75
        + 0.25 * np.sin(
            X * 0.08
            - t * 3
            + Y * 0.03
        )
    )

    arcos *= textura_arco * 0.75

    intensidade = np.clip(
        plasma + arcos,
        0, 1.4
    )

    # ======================================
    # PALETA ROSA
    # ======================================

    vermelho = np.clip(
        intensidade * 255,
        0, 255
    )

    verde = np.clip(
        intensidade ** 1.7 * 185,
        0, 255
    )

    azul = np.clip(
        intensidade * 190
        + intensidade ** 2 * 55,
        0, 255
    )

    imagem = np.stack(
        [vermelho, verde, azul],
        axis=-1
    ).astype(np.uint8)

    # ======================================
    # SOMBRA DO BURACO NEGRO
    # ======================================

    sombra = raio_tela < RAIO_SOMBRA

    imagem[sombra] = (2, 0, 7)

    # NumPy trabalha com altura x largura,
    # enquanto o Pygame usa largura x altura.
    return np.transpose(imagem, (1, 0, 2))


# ==========================================
# LOOP PRINCIPAL
# ==========================================

executando = True

while executando:

    dt = min(
        relogio.tick(FPS) / 1000,
        0.05
    )

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:
                executando = False

            if evento.key == pygame.K_SPACE:
                pausado = not pausado

            if evento.key == pygame.K_r:
                inclinacao = 0.34
                velocidade = 1.0

            if evento.key == pygame.K_UP:
                inclinacao = min(
                    0.9, inclinacao + 0.05
                )

            if evento.key == pygame.K_DOWN:
                inclinacao = max(
                    0.12, inclinacao - 0.05
                )

            if evento.key == pygame.K_RIGHT:
                velocidade = min(
                    4.0, velocidade + 0.25
                )

            if evento.key == pygame.K_LEFT:
                velocidade = max(
                    0.0, velocidade - 0.25
                )

    if not pausado:
        tempo += dt * velocidade

    tela.blit(fundo, (0, 0))

    pixels = criar_plasma(
        tempo, inclinacao
    )

    superficie = pygame.surfarray.make_surface(
        pixels
    )

    superficie = pygame.transform.smoothscale(
        superficie,
        (LARGURA, ALTURA)
    )

    # O preto do plasma fica transparente
    # para preservar as estrelas.
    superficie.set_colorkey((0, 0, 0))

    tela.blit(superficie, (0, 0))

    # Sombra central nítida
    pygame.draw.circle(
        tela,
        (2, 0, 7),
        (CX, CY),
        RAIO_SOMBRA
    )

    pygame.display.flip()

pygame.quit()
