import time
import random

w = 3
velocities = [(x, y) for x in range(-w, w) for y in range(-w, w)]
loops = 10000000


print (velocities)
# random_v = [(random.randint(-2, 2), random.randint(-2, 2)) for _ in range(8)]

start_time = time.time()
for _ in range(loops):
    v = random.choice(velocities)

end_time = time.time()
print(f"random.choice time: {end_time - start_time}")

start_time = time.time()
for _ in range(loops):
    v = (random.randint(-w, w), random.randint(-w, w))

end_time = time.time()
print(f"random.randint time: {end_time - start_time}")



