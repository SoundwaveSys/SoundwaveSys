from PIL import Image
import math

# ==========================================
# SETTINGS
# ==========================================

WIDTH = 1200
HEIGHT = 200

FRAMES = 60
DURATION = 80  # milliseconds per frame

OCEAN_FILE = "ocean.png"
SHIP_FILE = "going-merry.png"
OUTPUT_FILE = "ship-ocean.gif"


# ==========================================
# LOAD OCEAN
# ==========================================

ocean = Image.open(OCEAN_FILE).convert("RGBA")

# Keep the original aspect ratio
if ocean.width != WIDTH:
    new_height = int(ocean.height * WIDTH / ocean.width)

    ocean = ocean.resize(
        (WIDTH, new_height),
        Image.Resampling.LANCZOS
    )

# Crop to exactly 1200 x 200
if ocean.height >= HEIGHT:

    top_crop = (ocean.height - HEIGHT) // 2

    ocean = ocean.crop(
        (
            0,
            top_crop,
            WIDTH,
            top_crop + HEIGHT
        )
    )

else:

    # Fallback if ocean is smaller than required
    ocean = ocean.resize(
        (WIDTH, HEIGHT),
        Image.Resampling.LANCZOS
    )


# ==========================================
# LOAD SHIP
# ==========================================

ship = Image.open(SHIP_FILE).convert("RGBA")

# ------------------------------------------
# SHIP SIZE
# ------------------------------------------

SHIP_WIDTH = 240

scale = SHIP_WIDTH / ship.width

SHIP_HEIGHT = int(
    ship.height * scale
)

ship = ship.resize(
    (SHIP_WIDTH, SHIP_HEIGHT),
    Image.Resampling.LANCZOS
)


# ==========================================
# CREATE RGBA FRAMES
# ==========================================

frames = []


for i in range(FRAMES):

    # --------------------------------------
    # Transparent ocean canvas
    # --------------------------------------

    frame = ocean.copy()

    # --------------------------------------
    # Animation progress
    # --------------------------------------

    progress = i / (FRAMES - 1)

    angle = progress * math.pi * 2


    # ======================================
    # SHIP MOVEMENT
    # ======================================

    start_x = -SHIP_WIDTH

    end_x = WIDTH + 20

    x_movement = (
        start_x
        + (end_x - start_x) * progress
    )


    # ======================================
    # WAVE MOVEMENT
    # ======================================

    vertical_movement = (
        math.sin(angle * 3) * 5
    )


    # ======================================
    # SHIP ROCKING
    # ======================================

    rotation = (
        math.sin(angle * 2) * 2
    )


    moving_ship = ship.rotate(
        rotation,
        resample=Image.Resampling.BICUBIC,
        expand=True
    )


    # ======================================
    # SHIP POSITION
    # ======================================

    x = int(
        x_movement
        - (moving_ship.width - ship.width) / 2
    )

    # Position ship on the waves
    y = int(
        HEIGHT
        - moving_ship.height
        - 30
        + vertical_movement
    )


    # ======================================
    # PLACE SHIP
    # ======================================

    frame.alpha_composite(
        moving_ship,
        (x, y)
    )


    # ======================================
    # KEEP RGBA
    # ======================================

    frames.append(frame)


# ==========================================
# CONVERT RGBA → TRANSPARENT GIF FRAME
# ==========================================

def rgba_to_transparent_gif(frame):

    # --------------------------------------
    # Separate RGB and Alpha
    # --------------------------------------

    rgb = Image.new(
        "RGB",
        frame.size,
        (0, 0, 0)
    )

    rgb.paste(
        frame,
        mask=frame.getchannel("A")
    )


    # --------------------------------------
    # Quantize using 254 colors
    #
    # Palette index 0 will be reserved
    # exclusively for transparency.
    # --------------------------------------

    quantized = rgb.quantize(
        colors=254,
        method=Image.Quantize.MEDIANCUT
    )


    # --------------------------------------
    # Shift all normal colors by +1
    #
    # 0 = transparency
    # 1-254 = actual colors
    # --------------------------------------

    indexed = quantized.point(
        lambda p: p + 1
    )


    # --------------------------------------
    # Build palette
    # --------------------------------------

    old_palette = quantized.getpalette()

    new_palette = [
        0, 0, 0
    ]

    new_palette.extend(
        old_palette[:254 * 3]
    )


    # GIF palettes must contain 256 colors
    while len(new_palette) < 768:
        new_palette.extend([0, 0, 0])


    indexed.putpalette(new_palette)


    # --------------------------------------
    # Make transparent pixels index 0
    # --------------------------------------

    alpha = frame.getchannel("A")

    transparent_mask = alpha.point(
        lambda a: 255 if a == 0 else 0
    )

    indexed.paste(
        0,
        mask=transparent_mask
    )


    return indexed


# ==========================================
# CONVERT ALL FRAMES
# ==========================================

gif_frames = []

for frame in frames:

    gif_frame = rgba_to_transparent_gif(frame)

    gif_frames.append(gif_frame)


# ==========================================
# SAVE TRANSPARENT GIF
# ==========================================

gif_frames[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=gif_frames[1:],
    duration=DURATION,
    loop=0,
    optimize=False,
    transparency=0,
    disposal=2
)


# ==========================================
# DONE
# ==========================================

print()
print("==========================================")
print("       TRANSPARENT SHIP GIF CREATED")
print("==========================================")
print(f"File   : {OUTPUT_FILE}")
print(f"Size   : {WIDTH} x {HEIGHT}")
print(f"Frames : {FRAMES}")
print(f"Speed  : {DURATION} ms")
print("Transparency : ENABLED")
print("==========================================")