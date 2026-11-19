from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

from termagotchi.pet import Pet

VERSION = "v3"

# Each state has 2 faces that alternate, so the pet looks alive
FACES = {
    "happy": ["😄", "😊"],
    "content": ["🙂", "😌"],
    "hungry": ["🥺", "😩"],
    "sleepy": ["😪", "🥱"],
    "sad": ["😢", "😭"],
    "dead": ["💀", "👻"],
    "eating": ["😋", "🤤"],
    "playing": ["🥳", "🤩"],
    "sleeping": ["😴", "😴"],
}

# Icons shown around the face
ICONS = {
    "happy": "✨ 💖 ✨",
    "content": "🌱 🌱 🌱",
    "hungry": "🍽 ❓ 🍽",
    "sleepy": "💭 💭 💭",
    "sad": "💧 💧 💧",
    "dead": "🪦 🪦 🪦",
    "eating": "🍖 🍎 🍖",
    "playing": "🎾 ⚽ 🎾",
    "sleeping": "💤 🌙 💤",
}

ACTION_EXPRESSION = {"feed": "eating", "play": "playing", "sleep": "sleeping"}
REACTION_TICKS = 5  # 5 ticks x 0.5s = 2.5 seconds


def hearts(value: int, total: int = 4) -> str:
    n = round(value / 100 * total)
    return "♥" * n + "♡" * (total - n)


class TermagotchiApp(App):
    TITLE = f"Termagotchi {VERSION}"
    BINDINGS = [
        ("a", "do('feed')", "Feed"),
        ("b", "do('play')", "Play"),
        ("c", "do('sleep')", "Sleep"),
        ("r", "restart", "Restart"),
        ("x", "quit_app", "Quit"),
        ("escape", "quit_app", "Quit"),
    ]

    CSS = """
    Screen {
        align: center middle;
    }
    #device {
        width: 44;
        height: auto;
        padding: 0 2;
        background: #e46a8d;
        border: round #b8456a;
    }
    #lcd {
        width: 100%;
        height: auto;
        background: #9ead86;
        border: heavy #4a5a3a;
        color: #1f2a1f;
    }
    #lcd.active {
        background: #d6e6a8;
    }
    #icons {
        width: 100%;
        height: 1;
        content-align: center middle;
    }
    #face {
        width: 100%;
        height: 5;
        content-align: center middle;
    }
    #label, #status {
        width: 100%;
        height: 1;
        content-align: center middle;
    }
    #debug {
        width: 100%;
        height: 1;
        margin-top: 1;
        content-align: center middle;
        color: white;
    }
    #message {
        width: 100%;
        height: 1;
        content-align: center middle;
        color: white;
    }
    #buttons {
        width: 100%;
        height: auto;
        margin-top: 1;
        align: center middle;
    }
    Button {
        min-width: 8;
        margin: 0 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.pet = Pet()
        self.tick_count = 0
        self.override: str | None = None
        self.override_left = 0
        self.clicks = 0
        self.last_action = "-"
        self.msg = "Say hi!"

    def compose(self) -> ComposeResult:
        with Vertical(id="device"):
            with Vertical(id="lcd"):
                yield Static("", id="icons")
                yield Static("", id="face")
                yield Static("", id="label")
                yield Static("", id="status")
            yield Static("", id="message")
            yield Static("", id="debug")
            with Horizontal(id="buttons"):
                yield Button("🍖 Feed", id="feed")
                yield Button("🎾 Play", id="play")
                yield Button("💤 Sleep", id="sleep")
                yield Button("Quit", id="quit")

    def on_mount(self) -> None:
        self.set_interval(0.5, self.animate)
        self.set_interval(5, self.decay)
        self.refresh_view()

    def animate(self) -> None:
        self.tick_count += 1
        if self.override is not None:
            self.override_left -= 1
            if self.override_left <= 0:
                self.override = None
        self.refresh_view()

    def decay(self) -> None:
        self.pet.tick()
        self.refresh_view()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()
        if event.button.id == "quit":
            self.exit()
        else:
            self.action_do(event.button.id)

    def action_quit_app(self) -> None:
        self.exit()

    def action_do(self, name: str) -> None:
        self.clicks += 1
        self.last_action = name
        message = getattr(self.pet, name)()  # pet.feed() / play() / sleep()

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
        self.refresh_view()

    def action_restart(self) -> None:
        self.pet = Pet()
        self.override = None
        self.msg = "A new egg hatches!"
        self.refresh_view()

    def refresh_view(self) -> None:
        p = self.pet
        state = self.override or p.mood
        faces = FACES[state]
        face = faces[self.tick_count % len(faces)]

        self.query_one("#lcd").set_class(self.override is not None, "active")
        self.query_one("#icons", Static).update(ICONS[state])
        self.query_one("#face", Static).update(f"\n{face}")
        self.query_one("#label", Static).update(state.upper())
        self.query_one("#status", Static).update(
            f"HUNGER {hearts(100 - p.hunger)}  HAPPY {hearts(p.happiness)}"
        )
        self.query_one("#message", Static).update(self.msg)
        self.query_one("#debug", Static).update(
            f"{VERSION} | actions: {self.clicks} | last: {self.last_action}"
        )