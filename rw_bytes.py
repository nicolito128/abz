"""
Módulo con clases y funciones útiles para trabajar con streams de bytes.
"""

from reader import ReadCloser
from writer import WriteCloser


class Bytes(ReadCloser, WriteCloser):
    """
    Stream de bytes en memoria, legible y escribible.

    Las escrituras siempre se agregan al final del buffer y las lecturas
    consumen desde una posición propia, así que lo escrito se puede leer
    después en el mismo orden.
    """

    def __init__(self, data: bytes = b"") -> None:
        self._buffer = bytearray(data)
        self._pos = 0
        self._closed = False

    def read(self, n: int = -1) -> bytes:
        self._check_open()
        if n < 0:
            n = len(self._buffer) - self._pos
        chunk = bytes(self._buffer[self._pos:self._pos + n])
        self._pos += len(chunk)
        return chunk

    def write(self, data: bytes) -> int:
        self._check_open()
        self._buffer.extend(data)
        return len(data)

    def data(self) -> bytes:
        """Devuelve todo el contenido del buffer, sin importar lo ya leído."""
        return bytes(self._buffer)

    def close(self) -> None:
        self._closed = True

    def closed(self) -> bool:
        return self._closed

    def _check_open(self) -> None:
        if self._closed:
            raise ValueError("I/O operation on closed stream")
