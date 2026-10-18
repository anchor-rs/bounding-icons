import io
from dataclasses import dataclass
from pathlib import Path

import resvg_py
from PIL import Image

SVG_PATH = Path("bbox.svg")
NAME = "bbox"
OUTPUT_PATH = Path("pack")

SIZES: list[int] = [16, 24, 32, 48, 64, 128, 256]
FORMATS: list[str] = ["png", "ico"]

@dataclass
class Pack:
    name: str
    color: str

@dataclass
class Item:
    image: Image.Image
    size: int

PACKS: list[Pack] = [
    Pack("blue", "#2F7BF5"),
    Pack("orange", "#E7573D"),
    Pack("violet", "#8A5CF6"),
    Pack("yellow", "#F3A617"),
    Pack("menthol", "#11A58A"),
    Pack("pink", "#E03690"),
    Pack("pear", "#7AB51B"),
]

def render(svg_text: str, size: int) -> Item:
    png = resvg_py.svg_to_bytes(svg_string=svg_text, width=size, height=size)
    img = Image.open(io.BytesIO(png)).convert("RGBA")
    return Item(image=img, size=size)

def save_items(items: list[Item], path: Path, format: str):
    path.mkdir(parents=True, exist_ok=True)

    for item in items:
        item.image.save(
            path / f"{NAME}-{item.size}.{format}",
            format=format.upper(),
            sizes=[(item.size, item.size)]
        )

def save_items_bytes(items: list[Item], path: Path):
    path.mkdir(parents=True, exist_ok=True)

    for item in items:
        (path / f"{NAME}-{item.size}.rgba").write_bytes(item.image.tobytes())

def set_color(svg_text: str, color: str) -> str:
    return svg_text.replace("currentColor", color)

def main():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    with open(SVG_PATH, "r") as f:
        svg_text = f.read()

    for pack in PACKS:
        colored_svg = set_color(svg_text, pack.color)

        Path(OUTPUT_PATH / pack.name).mkdir(parents=True, exist_ok=True)

        with open(f"{OUTPUT_PATH / pack.name / NAME}-64.svg", "w") as f:
            f.write(colored_svg)

        items = [render(colored_svg, size) for size in SIZES]

        for format in FORMATS:
            save_items(items, OUTPUT_PATH / pack.name / format, format)

        save_items_bytes(items, OUTPUT_PATH / pack.name / "bytes")


if __name__ == "__main__":
    main()