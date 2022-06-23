from PIL import Image, ImageDraw

UNIT = 50
FRAME_LENGTH = 20
BG = "#ffffff"

def build(plan, dest, D, i_pos):
    base = draw_grid(D)

    imgs = [base] * 10

    x = i_pos[0]
    y = i_pos[1]

    for p in [str(x) for x in plan]:
        new_img = base.copy()
        draw = ImageDraw.Draw(new_img)

        x1 = UNIT * x + 3
        y1 = UNIT * y + 3
        x2 = UNIT * x + UNIT - 2
        y2 = UNIT * y + UNIT - 2

        draw.rectangle([x1, y1, x2, y2], fill="#aa3333")

        imgs += [new_img] * 5
    
        match p:
            case "right":
                x += 1
            case "left":
                x -= 1
            case "up":
                y -= 1
            case "down":
                y += 1

    gif = imgs[0].save(dest, save_all=True, 
            append_images=imgs[1:], 
            duration=len(plan) * FRAME_LENGTH)

def draw_grid(d):
    img = Image.new("RGB", (UNIT * d, UNIT * d), BG)
    draw = ImageDraw.Draw(img)

    for i in range(d):
        x = i * UNIT
        y = i * UNIT

        draw.line([0, y, d*UNIT, y], fill="#000000", width=2)
        draw.line([x, 0, x, d*UNIT], fill="#000000", width=2)
    
    return img


