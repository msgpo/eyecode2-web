import argparse
from PIL import Image, ImageFont, ImageDraw

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program_path")
    parser.add_argument("image_path")
    parser.add_argument("--width", type=int, default=710)
    parser.add_argument("--height", type=int, default=700)
    parser.add_argument("--fontsize", type=int, default=19)
    parser.add_argument("--xoffset", type=int, default=0)
    parser.add_argument("--yoffset", type=int, default=0)
    parser.add_argument("--lineoffset", type=int, default=2)
    parser.add_argument("--baseimage", type=str, default="")
    parser.add_argument("--header", type=str, default="")
    args = parser.parse_args()

    program_lines = [line.rstrip() for line in open(args.program_path, "r") if not line.strip().startswith("#")]

    white = (255, 255, 255)
    black = (0, 0, 0)

    image = Image.new("RGBA", (args.width, args.height), white)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/CONSOLA.TTF", args.fontsize)

    y_offset = args.yoffset
    line_height = args.fontsize + args.lineoffset
    header = False
    
    if len(args.header) > 0:
        program_lines = [args.header] + program_lines
        header = True

    for line in program_lines:
        if line.strip():
            if header:
                draw.rectangle([(0, 0), (args.width, line_height - 2)], fill=black)
                size = draw.textsize(line, font=font)
                draw.text(((args.width / 2) - (size[0] / 2), y_offset), line, white, font=font)
                header = False
            else:
                draw.text((args.xoffset, y_offset), line, black, font=font)
            
        y_offset += line_height

    if len(args.baseimage) == 0:
        image.save(args.image_path)
    else:
        base_image = Image.open(args.baseimage)
        base_image.paste(image, (0, 0))
        base_image.save(args.image_path)
