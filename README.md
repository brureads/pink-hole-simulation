
# Pink Hole Simulation

Uma simulação visual e interativa de um buraco negro rosa, desenvolvida em Python com Pygame CE.

O projeto utiliza milhares de partículas em movimento para representar artisticamente um disco de acreção, com efeitos de brilho, plasma e lente gravitacional.

## Sobre o projeto

O Pink Hole Simulation nasceu da ideia de transformar um fenômeno fascinante do universo em uma experiência visual interativa.

A versão 6.8, **Soft Plasma**, apresenta:

- 14.000 partículas no disco externo.
- 4.000 partículas na região interna.
- Arco luminoso inspirado no efeito de lente gravitacional.
- Efeito de brilho difuso (bloom).
- Movimento orbital animado.
- Controles interativos pelo teclado.
- Paleta de cores em rosa e magenta.

> Esta é uma representação artística, não uma simulação física precisa de um buraco negro.

## Tecnologias utilizadas

- **Python:** linguagem de programação principal.
- **Pygame CE:** biblioteca para criar a janela, desenhar partículas e executar animações.
- **Git:** controle de versões do projeto.
- **GitHub:** hospedagem do código-fonte.

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/brureads/pink-hole-simulation.git
```

### 2. Entre na pasta

```bash
cd pink-hole-simulation
```

### 3. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Execute a simulação

```bash
python main.py
```

## Controles

| Tecla | Função |
|---|---|
| Seta para cima | Aumentar a inclinação do disco |
| Seta para baixo | Diminuir a inclinação do disco |
| Seta para direita | Aumentar a velocidade |
| Seta para esquerda | Diminuir a velocidade |
| Espaço | Pausar ou continuar |
| R | Restaurar configurações |
| Esc | Fechar a simulação |

## Conceitos explorados

Durante o desenvolvimento, foram utilizados conceitos de:

- Programação em Python.
- Laços de repetição e funções.
- Trigonometria para calcular órbitas.
- Animação baseada em tempo (delta time).
- Transparência e composição de camadas.
- Renderização de partículas e efeitos luminosos.
- Versionamento com Git.

## Versão atual

**Pink Hole 6.8 — Soft Plasma**

## Autoria

Desenvolvido por Bruna Martins Moura.

GitHub: [@brureads](https://github.com/brureads)
