from termagotchi.sprites import BOTTOM, EFFECTS, FACES, TOP, W, render_sprite


def test_faces_are_well_formed():
    for name, variants in FACES.items():
        for face in variants:
            assert len(face) == 5, name
            for row in face:
                assert len(row) == W, f"{name}: bad width in {row!r}"
                assert set(row) <= {"#", "."}, name


def test_body_parts_have_correct_width():
    for row in TOP + BOTTOM:
        assert len(row) == W


def test_render_every_expression():
    for name in FACES:
        for frame in range(4):
            assert render_sprite(name, frame).plain


def test_every_pet_mood_has_a_face():
    for mood in ["happy", "content", "hungry", "sleepy", "sad", "dead"]:
        assert mood in FACES


def test_effects_match_expressions():
    for name in EFFECTS:
        assert name in FACES