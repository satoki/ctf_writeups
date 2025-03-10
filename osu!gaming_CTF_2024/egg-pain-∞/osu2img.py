from PIL import Image, ImageDraw


def parse_osu_file(file_path):
    hit_objects = []
    with open(file_path, "r", encoding="utf-8") as file:
        hit_objects_section = False
        for line in file:
            if line.startswith("[HitObjects]"):
                hit_objects_section = True
            elif hit_objects_section:
                if line.strip() == "":
                    break
                parts = line.split(",")
                if len(parts) >= 3:
                    x, y = int(parts[0]), int(parts[1])
                    hit_objects.append((x, y))
    return hit_objects


def draw_beatmap_trace(hit_objects, image_size=(512, 384)):
    img = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(img)

    for x, y in hit_objects:
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill="black")

    return img


file_path = "ParagonX9 - Chaoz Fantasy (sahuang) [egg pain ∞].osu"
hit_objects = parse_osu_file(file_path)
img = draw_beatmap_trace(hit_objects)
img.save("beatmap_trace.png")
