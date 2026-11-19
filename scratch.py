from termagotchi.pet import Pet

p = Pet()
for _ in range(10):
    p.tick()
print(p)
print(p.mood)
print(p.feed())
print(p)