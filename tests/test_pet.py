from termagotchi.pet import Pet


def test_tick_decays_stats():
    p = Pet()
    p.tick()
    assert p.age == 1
    assert p.hunger == 23
    assert p.energy == 78
    assert p.happiness == 68


def test_feed_reduces_hunger_and_clamps():
    p = Pet(hunger=10)
    p.feed()
    assert p.hunger == 0  # clamped, not negative


def test_play_when_too_tired_is_refused():
    p = Pet(energy=10)
    msg = p.play()
    assert "too tired" in msg
    assert p.energy == 10  # unchanged


def test_pet_dies_when_starving():
    p = Pet(hunger=98)
    p.tick()
    assert p.alive is False
    assert p.mood == "dead"


def test_dead_pet_ignores_actions():
    p = Pet(alive=False)
    p.feed()
    assert p.hunger == 20


def test_mood_hungry():
    assert Pet(hunger=80).mood == "hungry"