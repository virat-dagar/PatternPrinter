from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class PatternSpec:
    id: str
    name: str
    category: str
    shape: str
    description: str
    requires_rectangle: bool = False


def _solid_rectangle(symbol: str, width: int, height: int) -> list[str]:
    return [(symbol + " ") * width for _ in range(height)]


def _hollow_rectangle(symbol: str, width: int, height: int) -> list[str]:
    rows = []
    for row in range(height):
        line = []
        for col in range(width):
            line.append(symbol if row in (0, height - 1) or col in (0, width - 1) else " ")
        rows.append(" ".join(line))
    return rows


def _checkerboard_rectangle(symbol: str, width: int, height: int) -> list[str]:
    rows = []
    for row in range(height):
        line = []
        for col in range(width):
            line.append(symbol if (row + col) % 2 == 0 else " ")
        rows.append(" ".join(line))
    return rows


def _solid_square(symbol: str, size: int) -> list[str]:
    return [(symbol + " ") * size for _ in range(size)]


def _hollow_square(symbol: str, size: int) -> list[str]:
    return _hollow_rectangle(symbol, size, size)


def _right_triangle(symbol: str, size: int) -> list[str]:
    return [symbol * (row + 1) for row in range(size)]


def _right_triangle_hollow(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size):
        line = []
        for col in range(row + 1):
            line.append(symbol if row in (0, size - 1) or col in (0, row) else " ")
        rows.append("".join(line))
    return rows


def _right_triangle_reverse(symbol: str, size: int) -> list[str]:
    return [symbol * (size - row) for row in range(size)]


def _right_triangle_reverse_hollow(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size):
        line = []
        for col in range(row, size):
            line.append(symbol if row in (0, size - 1) or col in (row, size - 1) else " ")
        rows.append("".join(line))
    return rows


def _left_triangle(symbol: str, size: int) -> list[str]:
    return [" " * (size - row - 1) + symbol * (row + 1) for row in range(size)]


def _left_triangle_hollow(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size):
        line = [" "] * (size - row - 1)
        for col in range(row + 1):
            line.append(symbol if row == size - 1 or col in (0, row) else " ")
        rows.append("".join(line))
    return rows


def _left_triangle_reverse(symbol: str, size: int) -> list[str]:
    return [" " * row + symbol * (size - row) for row in range(size)]


def _left_triangle_reverse_hollow(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size):
        line = [" "] * row
        for col in range(row, size):
            line.append(symbol if row in (0, size - 1) or col in (row, size - 1) else " ")
        rows.append("".join(line))
    return rows


def _hill(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size):
        padding = " " * (size - row - 1)
        body = symbol * (row * 2 + 1)
        rows.append(padding + body)
    return rows


def _hill_hollow(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size):
        padding = " " * (size - row - 1)
        width = row * 2 + 1
        rows.append(padding + _edge_line(symbol, width, fill=row == size - 1))
    return rows


def _hill_reverse(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size):
        padding = " " * row
        body = symbol * ((size - row) * 2 - 1)
        rows.append(padding + body)
    return rows


def _hill_reverse_hollow(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size):
        padding = " " * row
        width = (size - row) * 2 - 1
        rows.append(padding + _edge_line(symbol, width, fill=row == 0))
    return rows


def _diamond(symbol: str, size: int) -> list[str]:
    top = _hill(symbol, size)
    bottom = [" " * row + symbol * ((size - row) * 2 - 1) for row in range(1, size)]
    return top + bottom


def _diamond_hollow(symbol: str, size: int) -> list[str]:
    rows = []
    total_rows = size * 2 - 1
    for row in range(total_rows):
        distance = abs(size - 1 - row)
        width = total_rows - distance * 2
        rows.append(" " * distance + _edge_line(symbol, width))
    return rows


def _half_diamond(symbol: str, size: int) -> list[str]:
    top = [symbol * row for row in range(1, size + 1)]
    bottom = [symbol * row for row in range(size - 1, 0, -1)]
    return top + bottom


def _mirrored_half_diamond(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(1, size + 1):
        rows.append(" " * (size - row) + symbol * row)
    for row in range(size - 1, 0, -1):
        rows.append(" " * (size - row) + symbol * row)
    return rows


def _hourglass(symbol: str, size: int) -> list[str]:
    top = _hill_reverse(symbol, size)
    bottom = _hill(symbol, size)[1:]
    return top + bottom


def _hourglass_hollow(symbol: str, size: int) -> list[str]:
    top = _hill_reverse_hollow(symbol, size)
    bottom = _hill_hollow(symbol, size)[1:]
    return top + bottom


def _butterfly(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(1, size + 1):
        rows.append(symbol * row + " " * ((size - row) * 2) + symbol * row)
    for row in range(size, 0, -1):
        rows.append(symbol * row + " " * ((size - row) * 2) + symbol * row)
    return rows


def _butterfly_hollow(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(1, size + 1):
        rows.append(_wing_line(symbol, row, size))
    for row in range(size, 0, -1):
        rows.append(_wing_line(symbol, row, size))
    return rows


def _x_pattern(symbol: str, size: int) -> list[str]:
    width = size * 2 - 1
    rows = []
    for row in range(width):
        line = []
        for col in range(width):
            line.append(symbol if col in (row, width - row - 1) else " ")
        rows.append("".join(line))
    return rows


def _plus_pattern(symbol: str, size: int) -> list[str]:
    width = size * 2 - 1
    middle = size - 1
    rows = []
    for row in range(width):
        if row == middle:
            rows.append(symbol * width)
        else:
            rows.append(" " * middle + symbol)
    return rows


def _right_wedge(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size * 2 - 1):
        width = size - abs(size - 1 - row)
        rows.append(symbol * width)
    return rows


def _left_wedge(symbol: str, size: int) -> list[str]:
    rows = []
    for row in range(size * 2 - 1):
        width = size - abs(size - 1 - row)
        rows.append(" " * (size - width) + symbol * width)
    return rows


def _chevron_down(symbol: str, size: int) -> list[str]:
    rows = []
    width = size * 2 - 1
    for row in range(size):
        line = []
        for col in range(width):
            line.append(symbol if col in (row, width - row - 1) else " ")
        rows.append("".join(line))
    return rows


def _chevron_up(symbol: str, size: int) -> list[str]:
    return list(reversed(_chevron_down(symbol, size)))


PATTERN_SPECS = [
    PatternSpec("solid-rectangle", "Solid rectangle", "Rectangles", "solid", "A filled block with adjustable width and height.", True),
    PatternSpec("hollow-rectangle", "Hollow rectangle", "Rectangles", "hollow", "A clean outline rectangle with empty interior space.", True),
    PatternSpec("checkerboard-rectangle", "Checkerboard rectangle", "Rectangles", "alternating", "A rectangle with alternating filled cells.", True),
    PatternSpec("solid-square", "Solid square", "Squares", "solid", "A balanced square built from the line count."),
    PatternSpec("hollow-square", "Hollow square", "Squares", "hollow", "A square outline built from the line count."),
    PatternSpec("right-triangle", "Right triangle", "Triangles", "solid", "Right angle on the lower-left edge."),
    PatternSpec("right-triangle-hollow", "Hollow right triangle", "Triangles", "hollow", "Outlined triangle with the hypotenuse rising right."),
    PatternSpec("right-triangle-reverse", "Reversed right triangle", "Triangles", "solid", "Right angle on the upper-left edge."),
    PatternSpec("right-triangle-reverse-hollow", "Hollow reversed right triangle", "Triangles", "hollow", "Outlined reversed triangle aligned to the left."),
    PatternSpec("left-triangle", "Left triangle", "Triangles", "solid", "Right-aligned triangle with the right angle at the bottom."),
    PatternSpec("left-triangle-hollow", "Hollow left triangle", "Triangles", "hollow", "Right-aligned triangle with only the border drawn."),
    PatternSpec("left-triangle-reverse", "Reversed left triangle", "Triangles", "solid", "Right-aligned triangle tapering downward."),
    PatternSpec("left-triangle-reverse-hollow", "Hollow reversed left triangle", "Triangles", "hollow", "Right-aligned outline triangle tapering downward."),
    PatternSpec("hill", "Hill", "Pyramids", "solid", "A centered pyramid that grows upward."),
    PatternSpec("hill-hollow", "Hollow hill", "Pyramids", "hollow", "A centered pyramid with only the outline and base."),
    PatternSpec("hill-reverse", "Inverted hill", "Pyramids", "solid", "A centered pyramid turned upside down."),
    PatternSpec("hill-reverse-hollow", "Hollow inverted hill", "Pyramids", "hollow", "An inverted outline pyramid."),
    PatternSpec("diamond", "Diamond", "Diamonds", "solid", "A symmetric full diamond pattern."),
    PatternSpec("diamond-hollow", "Hollow diamond", "Diamonds", "hollow", "A symmetric diamond outline with an open center."),
    PatternSpec("half-diamond", "Half diamond", "Diamonds", "solid", "A diamond profile that expands and contracts on the left."),
    PatternSpec("mirrored-half-diamond", "Mirrored half diamond", "Diamonds", "solid", "A right-aligned diamond profile."),
    PatternSpec("hourglass", "Hourglass", "Decorative", "solid", "Two pyramids meeting at the center."),
    PatternSpec("hourglass-hollow", "Hollow hourglass", "Decorative", "hollow", "An outlined hourglass with a narrow middle."),
    PatternSpec("butterfly", "Butterfly", "Decorative", "solid", "Mirrored wings expanding from the center."),
    PatternSpec("butterfly-hollow", "Hollow butterfly", "Decorative", "hollow", "A light outline version of the butterfly pattern."),
    PatternSpec("x-pattern", "X pattern", "Symbols", "hollow", "A diagonal cross built from the selected symbol."),
    PatternSpec("plus-pattern", "Plus pattern", "Symbols", "solid", "A centered plus sign."),
    PatternSpec("right-wedge", "Right wedge", "Arrows", "solid", "A wedge that points toward the right."),
    PatternSpec("left-wedge", "Left wedge", "Arrows", "solid", "A wedge that points toward the left."),
    PatternSpec("chevron-up", "Chevron up", "Arrows", "hollow", "A minimal upward chevron."),
    PatternSpec("chevron-down", "Chevron down", "Arrows", "hollow", "A minimal downward chevron."),
]

PATTERN_RENDERERS: dict[str, Callable[..., list[str]]] = {
    "solid-rectangle": _solid_rectangle,
    "hollow-rectangle": _hollow_rectangle,
    "checkerboard-rectangle": _checkerboard_rectangle,
    "solid-square": _solid_square,
    "hollow-square": _hollow_square,
    "right-triangle": _right_triangle,
    "right-triangle-hollow": _right_triangle_hollow,
    "right-triangle-reverse": _right_triangle_reverse,
    "right-triangle-reverse-hollow": _right_triangle_reverse_hollow,
    "left-triangle": _left_triangle,
    "left-triangle-hollow": _left_triangle_hollow,
    "left-triangle-reverse": _left_triangle_reverse,
    "left-triangle-reverse-hollow": _left_triangle_reverse_hollow,
    "hill": _hill,
    "hill-hollow": _hill_hollow,
    "hill-reverse": _hill_reverse,
    "hill-reverse-hollow": _hill_reverse_hollow,
    "diamond": _diamond,
    "diamond-hollow": _diamond_hollow,
    "half-diamond": _half_diamond,
    "mirrored-half-diamond": _mirrored_half_diamond,
    "hourglass": _hourglass,
    "hourglass-hollow": _hourglass_hollow,
    "butterfly": _butterfly,
    "butterfly-hollow": _butterfly_hollow,
    "x-pattern": _x_pattern,
    "plus-pattern": _plus_pattern,
    "right-wedge": _right_wedge,
    "left-wedge": _left_wedge,
    "chevron-up": _chevron_up,
    "chevron-down": _chevron_down,
}


def list_patterns() -> list[dict[str, object]]:
    return [spec.__dict__ for spec in PATTERN_SPECS]


def get_pattern(pattern_id: str) -> PatternSpec | None:
    return next((spec for spec in PATTERN_SPECS if spec.id == pattern_id), None)


def render_pattern(pattern_id: str, symbol: str = "*", size: int = 6, width: int = 12, height: int = 6) -> str:
    spec = get_pattern(pattern_id)
    if spec is None:
        raise ValueError("Unknown pattern.")

    clean_symbol = (symbol or "*")[:2]
    renderer = PATTERN_RENDERERS[pattern_id]

    if spec.requires_rectangle:
        rows = renderer(clean_symbol, _clamp(width, 1, 40), _clamp(height, 1, 24))
    else:
        rows = renderer(clean_symbol, _clamp(size, 1, 24))

    return "\n".join(rows)


def _edge_line(symbol: str, width: int, fill: bool = False) -> str:
    if width <= 1:
        return symbol
    if fill:
        return symbol * width
    return symbol + " " * (width - 2) + symbol


def _wing_line(symbol: str, row: int, size: int) -> str:
    inner_width = max(0, row - 2)
    outer_gap = " " * ((size - row) * 2)
    wing = symbol if row == 1 else symbol + " " * inner_width + symbol
    return wing + outer_gap + wing


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))
