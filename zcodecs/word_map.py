"""
La codificación de un texto usando un hashmap (diccionarios en python) es una de las formas más simples de compresión.

Tomemos como ejemplo el siguiente caso:

    In: "Anna amaria a Anna Maria."

Para este caso, podemos asociar a cada palabra un número único dentro de la secuencia. De esta forma
obtenemos como resultado:

    Out:
        0 -> "Anna"
        1 -> " "
        2 -> "amaria"
        3 -> "a"
        5 -> "Maria"
        6 -> "."

        +

        [0 1 2 1 3 1 0 1 5 6]

La salida está conformada por el diccionario que asocia cada palabra con su respectivo valor y
por un arreglo de números.

Cabe aclarar que este algoritmo no siempre genera una cadena comprimida. Si se desea guardar el resultado es necesario
almacenar el diccionario de palabras junto con la cadena comprimida para poder decodificarla, por lo que en secuencias
muy cortas o con pocas repeticiones puede resultar ineficiente.
"""

import re

from reader import Reader
from writer import Writer
from .codec import Codec


# Regexp para las palabras
_TOKEN = re.compile(r"\w+|\s+|[^\w\s]")


class WordMap(Codec):
    """
    Compresión por diccionario de palabras.

    Formato (enteros como varints):
        [n_palabras] ([largo][bytes utf-8])* [n_tokens] [índice]*
    """

    def encode(self, dst: Writer, src: Reader) -> bytes:
        text = src.read().decode("utf-8")

        ids: dict[str, int] = {}
        indexes = [ids.setdefault(t, len(ids)) for t in _TOKEN.findall(text)]

        out = bytearray(self._varint(len(ids)))
        for word in ids:  # conserva el orden de inserción
            raw = word.encode("utf-8")
            out += self._varint(len(raw)) + raw
        out += self._varint(len(indexes))
        for i in indexes:
            out += self._varint(i)

        b = bytes(out)
        dst.write(b)
        return b

    def decode(self, dst: Writer, src: Reader) -> bytes:
        data = src.read()
        pos = 0

        n_words, pos = self._read_varint(data, pos)
        words: list[str] = []
        for _ in range(n_words):
            size, pos = self._read_varint(data, pos)
            if pos + size > len(data):
                raise EOFError("Datos truncados")
            words.append(data[pos:pos + size].decode("utf-8"))
            pos += size

        n_tokens, pos = self._read_varint(data, pos)
        parts: list[str] = []
        for _ in range(n_tokens):
            index, pos = self._read_varint(data, pos)
            parts.append(words[index])

        b = bytes("".join(parts).encode("utf-8"))
        dst.write(b)
        return b

    @staticmethod
    def _varint(n: int) -> bytes:
        out = bytearray()
        while True:
            byte = n & 0x7F
            n >>= 7
            if not n:
                out.append(byte)
                return bytes(out)
            out.append(byte | 0x80)  # bit alto = "siguiente byte"

    @staticmethod
    def _read_varint(data: bytes, pos: int) -> tuple[int, int]:
        """Lee un varint desde 'pos'. Devuelve (valor, nueva_posición)."""
        result = shift = 0
        while pos < len(data):
            byte = data[pos]
            pos += 1
            result |= (byte & 0x7F) << shift
            if not byte & 0x80:
                return result, pos
            shift += 7
        raise EOFError("Datos truncados")
