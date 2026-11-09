
import pygame
import random
import math

pygame.init()

# ==========================================
# PINK HOLE 3.0 - COSMIC FLOW
# ==========================================

LARGURA = 1100
ALTURA = 700
FPS = 60

CX = LARGURA // 2
CY = ALTURA // 2

RAIO_SOMBRA = 65
RAIO_INTERNO = 88
RAIO_EXTERNO = 310

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pink Hole 3.0 | Cosmic Flow")
relogio = pygame.time.Clock()

random.seed(42)

# ==========================================
# ESTRELAS
# ==========================================

estrelas = []

for _ in range(230):
    estrelas.append((
        random.randrange(LARGURA),
        random.randrange(ALTURA),
        random.randint(55, 190),
        random.choice([1, 1, 1, 2])
    ))

# ==========================================
# PARTICULAS DO DISCO
# ==========================================

particulas = []

for _ in range(9000):
    raio = RAIO_INTERNO + (
        random.random() ** 1.25
    ) * (RAIO_EXTERNO - RAIO_INTERNO)

    particulas.append({
        "raio": raio,
        "angulo": random.uniform(0, math.tau),
        "velocidade": 0.014 * (120 / raio) ** 1.5,
        "altura": random.gauss(0, 3),
        "brilho": random.uniform(0.55, 1.0)
    })

# ==========================================
# FUNCOES DE COR
# ==========================================

def misturar(cor1, cor2, fator):
    fator = max(0, min(1, fator))

    return tuple(
        int(a + (b - a) * fator)
        for a, b in zip(cor1, cor2)
    )


def cor_disco(raio, brilho):
    t = (
        (raio - RAIO_INTERNO)
        / (RAIO_EXTERNO - RAIO_INTERNO)
    )

    if t < 0.35:
        cor = misturar(
            (255, 235, 250),
            (255, 105, 205),
            t / 0.35
        )
    else:
        cor = misturar(
            (255, 105, 205),
            (165, 20, 105),
            (t - 0.35) / 0.65
        )

    return tuple(int(c * brilho) for c in cor)


# ==========================================
# CAMADAS DE DESENHO
# ==========================================

fundo = pygame.Surface((LARGURA, ALTURA))
fundo.fill((0, 0, 0))

for x, y, brilho, tamanho in estrelas:
    pygame.draw.circle(
        fundo,
        (brilho, brilho, brilho),
        (x, y),
        tamanho
    )

disco_tras = pygame.Surface(
    (LARGURA, ALTURA), pygame.SRCALPHA
)

disco_frente = pygame.Surface(
    (LARGURA, ALTURA), pygame.SRCALPHA
)

lente = pygame.Surface(
    (LARGURA, ALTURA), pygame.SRCALPHA
)

# ==========================================
# LENTE GRAVITACIONAL ARTISTICA
# ==========================================

def desenhar_lente(superficie, tempo):

    # Faixas suaves, em vez de linhas finas.
    # A altura e maior no centro do arco.

    for lado in (-1, 1):
        for camada in range(36):

            largura_arco = 112 + camada * 2.2
            altura_arco = 72 + camada * 1.15

            pontos = []

            for passo in range(100):
                t = passo / 99
                nx = -1 + 2 * t

                curva = math.sqrt(
                    max(0, 1 - nx * nx)
                )

                x = CX + nx * largura_arco
                y = CY + lado * curva * altura_arco

                # Pequena oscilacao luminosa
                y += math.sin(
                    tempo * 0.7 + t * 8 + camada * 0.15
                ) * 0.6

                pontos.append((int(x), int(y)))

            intensidade = 1 - camada / 36

            cor = (
                255,
                int(65 + intensidade * 145),
                int(165 + intensidade * 80),
                int(5 + intensidade * 10)
            )

            pygame.draw.lines(
                superficie,
                cor,
                False,
                pontos,
                3
            )


# ==========================================
# DESENHA PARTICULAS
# ==========================================

def desenhar_particula(superficie, p, dt):

    p["angulo"] = (
        p["angulo"] + p["velocidade"] * dt * 60
    ) % math.tau

    angulo = p["angulo"]
    raio = p["raio"]

    x = CX + math.cos(angulo) * raio
    y = (
        CY
        + math.sin(angulo) * raio * 0.34
        + p["altura"]
    )

    cor = cor_disco(raio, p["brilho"])

    pos = (int(x), int(y))

    pygame.draw.circle(
        superficie,
        (*cor, 115),
        pos,
        1
    )

    # Trilha curta seguindo a orbita
    angulo_anterior = angulo - 0.018

    x2 = CX + math.cos(angulo_anterior) * raio
    y2 = (
        CY
        + math.sin(angulo_anterior) * raio * 0.34
        + p["altura"]
    )

    pygame.draw.line(
        superficie,
        (*cor, 70),
        (int(x2), int(y2)),
        pos,
        1
    )


# ==========================================
# SUAVIZACAO
# ==========================================

def aplicar_brilho(destino, camada):

    pequena = pygame.transform.smoothscale(
        camada,
        (LARGURA // 4, ALTURA // 4)
    )

    suave = pygame.transform.smoothscale(
        pequena,
        (LARGURA, ALTURA)
    )

    suave.set_alpha(95)

    destino.blit(
        suave,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_ADD
    )

    destino.blit(camada, (0, 0))


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

    tela.blit(fundo, (0, 0))

    disco_tras.fill((0, 0, 0, 0))
    disco_frente.fill((0, 0, 0, 0))
    lente.fill((0, 0, 0, 0))

    # Separa a metade traseira da frontal
    for p in particulas:
        if math.sin(p["angulo"]) < 0:
            desenhar_particula(disco_tras, p, dt)
        else:
            desenhar_particula(disco_frente, p, dt)

    # PARTE TRASEIRA
    aplicar_brilho(tela, disco_tras)

    # LENTE GRAVITACIONAL
    desenhar_lente(lente, tempo)
    aplicar_brilho(tela, lente)

    # SOMBRA DO BURACO NEGRO
    pygame.draw.circle(
        tela,
        (2, 0, 7),
        (CX, CY),
        RAIO_SOMBRA
    )

    # BORDA LUMINOSA SUAVE
    pygame.draw.circle(
        tela,
        (115, 30, 90),
        (CX, CY),
        RAIO_SOMBRA + 2,
        1
    )

    # PARTE FRONTAL
    aplicar_brilho(tela, disco_frente)

    pygame.display.flip()

pygame.quit()
