"""Pixel-art sprites for a minimalist, original-style Tamagotchi.

Every sprite is a grid of text: '#' is a dark pixel, '.' is an empty pixel.
The body is a solid blob and the face is carved out of it, like an LCD toy.
"""
from rich.text import Text

W = 14        # sprite width in pixels
HEIGHT = 16   # canvas height in pixels (must be even)
ZOOM = 1      # 1 = compact (half-blocks), 2 = big (square 2-char blocks)

LCD_FG = "#1f2a1f"
SOLID = "#" * W
BIG_EYES = "##..######..##"

# --- body (13 rows total: 4 top + 5 face + 4 bottom) ---
TOP = [
    "....######....",
    "..##########..",
    ".############.",
    SOLID,
]
BOTTOM = [
    SOLID,
    ".############.",
    "..##########..",
    "...########...",
]

# --- faces: 5 rows each, drawn over the middle of the body ---
CONTENT = [
    "##..######..##",
    "##..######..##",
    SOLID,
    SOLID,
    "######..######",
]
HAPPY = [
    "####.####.####",
    "###.#.##.#.###",
    SOLID,
    "####.####.####",
    "#####....#####",
]
EXCITED = [
    "####.####.####",
    "###.#.##.#.###",
    SOLID,
    "####......####",
    "#####....#####",
]
HUNGRY = [
    "###..####..###",
    "###..####..###",
    SOLID,
    "######..######",
    "######..######",
]
SLEEPY = [
    SOLID,
    "###..####..###",
    SOLID,
    SOLID,
    "######..######",
]
SLEEPING_A = [
    SOLID,
    "##...####...##",
    SOLID,
    SOLID,
    SOLID,
]
SLEEPING_B = [
    SOLID,
    "##...####...##",
    SOLID,
    SOLID,
    "######..######",
]
SAD = [
    "###..####..###",
    "####.####.####",
    SOLID,
    "#####....#####",
    "####.####.####",
]
DEAD = [
    "###.#.##.#.###",
    "####.####.####",
    "###.#.##.#.###",
    SOLID,
    "#####....#####",
]

# --- action faces (clearly different from the mood faces) ---
PLAY_A = [
    BIG_EYES,
    BIG_EYES,
    SOLID,
    "###........###",
    "####......####",
]
EAT_OPEN = [
    "####.####.####",
    "###.#.##.#.###",
    SOLID,
    "###........###",
    "####......####",
]
EAT_CLOSED = [
    "####.####.####",
    "###.#.##.#.###",
    SOLID,
    SOLID,
    "######..######",
]

# Each expression is a list of animation variants (cycled by frame number).
FACES = {
    "content": [CONTENT],
    "happy": [HAPPY],
    "hungry": [HUNGRY],
    "sleepy": [SLEEPY],
    "sad": [SAD],
    "dead": [DEAD],
    "eating": [EAT_OPEN, EAT_CLOSED],
    "playing": [PLAY_A, EXCITED],
    "sleeping": [SLEEPING_A, SLEEPING_B],
}

# Small icons shown above the pet during an action (cycled by frame)
EFFECTS = {
    "eating": ["  . o .  ", " o . o . "],
    "playing": ["♪       ", "    ♫   ", "  ♪   ♫ "],
    "sleeping": ["z", "z Z", "z Z z"],
}


def build_grid(face: list[str], bob: int) -> list[str]:
    """Stack top + face + bottom, shifted down by `bob` pixels, onto the canvas."""
    blank = "." * W
    rows = [blank] * (1 + bob) + TOP + face + BOTTOM
    rows += [blank] * (HEIGHT - len(rows))
    return rows


def render_sprite(expression: str, frame: int = 0) -> Text:
    variants = FACES[expression]
    face = variants[frame % len(variants)]
    bob = 0 if expression == "dead" else frame % 2
    rows = build_grid(face, bob)

    if ZOOM == 1:
        # Half-blocks: one character holds two vertical pixels (square pixels).
        lines = []
        for y in range(0, HEIGHT, 2):
            line = ""
            for x in range(W):
                top = rows[y][x] == "#"
                bottom = rows[y + 1][x] == "#"
                if top and bottom:
                    line += "█"
                elif top:
                    line += "▀"
                elif bottom:
                    line += "▄"
                else:
                    line += " "
            lines.append(line)
    else:
        # Each pixel is two full-block characters wide (square, but taller output).
        lines = ["".join("██" if c == "#" else "  " for c in row) for row in rows]

    return Text("\n".join(lines), style=LCD_FG)


if __name__ == "__main__":
    # Preview every expression: python -m termagotchi.sprites
    from rich.console import Console

    console = Console()
    for name in FACES:
        console.print(f"[bold]{name}[/bold]")
        console.print(render_sprite(name, 0))