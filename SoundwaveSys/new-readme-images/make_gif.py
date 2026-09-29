from PIL import Image
import math

# ==========================================
# SETTINGS
# ==========================================

WIDTH = 1200
HEIGHT = 300

FRAMES = 40
DURATION = 80  # milliseconds per frame

OCEAN_FILE = "ocean.png"
SHIP_FILE = "going-merry.png"
OUTPUT_FILE = "ship-ocean.gif"


# ==========================================
# LOAD OCEAN
# ==========================================

ocean = Image.open(OCEAN_FILE).convert("RGBA")

ocean = ocean.resize(
    (WIDTH, HEIGHT),
    Image.Resampling.LANCZOS
)


# ==========================================
# LOAD SHIP
# ==========================================

ship = Image.open(SHIP_FILE).convert("RGBA")

# Ship width
SHIP_WIDTH = 320

scale = SHIP_WIDTH / ship.width
SHIP_HEIGHT = int(ship.height * scale)

ship = ship.resize(
    (SHIP_WIDTH, SHIP_HEIGHT),
    Image.Resampling.LANCZOS
)


# ==========================================
# CREATE ANIMATION
# ==========================================

frames = []

for i in range(FRAMES):

    frame = ocean.copy()

    # --------------------------------------
    # Smooth sailing movement
    # --------------------------------------

    progress = i / FRAMES
    angle = progress * math.pi * 2

    # Small left/right movement
    horizontal_movement = math.sin(angle) * 12

    # Gentle up/down movement
    vertical_movement = math.sin(angle * 2) * 4

    # Slight rocking
    rotation = math.sin(angle) * 1.5

    # Rotate ship
    moving_ship = ship.rotate(
        rotation,
        resample=Image.Resampling.BICUBIC,
        expand=True
    )

    # --------------------------------------
    # Ship position
    # --------------------------------------

    x = int(
        WIDTH
        - moving_ship.width
        - 35
        + horizontal_movement
    )

    y = int(
        HEIGHT
        - moving_ship.height
        + vertical_movement
    )

    # --------------------------------------
    # Place ship
    # --------------------------------------

    frame.alpha_composite(
        moving_ship,
        (x, y)
    )

    frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE))


# ==========================================
# SAVE GIF
# ==========================================

frames[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=frames[1:],
    duration=DURATION,
    loop=0,
    optimize=True
)

print()
print("===================================")
print(" Ship + Ocean GIF created!")
print("===================================")
print(f"File   : {OUTPUT_FILE}")
print(f"Size   : {WIDTH} x {HEIGHT}")
print(f"Frames : {FRAMES}")
print(f"Speed  : {DURATION} ms")
print("===================================")