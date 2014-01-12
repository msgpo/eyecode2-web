import argparse, re
from PIL import Image, ImageFont, ImageDraw

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program_path")
    parser.add_argument("image_path")
    parser.add_argument("--width", type=int, default=670)
    parser.add_argument("--height", type=int, default=700)
    parser.add_argument("--fontsize", type=int, default=19)
    parser.add_argument("--xoffset", type=int, default=0)
    parser.add_argument("--yoffset", type=int, default=0)
    parser.add_argument("--lineoffset", type=int, default=2)
    parser.add_argument("--baseimage", type=str, default="")
    parser.add_argument("--header", type=str, default="")
    parser.add_argument("--line_colors", type=str, default=None)
    parser.add_argument("--bg_color", type=str, default=None)
    args = parser.parse_args()

    program_lines = [line.rstrip() for line in open(args.program_path, "r")]

    white  = (255, 255, 255)
    black  = (0, 0, 0)
    red    = (149, 26, 28)
    blue   = (1, 142, 169)
    green  = (29, 147, 23)
    color_map = { "w": white, "k": black, "r": red, "b": blue, "g": green }

    image = Image.new("RGBA", (args.width, args.height), white)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/CONSOLA.TTF", args.fontsize)

    if args.bg_color is not None:
        draw.rectangle([(0, 0), image.size], fill=args.bg_color)

    y_offset = args.yoffset
    line_height = args.fontsize + args.lineoffset
    header = False
    id_regex = re.compile("[a-zA-Z_]+|[+*=]")

    if len(args.header) > 0:
        program_lines = [args.header] + program_lines
        header = True

    line_colors = []
    if args.line_colors is not None:
        import ast
        line_colors = ast.literal_eval(args.line_colors)

    for line_idx, line in enumerate(program_lines):
        if line.strip():
            if header:
                draw.rectangle([(0, 0), (args.width, line_height - 2)], fill=black)
                size = draw.textsize(line, font=font)
                draw.text(((args.width / 2) - (size[0] / 2), y_offset), line, white, font=font)
                header = False
            else:
                text_color = black
                if line_idx < len(line_colors):
                    lc = line_colors[line_idx]
                    if len(lc) > 0:
                        #draw.rectangle([(0, y_offset), (args.width, y_offset + line_height - 1)], fill=lc)
                        text_color = lc

                draw.text((args.xoffset, y_offset), line, text_color, font=font)
            
        # Next line
        y_offset += line_height

    if len(args.baseimage) == 0:
        image.save(args.image_path)
    else:
        base_image = Image.open(args.baseimage)
        base_image.paste(image, (0, 0))
        base_image.save(args.image_path)
