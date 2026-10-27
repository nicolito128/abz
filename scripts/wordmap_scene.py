"""
Animación del algoritmo WordMap (compresión por diccionario de palabras).

Renderizar (calidad media):
    manim -pqm wordmap_scene.py WordMapAnimation

Calidad alta:
    manim -pqh wordmap_scene.py WordMapAnimation
"""

import re

from manim import *

TEXT = "Anna amaria a Anna Maria."
_TOKEN = re.compile(r"\w+|\s+|[^\w\s]")

PALETTE = [BLUE, GREEN, ORANGE, PINK, TEAL, PURPLE_B, RED_B, GOLD]


def show(tok: str) -> str:
    """Hace visibles los espacios."""
    return "␣" if tok.isspace() else tok


def varint_len(n: int) -> int:
    size = 1
    while n >= 0x80:
        n >>= 7
        size += 1
    return size


def encoded_size(tokens: list[str]) -> int:
    """Tamaño en bytes según el formato real de WordMap."""
    ids: dict[str, int] = {}
    indexes = [ids.setdefault(t, len(ids)) for t in tokens]
    total = varint_len(len(ids))
    for w in ids:
        raw = len(w.encode("utf-8"))
        total += varint_len(raw) + raw
    total += varint_len(len(indexes))
    total += sum(varint_len(i) for i in indexes)
    return total


class WordMapAnimation(Scene):
    def construct(self):
        tokens = _TOKEN.findall(TEXT)

        # ------------------------------------------------------------------
        # 1. Título e entrada
        # ------------------------------------------------------------------
        title = Text("WordMap: compresión por diccionario", font_size=36)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        input_text = Text(f'In: "{TEXT}"', font_size=34)
        input_text.move_to(UP * 1.5)
        self.play(FadeIn(input_text, shift=UP * 0.3))
        self.wait(1)

        # ------------------------------------------------------------------
        # 2. Tokenización
        # ------------------------------------------------------------------
        regex_label = Text(
            r"Tokens:  \w+  |  \s+  |  [^\w\s]",
            font_size=22,
            color=GREY_B,
        ).next_to(title, DOWN, buff=0.25)

        cells = VGroup()
        for t in tokens:
            label = Text(show(t), font_size=30)
            rect = SurroundingRectangle(label, color=GREY, buff=0.12, corner_radius=0.08)
            cells.add(VGroup(rect, label))
        cells.arrange(RIGHT, buff=0.08)
        if cells.width > 12.5:
            cells.scale_to_fit_width(12.5)
        cells.move_to(UP * 2.0)

        self.play(
            FadeOut(input_text, shift=UP * 0.3),
            FadeIn(regex_label),
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cells], lag_ratio=0.12),
            run_time=2,
        )
        self.wait(0.5)

        # ------------------------------------------------------------------
        # 3. Armado del diccionario y de la salida
        # ------------------------------------------------------------------
        dict_title = Text("Diccionario", font_size=28, color=YELLOW)
        dict_title.move_to(LEFT * 5 + UP * 0.6)
        out_title = Text("Salida (índices)", font_size=28, color=YELLOW)
        out_title.move_to(RIGHT * 1.5 + DOWN * 1.5)
        self.play(FadeIn(dict_title), FadeIn(out_title))

        box_size = 0.65
        out_origin = LEFT * 2.2 + DOWN * 2.5  # centro de la primera caja

        ids: dict[str, int] = {}
        rows: list[VGroup] = []
        index_labels: list[Text] = []
        out_boxes: list[VGroup] = []

        status = Text("", font_size=26)
        status.move_to(RIGHT * 2 + UP * 0.5)

        for k, (tok, cell) in enumerate(zip(tokens, cells)):
            hl = SurroundingRectangle(cell, color=YELLOW, buff=0.05, corner_radius=0.08)
            self.play(Create(hl), run_time=0.3)

            if tok not in ids:
                i = len(ids)
                ids[tok] = i
                color = PALETTE[i % len(PALETTE)]

                row = VGroup(
                    Text(str(i), font_size=26, color=color),
                    Text("→", font_size=26),
                    Text(f'"{show(tok)}"', font_size=26),
                ).arrange(RIGHT, buff=0.25)
                row.move_to(
                    LEFT * 5.8 + DOWN * (0.05 + 0.55 * i), aligned_edge=LEFT
                )
                rows.append(row)

                new_status = Text("¡Palabra nueva! → se agrega al diccionario",
                                  font_size=24, color=GREEN).move_to(status)
                self.play(
                    Transform(status, new_status),
                    FadeIn(row[0], row[1]),
                    TransformFromCopy(cell[1], row[2]),
                    cell[0].animate.set_color(color),
                    run_time=0.9,
                )
            else:
                i = ids[tok]
                color = PALETTE[i % len(PALETTE)]
                new_status = Text("Ya existe → se reutiliza su índice",
                                  font_size=24, color=ORANGE).move_to(status)
                self.play(
                    Transform(status, new_status),
                    Indicate(rows[i], color=YELLOW, scale_factor=1.15),
                    cell[0].animate.set_color(color),
                    run_time=0.9,
                )

            # índice debajo del token
            idx = Text(str(i), font_size=28, color=color)
            idx.next_to(cell, DOWN, buff=0.3)
            index_labels.append(idx)

            # caja en la salida
            box = VGroup(
                Square(side_length=box_size, color=color),
                Text(str(i), font_size=26, color=color),
            )
            box.move_to(out_origin + RIGHT * (box_size + 0.08) * k)
            out_boxes.append(box)

            self.play(
                TransformFromCopy(rows[i][0], idx),
                FadeOut(hl),
                run_time=0.5,
            )
            self.play(TransformFromCopy(idx, box), run_time=0.5)

        self.play(FadeOut(status))
        self.wait(0.5)

        # Resultado completo
        arr = [ids[t] for t in tokens]
        result = Text(f"{arr}", font_size=26, color=YELLOW)
        result.next_to(VGroup(*out_boxes), UP, buff=0.25)
        self.play(Write(result))
        self.wait(1.5)

        # ------------------------------------------------------------------
        # 4. Decodificación
        # ------------------------------------------------------------------
        self.play(
            FadeOut(cells),
            FadeOut(VGroup(*index_labels)),
            FadeOut(regex_label),
            FadeOut(result),
        )

        dec_title = Text("Decodificación: reemplazar cada índice por su palabra",
                         font_size=26, color=GREY_B)
        dec_title.next_to(title, DOWN, buff=0.3)
        self.play(
            FadeIn(dec_title),
            VGroup(*out_boxes).animate.move_to(RIGHT * 1.2 + UP * 1.4),
            out_title.animate.move_to(RIGHT * 1.2 + UP * 2.1),
        )

        anchor = LEFT * 1.8 + DOWN * 0.8
        decoded = Text("", font_size=32)
        decoded.move_to(anchor, aligned_edge=LEFT)
        inverse = {v: k for k, v in ids.items()}
        parts: list[str] = []

        for k, i in enumerate(arr):
            parts.append(show(inverse[i]))
            new_decoded = Text("".join(parts), font_size=32)
            new_decoded.move_to(anchor, aligned_edge=LEFT)
            self.play(
                Indicate(out_boxes[k], color=YELLOW),
                Indicate(rows[i], color=YELLOW, scale_factor=1.15),
                Transform(decoded, new_decoded),
                run_time=0.6,
            )

        final_text = Text(f'Out: "{TEXT}"', font_size=32, color=GREEN)
        final_text.move_to(anchor, aligned_edge=LEFT)
        self.play(Transform(decoded, final_text))
        self.wait(1.5)

        # ------------------------------------------------------------------
        # 5. ¿Realmente comprimió?
        # ------------------------------------------------------------------
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])

        original = len(TEXT.encode("utf-8"))
        encoded = encoded_size(tokens)

        s1 = Text(f"Original:    {original} bytes", font_size=34)
        s2 = Text(f"Codificado: {encoded} bytes (diccionario + índices)", font_size=34,
                  color=RED_B if encoded >= original else GREEN)
        VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.6)

        note = Text(
            "Hay que guardar el diccionario junto con los índices,\n"
            "así que con textos cortos o con pocas repeticiones\n"
            "el resultado puede ser más grande que la entrada.",
            font_size=26,
            color=GREY_B,
            line_spacing=0.9,
        ).next_to(VGroup(s1, s2), DOWN, buff=0.7)

        self.play(FadeIn(s1, shift=UP * 0.2))
        self.play(FadeIn(s2, shift=UP * 0.2))
        self.wait(0.5)
        self.play(Write(note))
        self.wait(3)
