import tkinter as tk

from termagotchi.pet import Pet
from termagotchi.sprites import EFFECTS, FACES, W, build_grid

PIXEL = 20                  # size of one sprite pixel on screen (was 12)
CANVAS_W, CANVAS_H = 340, 440
LCD_BG = "#9ead86"
LCD_ACTIVE = "#d6e6a8"      # LCD lightens while the pet reacts
LCD_FG = "#1f2a1f"
BODY = "#e46a8d"

ACTION_EXPRESSION = {"feed": "eating", "play": "playing", "sleep": "sleeping"}
REACTION_TICKS = 5          # 5 ticks x 0.5 s = 2.5 s


def hearts(value: int, total: int = 4) -> str:
    n = round(value / 100 * total)
    return "♥" * n + "♡" * (total - n)


class TermagotchiGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Termagotchi")
        root.configure(bg=BODY)
        root.resizable(False, False)

        self.pet = Pet()
        self.tick_count = 0
        self.override: str | None = None
        self.override_left = 0
        self.clicks = 0
        self.last_action = "-"
        self.msg = "Say hi!"

        # --- LCD screen ---
        self.canvas = tk.Canvas(
            root, width=CANVAS_W, height=CANVAS_H, bg=LCD_BG,
            highlightthickness=6, highlightbackground="#4a5a3a",
        )
        self.canvas.pack(padx=20, pady=(20, 8))

        # --- message + debug lines ---
        self.msg_var = tk.StringVar()
        self.debug_var = tk.StringVar()
        tk.Label(root, textvariable=self.msg_var, bg=BODY, fg="white",
                 font=("Consolas", 11, "bold")).pack()
        tk.Label(root, textvariable=self.debug_var, bg=BODY, fg="#ffd6e0",
                 font=("Consolas", 9)).pack()

        # --- buttons ---
        row = tk.Frame(root, bg=BODY)
        row.pack(pady=(8, 20))
        for label, cmd in [
            ("A  Feed", lambda: self.do("feed")),
            ("B  Play", lambda: self.do("play")),
            ("C  Sleep", lambda: self.do("sleep")),
            ("Quit", root.destroy),
        ]:
            tk.Button(row, text=label, width=9, command=cmd,
                      font=("Consolas", 10, "bold")).pack(side="left", padx=4)

        # --- keyboard shortcuts (no Ctrl, so no VS Code conflicts) ---
        root.bind("a", lambda e: self.do("feed"))
        root.bind("b", lambda e: self.do("play"))
        root.bind("c", lambda e: self.do("sleep"))
        root.bind("r", lambda e: self.restart())
        root.bind("<Escape>", lambda e: root.destroy())

        # --- clocks ---
        self.redraw()
        root.after(500, self.animate)
        root.after(5000, self.decay)

    # ---------- clocks ----------
    def animate(self) -> None:
        self.tick_count += 1
        if self.override is not None:
            self.override_left -= 1
            if self.override_left <= 0:
                self.override = None
        self.redraw()
        self.root.after(500, self.animate)

    def decay(self) -> None:
        self.pet.tick()
        self.redraw()
        self.root.after(5000, self.decay)

    # ---------- actions ----------
    def do(self, name: str) -> None:
        self.clicks += 1
        self.last_action = name
        message = getattr(self.pet, name)()   # pet.feed() / play() / sleep()

        if not self.pet.alive:
            self.override = None
        elif "too tired" in message:
            self.override = "sad"
            self.override_left = REACTION_TICKS
        else:
            self.override = ACTION_EXPRESSION[name]
            self.override_left = REACTION_TICKS

        self.tick_count = 0
        self.msg = message
        self.redraw()

    def restart(self) -> None:
        self.pet = Pet()
        self.override = None
        self.msg = "A new egg hatches!"
        self.redraw()

    # ---------- drawing ----------
    def redraw(self) -> None:
        p = self.pet
        expression = self.override or p.mood
        c = self.canvas

        c.delete("all")
        c.configure(bg=LCD_ACTIVE if self.override else LCD_BG)

        # effect icons above the pet
        effects = EFFECTS.get(self.override)
        if effects:
            c.create_text(CANVAS_W // 2, 20, text=effects[self.tick_count % len(effects)],
                          font=("Consolas", 18, "bold"), fill=LCD_FG)

        # pixel sprite
        variants = FACES[expression]
        face = variants[self.tick_count % len(variants)]
        bob = 0 if expression == "dead" else self.tick_count % 2
        grid = build_grid(face, bob)
        x0 = (CANVAS_W - W * PIXEL) // 2
        y0 = 40
        for y, row in enumerate(grid):
            for x, ch in enumerate(row):
                if ch == "#":
                    c.create_rectangle(
                        x0 + x * PIXEL, y0 + y * PIXEL,
                        x0 + (x + 1) * PIXEL, y0 + (y + 1) * PIXEL,
                        fill=LCD_FG, outline=LCD_FG,
                    )

        # expression name + hearts
        c.create_text(CANVAS_W // 2, 386, text=expression.upper(),
                      font=("Consolas", 12, "bold"), fill=LCD_FG)
        c.create_text(
            CANVAS_W // 2, 412,
            text=f"HUNGER {hearts(100 - p.hunger)}  HAPPY {hearts(p.happiness)}",
            font=("Consolas", 11, "bold"), fill=LCD_FG,
        )

        self.msg_var.set(self.msg)
        self.debug_var.set(f"clicks: {self.clicks} | last: {self.last_action}")


def main() -> None:
    root = tk.Tk()
    TermagotchiGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()