from dataclasses import dataclass


def _clamp(value: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, value))


@dataclass
class Pet:
    """A pet's state. Pure logic: no I/O, no LLM, easy to test."""

    name: str = "Tama"
    hunger: int = 20      # 0 = full, 100 = starving
    energy: int = 80      # 0 = exhausted, 100 = fully rested
    happiness: int = 70   # 0 = miserable, 100 = ecstatic
    age: int = 0          # in ticks
    alive: bool = True

    # --- time ---
    def tick(self) -> None:
        """Advance time by one step: stats decay."""
        if not self.alive:
            return
        self.age += 1
        self.hunger = _clamp(self.hunger + 3)
        self.energy = _clamp(self.energy - 2)
        self.happiness = _clamp(self.happiness - 2)
        if self.hunger >= 100:
            self.alive = False

    # --- actions (each returns a message describing what happened) ---
    def feed(self) -> str:
        if not self.alive:
            return f"{self.name} is no longer with us."
        self.hunger = _clamp(self.hunger - 30)
        self.happiness = _clamp(self.happiness + 5)
        return f"{self.name} munches happily."

    def play(self) -> str:
        if not self.alive:
            return f"{self.name} is no longer with us."
        if self.energy < 15:
            return f"{self.name} is too tired to play."
        self.happiness = _clamp(self.happiness + 20)
        self.energy = _clamp(self.energy - 15)
        self.hunger = _clamp(self.hunger + 10)
        return f"{self.name} bounces around!"

    def sleep(self) -> str:
        if not self.alive:
            return f"{self.name} is no longer with us."
        self.energy = _clamp(self.energy + 40)
        self.hunger = _clamp(self.hunger + 10)
        return f"{self.name} takes a nap. Zzz..."

    # --- derived state ---
    @property
    def mood(self) -> str:
        if not self.alive:
            return "dead"
        if self.hunger > 70:
            return "hungry"
        if self.energy < 25:
            return "sleepy"
        if self.happiness < 30:
            return "sad"
        if self.happiness > 70:
            return "happy"
        return "content"